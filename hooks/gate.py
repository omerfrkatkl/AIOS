#!/usr/bin/env python3
"""
AIOS gate - Claude Code Stop hook.

Scans each completed response against the REJECTED ledger. On a match it exits
with code 2, which blocks completion and feeds the rejection rationale back to
the model via stderr.

Design decisions (see DECISIONS.md, 2026-08-15):
  - Deterministic script. Never relies on the model "remembering".
  - v1 matching is lexical: stem + ordered subsequence + window. No embeddings,
    no LLM judge. Volume of records matters more than matching precision here.
  - FAIL-OPEN: on any error the gate lets work continue and leaves a canary
    trace. Failing closed would halt all work.
  - NEVER SILENTLY SUPPRESS: the model is told to surface the match to the
    owner, not to abandon the idea. False suppression is the worse failure.
"""

import json
import os
import re
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path

# Windows consoles default to cp1252 and mangle UTF-8. The block message
# reaches Claude Code through stderr, so this is mandatory.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

AIOS_DIR = Path(os.environ.get("AIOS_DIR", Path(__file__).resolve().parents[1]))
LEDGER_PATH = AIOS_DIR / "REJECTED.md"
CANARY_LOG = AIOS_DIR / ".gate-canary.log"

# G12: warn once when a session grows long WITHOUT anything being written out.
# Length alone is not the risk - a long session that keeps updating STATE and
# DECISIONS is healthy. Length with no externalisation is where context dies.
# The threshold is a [hipotez]: lower it if it never fires, raise it if it
# fires while the session still feels fine. Override with AIOS_SESSION_LIMIT.
SESSION_CHAR_LIMIT = int(os.environ.get("AIOS_SESSION_LIMIT", 120_000))
EXTERNALISED = ("STATE.md", "DECISIONS.md")

STEM_LEN = 4
WINDOW = 15
APPROVED_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def canary(event: str) -> None:
    """Proof that the gate actually ran. This is the trigger measurement."""
    try:
        # BOM is written only when the file is first created; PowerShell and
        # Notepad read BOM-less UTF-8 as ANSI and mangle Turkish characters.
        encoding = "utf-8-sig" if not CANARY_LOG.exists() else "utf-8"
        with CANARY_LOG.open("a", encoding=encoding) as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')}\t{event}\n")
    except Exception:
        pass


