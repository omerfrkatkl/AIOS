#!/usr/bin/env python3
"""
AIOS gate v3 - enforcement hook (F4).

Scans each completed response against LEDGER.md (three states):
  rejected (active) -> BLOCK: exit 2, rationale fed back via stderr
  deferred (active, revisit not passed) -> WARN: exit 2 with advisory text
  approved / PENDING / expired-deferred -> silent

Ported behaviours (behaviour inventory, 2026-08-24 - see arsiv/hooks/gate.py):
  - Deterministic script; never relies on the model "remembering".
  - Lexical matcher: Turkish folding + stem + ordered subsequence + window.
  - FAIL-OPEN: any error lets work continue and leaves a log trace.
  - NEVER SILENTLY SUPPRESS: surface the match, judge the scope, owner decides.
  - Loop guard: stop_hook_active skips the second pass.
  - Sidechain (subagent) transcript entries are skipped.
  - Transcript read retries briefly (flush race observed once).
  - Long-session advisory: length + nothing externalised, once per session.
  - --demo: try the gate without any agent tool.
  - --scan-file PATH: detection mode for surfaces that cannot block (opencode).

Changes vs v2: LEDGER.md three-state records, aioslog (logs/aios.jsonl)
replaces the private canary file, deferred-warning channel added.
"""

import json
import os
import re
import sys
import time
import unicodedata
from datetime import date, datetime
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REAL_ROOT = Path(__file__).resolve().parents[1]  # tools/ her zaman burada; AIOS_DIR override edilse de
AIOS_DIR = Path(os.environ.get("AIOS_DIR", REAL_ROOT))
sys.path.insert(0, str(REAL_ROOT / "tools"))
from aioslog import log_event  # noqa: E402

LEDGER_PATH = AIOS_DIR / "LEDGER.md"

SESSION_CHAR_LIMIT = int(os.environ.get("AIOS_SESSION_LIMIT", 120_000))
EXTERNALISED = ("STATE.md", "DECISIONS.md")

STEM_LEN = 4
WINDOW = 15
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def normalize(text: str) -> str:
    """Flatten text for comparison. Applied identically to both sides.

    Folding 'ı' to 'i' is deliberate: Turkish casing turns 'AIOS' into 'aıos',
    which would miss the 'aios' key.
    """
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("İ", "i").replace("I", "i")
    text = text.lower().replace("ı", "i")
    text = re.sub(r"[^\w\sğüşöç]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def _stem(token: str) -> str:
    return token[:STEM_LEN] if len(token) > STEM_LEN else token


def _stems(text: str) -> list[str]:
    return [_stem(t) for t in normalize(text).split() if len(t) > 2]


def _phrase_hit(key: str, text_stems: list[str], text_words: list[str]) -> bool:
    """Key words appear IN ORDER within a window (stem + order + window)."""
    key_stems = _stems(key)
    if not key_stems:
        return False
    if len(key_stems) == 1:
        exact = normalize(key).split()
        return len(exact) == 1 and exact[0] in text_words
    window = max(WINDOW, len(key_stems) * 3)
    for start in range(max(1, len(text_stems) - window + 1)):
        segment = text_stems[start:start + window]
        index, ok = -1, True
        for stem in key_stems:
            try:
                index = segment.index(stem, index + 1)
            except ValueError:
                ok = False
                break
        if ok:
            return True
    return False


def parse_ledger(path: Path) -> dict:
    """Read LEDGER.md -> {"reject": [rec], "defer": [rec]}.

    A record is ACTIVE only when `active:` holds a YYYY-MM-DD date (PENDING
    otherwise). deferred counts while revisit >= today (missing/broken revisit
    stays in warn - a broken date must not silence a deferred idea).
    """
    out = {"reject": [], "defer": []}
    if not path.exists():
        return out
    today = date.today()
    records, current, in_fence = [], None, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence  # schema example is not a record
            continue
        if in_fence:
            continue
        header = re.match(r"^##\s+(L-\d+)\s*·\s*(.+?)\s*$", line)
        if header:
            if current:
                records.append(current)
            current = {"id": header.group(1), "title": header.group(2), "fields": {}}
            continue
        if current is None:
            continue
        field = re.match(r"^\s*-\s+\*\*(\w+):\*\*\s*(.+?)\s*$", line)
        if field:
            current["fields"][field.group(1)] = field.group(2).strip()
    if current:
        records.append(current)

    for rec in records:
        f = rec["fields"]
        if not f.get("keys") or not DATE_RE.fullmatch(f.get("active", "")):
            continue  # PENDING: inert at the gate
        status = f.get("status", "")
        if status == "rejected":
            out["reject"].append(rec)
        elif status == "deferred":
            try:
                rv = datetime.strptime(f.get("revisit", ""), "%Y-%m-%d").date()
                if rv < today:
                    continue  # expired: silent
            except ValueError:
                pass  # broken revisit stays in warn
            out["defer"].append(rec)
    return out


def find_matches(response: str, records: list[dict]) -> list[dict]:
    text_stems = _stems(response)
    text_words = normalize(response).split()
    hits = []
    for record in records:
        keys = record["fields"].get("keys", "")
        matched = [
            k.strip() for k in keys.split("|")
            if k.strip() and _phrase_hit(k, text_stems, text_words)
        ]
        if matched:
            hits.append({**record, "matched": matched})
    return hits


def _detail(hit: dict) -> list[str]:
    f = hit["fields"]
    return [
        f"[{hit['id']}] {hit['title']}",
        f"  matched key : {', '.join(hit['matched'])}",
        f"  reason      : {f.get('reason', '(none)')}",
        f"  scope       : {f.get('scope', '(none)')}",
        f"  strength    : {f.get('strength', '(none)')}",
        f"  alternative : {f.get('alternative', '(none)')}",
        "",
    ]


def build_block_message(hits: list[dict]) -> str:
    lines = ["GATE: this response matches a previously REJECTED proposal.", ""]
    for hit in hits:
        lines += _detail(hit)
    lines += [
        "WHAT TO DO - do not silently drop the idea:",
        "1. Tell the owner about this match explicitly.",
        "2. Judge whether the proposal falls OUTSIDE the rejection's scope; if it does, say why.",
        "3. Leave the decision to the owner: proceed anyway?",
        "False suppression costs more than repeating a proposal.",
    ]
    return "\n".join(lines)


def build_defer_message(hits: list[dict]) -> str:
    lines = ["GATE: this response matches a previously DEFERRED proposal (advisory).", ""]
    for hit in hits:
        lines += _detail(hit)
        lines.append(f"  revisit      : {hit['fields'].get('revisit', '(none)')}")
        lines.append("")
    lines += [
        "WHAT TO DO - this is a warning, not a veto:",
        "1. Tell the owner this matches a deferred idea and when it is due for revisit.",
        "2. If the owner wants to proceed now, he will say so - then continue.",
        "3. Do not silently drop the idea either way.",
    ]
    return "\n".join(lines)


def _collect_text(node) -> list[str]:
    out = []
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, dict):
        if node.get("type") == "text" and isinstance(node.get("text"), str):
            out.append(node["text"])
        elif isinstance(node.get("text"), str) and "type" not in node:
            out.append(node["text"])
        else:
            for key in ("content", "message"):
                if key in node:
                    out += _collect_text(node[key])
    elif isinstance(node, list):
        for item in node:
            out += _collect_text(item)
    return out