def normalize(text: str) -> str:
    """Flatten text for comparison. Applied identically to both sides.

    Folding 'ı' to 'i' is deliberate: Turkish casing turns 'AIOS' into 'aıos',
    which would miss the 'aios' key. Acronyms appear in keys far more often
    than Turkish words that depend on the dotless i.
    """
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("İ", "i").replace("I", "i")
    text = text.lower().replace("ı", "i")
    text = re.sub(r"[^\w\sğüşöç]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def _stem(token: str) -> str:
    """Crude Turkish stem: drop the suffix. 'içinde' and 'içine' both -> 'için'."""
    return token[:STEM_LEN] if len(token) > STEM_LEN else token


def _stems(text: str) -> list[str]:
    return [_stem(t) for t in normalize(text).split() if len(t) > 2]


def _phrase_hit(key: str, text_stems: list[str], text_words: list[str]) -> bool:
    """Do the key's words appear IN ORDER within a window of the text?

    Three constraints work together:
      - stem match       tolerates Turkish inflection ('içinde' ~ 'içine')
      - order preserved  separates 'projeleri aios içinde' from 'aios için ... proje'
      - window           prevents scattered accidental matches
    Single-word keys require an exact match instead of a stem: 'graphiti'
    stems to 'grap' and would collide with 'graph'.
    """
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
        for stem in key_stems:  # ordered subsequence search
            try:
                index = segment.index(stem, index + 1)
            except ValueError:
                ok = False
                break
        if ok:
            return True
    return False


def parse_ledger(path: Path) -> list[dict]:
    """Read REJECTED.md into records. Only approved records are returned.

    'approved' must be a YYYY-MM-DD date. Placeholders such as PENDING leave
    the record inert, so the model may draft freely while only the owner can
    activate a record.
    """
    if not path.exists():
        return []
    records, current = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        header = re.match(r"^##\s+(R-\d+)\s*·\s*(.+?)\s*$", line)
        if header:
            if current:
                records.append(current)
            current = {"id": header.group(1), "title": header.group(2)}
            continue
        if current is None:
            continue
        field = re.match(r"^\s*-\s+\*\*(\w+):\*\*\s*(.+?)\s*$", line)
        if field:
            current[field.group(1)] = field.group(2)
    if current:
        records.append(current)
    return [
        r for r in records
        if r.get("keys") and APPROVED_DATE.fullmatch((r.get("approved") or "").strip())
    ]


def find_matches(response: str, records: list[dict]) -> list[dict]:
    """Which records have a key phrase present in the response."""
    text_stems = _stems(response)
    text_words = normalize(response).split()
    hits = []
    for record in records:
        matched = [
            k.strip() for k in record["keys"].split("|")
            if k.strip() and _phrase_hit(k, text_stems, text_words)
        ]
        if matched:
            hits.append({**record, "matched": matched})
    return hits


def build_block_message(hits: list[dict]) -> str:
    lines = ["GATE: this response matches a previously rejected proposal.", ""]
    for hit in hits:
        lines += [
            f"[{hit['id']}] {hit['title']}",
            f"  matched key : {', '.join(hit['matched'])}",
            f"  reason      : {hit.get('reason', '(none)')}",
            f"  scope       : {hit.get('scope', '(none)')}",
            f"  strength    : {hit.get('strength', '(none)')}",
            f"  alternative : {hit.get('alternative', '(none)')}",
            "",
        ]
    lines += [
        "WHAT TO DO - do not silently drop the idea:",
        "1. Tell the owner about this match explicitly.",
        "2. Judge whether the proposal falls OUTSIDE the rejection's scope; if it does, say why.",
        "3. Leave the decision to the owner: proceed anyway?",
        "False suppression costs more than repeating a proposal.",
    ]
    return "\n".join(lines)


def _collect_text(node) -> list[str]:
    """Gather text blocks from a content node. Tolerant of schema variants."""
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
    """Is this an assistant message? Accepts several schema variants.

    isSidechain entries are subagent output, not the main response; the gate
    must skip them. (Observed in a real transcript.)
    """
    if entry.get("isSidechain"):
        return False
    if entry.get("type") == "assistant" or entry.get("role") == "assistant":
        return True
    message = entry.get("message")
    return isinstance(message, dict) and message.get("role") == "assistant"


def last_assistant_text(transcript_path: str) -> str:
    """Extract the latest assistant message from the transcript JSONL.

    The Stop hook can fire before the final message is flushed to disk, so
    this retries briefly.
    """
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
                        continue  # partially written trailing line
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
    """Timestamp of the transcript's first entry, as epoch seconds."""
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


def long_session_warning(payload: dict) -> str | None:
    """Advisory, at most once per session. Returns the message or None."""
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

    # Already warned in this session? The canary log is the record; no new file.
    try:
        if CANARY_LOG.exists() and f"LONG-SESSION {session[:8]}" in CANARY_LOG.read_text(
                encoding="utf-8", errors="replace"):
            return None
    except Exception:
        pass

    started = session_start(transcript)
    if started:
        for name in EXTERNALISED:
            path = AIOS_DIR / name
            if path.exists() and path.stat().st_mtime > started:
                return None  # something was written out; the session is healthy

    canary(f"LONG-SESSION {session[:8]} | {size} chars | nothing externalised")
    return (
        f"GATE: this session has reached {size:,} characters and neither STATE.md nor "
        "DECISIONS.md has been written during it.\n\n"
        "Length alone is fine; length without externalisation is where context dies.\n\n"
        "WHAT TO DO:\n"
        "1. Write what has been decided into DECISIONS.md and update STATE.md.\n"
        "2. Run `python tools/review.py` and show the owner the result.\n"
        "3. Suggest continuing in a fresh session.\n"
        "This advisory fires once per session and will not repeat."
    )


def demo() -> int:
    """Try the gate without Claude Code: scan sample text and print the message."""
    sample = " ".join(a for a in sys.argv[2:]) or "Let's use a graph based memory layer."
    records = parse_ledger(LEDGER_PATH)
    print(f"Ledger : {len(records)} approved records")
    print(f"Text   : {sample}\n")
    hits = find_matches(sample, records)
    if not hits:
        print("No match - the gate would not block.")
        return 0
    print(build_block_message(hits))
    print("\n(This text reaches Claude Code through stderr.)")
    return 0


def main() -> int:
    if "--demo" in sys.argv:
        return demo()

    try:
        payload = json.load(sys.stdin)
    except Exception as exc:
        canary(f"ERROR could not read input: {exc}")
        return 0

    # Loop guard: if the gate already blocked once, do not block again.
    if payload.get("stop_hook_active"):
        canary("SKIPPED stop_hook_active")
        return 0

    try:
        records = parse_ledger(LEDGER_PATH)
        if not records:
            canary("FIRED no approved records")
            return 0

        transcript = payload.get("transcript_path", "")
        response = last_assistant_text(transcript)
        if not response.strip():
            canary(f"FIRED empty response | transcript={transcript}")
            return 0

        hits = find_matches(response, records)
        if not hits:
            warning = long_session_warning(payload)
            if warning:
                print(warning, file=sys.stderr)
                return 2
            canary(f"FIRED clean | {len(records)} records | {len(response)} chars")
            return 0

        canary(f"BLOCKED {','.join(h['id'] for h in hits)}")
        print(build_block_message(hits), file=sys.stderr)
        return 2

    except Exception as exc:
        # Fail-open: an error must not halt work, but must leave a trace.
        canary(f"ERROR fail-open: {exc}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