def _is_assistant(entry: dict) -> bool:
    """Sidechain entries are subagent output - the gate skips them."""
    if entry.get("isSidechain"):
        return False
    if entry.get("type") == "assistant" or entry.get("role") == "assistant":
        return True
    message = entry.get("message")
    return isinstance(message, dict) and message.get("role") == "assistant"


def last_assistant_text(transcript_path: str) -> str:
    """Latest assistant message; retries briefly (flush race observed once)."""
    for attempt in range(4):
        if attempt:
            time.sleep(0.25)
        try:
            entries = []
            with open(transcript_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except Exception:
            continue
        for entry in reversed(entries):
            if not _is_assistant(entry):
                continue
            parts = [p for p in _collect_text(entry.get("message", entry)) if p.strip()]
            if parts:
                return "\n".join(parts)
    return ""


def session_start(transcript_path: str) -> float | None:
    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                stamp = json.loads(line).get("timestamp")
                if stamp:
                    return datetime.fromisoformat(stamp.replace("Z", "+00:00")).timestamp()
                return Path(transcript_path).stat().st_ctime
    except Exception:
        return None
    return None


def _warned_before(session: str) -> bool:
    from aioslog import last_events
    return any(
        session[:8] in str(rec.get("msg", "")) + str(rec.get("session", ""))
        for rec in last_events(source="gate", event_prefix="LONG-SESSION", limit=200)
    )


def long_session_warning(payload: dict) -> str | None:
    """Advisory, at most once per session (G12)."""
    transcript = payload.get("transcript_path", "")
    session = payload.get("session_id") or payload.get("sessionId") or ""
    if not transcript or not session:
        return None
    try:
        size = Path(transcript).stat().st_size
    except Exception:
        return None
    if size < SESSION_CHAR_LIMIT:
        return None
    if _warned_before(session):
        return None
    started = session_start(transcript)
    if started:
        for name in EXTERNALISED:
            path = AIOS_DIR / name
            if path.exists() and path.stat().st_mtime > started:
                return None
    log_event("gate", "LONG-SESSION", "warn", f"LONG-SESSION {session[:8]}",
              session=session[:8], size=size)
    return (
        f"GATE: this session has reached {size:,} characters and neither STATE.md nor "
        "DECISIONS.md has been written during it.\n\n"
        "Length alone is fine; length without externalisation is where context dies.\n\n"
        "WHAT TO DO:\n"
        "1. Write what has been decided into DECISIONS.md and update STATE.md.\n"
        "2. Run `uv run --no-project python tools/review.py` and show the owner the result.\n"
        "3. Suggest continuing in a fresh session.\n"
        "This advisory fires once per session and will not repeat."
    )


def scan_text(text: str) -> int:
    """Matching flow for demo and --scan-file (no long-session advisory)."""
    ledger = parse_ledger(LEDGER_PATH)
    reject, defer = ledger["reject"], ledger["defer"]
    if not reject and not defer:
        print("No active records - the gate would not act.")
        return 0
    if not text.strip():
        print("Empty text - the gate would not act.")
        return 0
    hits = find_matches(text, reject)
    if hits:
        print(build_block_message(hits), file=sys.stderr)
        return 2
    hits = find_matches(text, defer)
    if hits:
        print(build_defer_message(hits), file=sys.stderr)
        return 2
    print("No match - the gate would not act.")
    return 0


def demo() -> int:
    sample = " ".join(a for a in sys.argv[2:]) or "Let's use a graph based memory layer."
    ledger = parse_ledger(LEDGER_PATH)
    total = len(ledger["reject"]) + len(ledger["defer"])
    print(f"Ledger : {total} active records "
          f"({len(ledger['reject'])} rejected, {len(ledger['defer'])} deferred)")
    print(f"Text   : {sample}\n")
    scan_text(sample)
    print("\n(Block/warn text reaches the agent through stderr.)")
    return 0


def _in_scope(cwd: str) -> bool:
    """AIOS dir is always in scope; managed projects opt in via a `.aios`
    marker at their root (written by the F8 new-project ritual). Walks up
    from cwd so project subdirectories are covered too."""
    if not cwd:
        return False
    cwd_p = Path(cwd)
    try:
        if os.path.commonpath([str(cwd_p), str(AIOS_DIR)]) == str(AIOS_DIR):
            return True
    except ValueError:
        pass
    for base in [cwd_p, *cwd_p.parents]:
        if (base / ".aios").exists():
            return True
    return False


def main() -> int:
    if "--demo" in sys.argv:
        return demo()

    if "--scan-file" in sys.argv:
        path = sys.argv[sys.argv.index("--scan-file") + 1]
        surface = "scan-file"
        if "--surface" in sys.argv:
            surface = sys.argv[sys.argv.index("--surface") + 1]
        try:
            text = Path(path).read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            log_event("gate", "ERROR", "error", f"scan-file unreadable: {exc}")
            return 0
        try:
            ledger = parse_ledger(LEDGER_PATH)
            hits = find_matches(text, ledger["reject"])
            if hits:
                log_event("gate", "BLOCKED", "warn", ",".join(h["id"] for h in hits),
                          surface=surface)
                return 0
            hits = find_matches(text, ledger["defer"])
            if hits:
                log_event("gate", "DEFERRED-WARN", "warn", ",".join(h["id"] for h in hits),
                          surface=surface)
                return 0
            log_event("gate", "FIRED", "info", "clean", surface=surface)
        except Exception as exc:
            log_event("gate", "ERROR", "error", f"fail-open: {exc}")
        return 0  # detection mode never blocks

    try:
        payload = json.load(sys.stdin)
    except Exception as exc:
        log_event("gate", "ERROR", "error", f"could not read input: {exc}")
        return 0

    # Loop guard: if the gate already blocked once, do not block again.
    if payload.get("stop_hook_active"):
        log_event("gate", "SKIPPED", "info", "stop_hook_active")
        return 0

    # Scope filter: the hook is installed at user level, so it fires for EVERY
    # Claude Code session on this machine. AIOS enforcement applies to sessions
    # inside the AIOS directory and to opted-in managed projects (`.aios`
    # marker). Everything else is skipped SILENTLY - no log, no latency.
    cwd = os.path.abspath(os.path.expanduser(payload.get("cwd") or ""))
    if not _in_scope(cwd):
        return 0

    try:
        ledger = parse_ledger(LEDGER_PATH)
        reject, defer = ledger["reject"], ledger["defer"]
        if not reject and not defer:
            log_event("gate", "FIRED", "info", "no active records")
            return 0

        transcript = payload.get("transcript_path", "")
        response = last_assistant_text(transcript)
        if not response.strip():
            log_event("gate", "FIRED", "info", "empty response", transcript=transcript)
            return 0

        hits = find_matches(response, reject)
        if hits:
            log_event("gate", "BLOCKED", "warn", ",".join(h["id"] for h in hits))
            print(build_block_message(hits), file=sys.stderr)
            return 2

        hits = find_matches(response, defer)
        if hits:
            log_event("gate", "DEFERRED-WARN", "warn", ",".join(h["id"] for h in hits))
            print(build_defer_message(hits), file=sys.stderr)
            return 2

        warning = long_session_warning(payload)
        if warning:
            print(warning, file=sys.stderr)
            return 2

        log_event("gate", "FIRED", "info", "clean",
                  records=len(reject) + len(defer), chars=len(response))
        return 0

    except Exception as exc:
        # Fail-open: an error must not halt work, but must leave a trace.
        log_event("gate", "ERROR", "error", f"fail-open: {exc}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
