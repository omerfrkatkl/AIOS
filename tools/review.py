#!/usr/bin/env python3
"""
Weekly review - the owner's single touchpoint for decision visibility (v2).

Answers in at most ~7 healthy lines: what was decided since the last review,
what waits for approval, what has gone stale, ledger health, gate recency.

Design decisions carried from v2 (arsiv):
  - The "last review" marker is an append-only entry in DECISIONS.md.
  - Output stays silent when healthy; over-budget lines mean decisions pile up.
  - Pending approvals are always listed in full.
  - Status is read from the entry HEADER only, never the body.
v2 additions: LEDGER three-state health, gate recency from logs/aios.jsonl,
token trend from context_cost events, rules-pointer check.

Usage:
  uv run --no-project python tools/review.py            summary
  uv run --no-project python tools/review.py --full     summary + pending texts
  uv run --no-project python tools/review.py --done     record that a review happened
  uv run --no-project python tools/review.py --files    digest of every tracked file
"""

import argparse
import hashlib
import re
import sys
from datetime import date, datetime
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AIOS_DIR / "tools"))
from aioslog import last_events  # noqa: E402

DECISIONS = AIOS_DIR / "DECISIONS.md"
LEDGER = AIOS_DIR / "LEDGER.md"
POINTER = AIOS_DIR.parent / "CLAUDE.md"
POINTER_IMPORT = "@AIOS/CLAUDE.md"

REVIEW_TITLE = "Gözden geçirildi"
LINE_BUDGET = 7
REVIEW_DUE_DAYS = 7
STALE_LEDGER_DAYS = 21
PENDING_MARKERS = ("onaya açık", "onay bekliyor", "incelenmedi")
CLOSES = re.compile(r"^\s*-\s+\*\*kapatır:\*\*\s*(\d{4}-\d{2}-\d{2})/(.+?)\s*$")
SUFFIX = re.compile(r"\s*·\s*T-[ABC]\b.*$")
TIER = re.compile(r"^T-[ABC]$")
APPROVED_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")

TRACKED = [
    "CLAUDE.md", "STATE.md", "DECISIONS.md", "REQUIREMENTS.md", "PLAN.md",
    "vision.md", "PROJECT-INSTRUCTIONS.md", "README.md", "LICENSE", "EMERGENCY.md",
    "hooks/gate.py", "tools/summary.py", "tools/context_cost.py", "tools/aioslog.py",
    "tools/review.py", "tools/decide.py", "tools/ledger.py", "tools/why.py",
    "tools/bundle.py", "tools/backup.py", "tools/milestone.py", "tools/audit.py",
    "tools/sindir.py", "tools/registry.py", "tools/kesif.py", "tools/kotu.py",
    "tests/test_gate.py",
    "adapters/claude-code/hook.json", "adapters/claude-code/install.py",
    "adapters/opencode/gate-plugin.js", "adapters/opencode/install.py",
]


def parse_decisions() -> list[dict]:
    if not DECISIONS.exists():
        return []
    entries, current = [], None
    for line in DECISIONS.read_text(encoding="utf-8").splitlines():
        if not line.startswith("## "):
            if current is not None:
                current["body"].append(line)
            continue
        parts = [p.strip() for p in line[3:].split("·")]
        if not parts or not APPROVED_DATE.fullmatch(parts[0]):
            continue
        tier_at = next((i for i, p in enumerate(parts) if TIER.fullmatch(p)), None)
        title = " · ".join(parts[1:tier_at]) if tier_at else " · ".join(parts[1:])
        current = {
            "date": parts[0],
            "title": title,
            "tier": parts[tier_at] if tier_at else "T-C",
            "status": " · ".join(parts[tier_at + 1:]) if tier_at else "",
            "body": [],
        }
        entries.append(current)
    return entries


def closed_keys(entries: list[dict]) -> set[str]:
    keys = set()
    for entry in entries:
        for line in entry["body"]:
            hit = CLOSES.match(line)
            if hit:
                title = SUFFIX.sub("", hit.group(2)).strip()
                keys.add(f"{hit.group(1)}/{title}")
    return keys


def dangling_links(entries: list[dict], closed: set[str]) -> list[str]:
    real = {f"{e['date']}/{e['title']}" for e in entries}
    return sorted(k for k in closed if k not in real)


def is_pending(entry: dict, closed: set[str]) -> bool:
    if f"{entry['date']}/{entry['title']}" in closed:
        return False
    status = entry["status"].lower()
    if "onaylandı" in status:
        return False
    return any(marker in status for marker in PENDING_MARKERS)


def days_since(iso: str) -> int:
    return (date.today() - datetime.strptime(iso, "%Y-%m-%d").date()).days


STATE = AIOS_DIR / "STATE.md"
STATE_UPDATED = re.compile(r"\*\*Son güncelleme\*\*\s*\|\s*(\d{4}-\d{2}-\d{2})")
STATE_WORD_CEILING = 900


def handoff_health(entries: list[dict]) -> list[str]:
    problems = []
    if not STATE.exists():
        return ["STATE.md MISSING - no handoff surface"]
    text = STATE.read_text(encoding="utf-8")
    stamp = STATE_UPDATED.search(text)
    latest = max((e["date"] for e in entries), default=None)
    if not stamp:
        problems.append("STATE.md has no 'Son güncelleme' stamp")
    elif latest and stamp.group(1) < latest:
        gap = (datetime.strptime(latest, "%Y-%m-%d")
               - datetime.strptime(stamp.group(1), "%Y-%m-%d")).days
        problems.append(f"STATE.md STALE - stamped {stamp.group(1)}, {gap}d behind decisions")
    words = len(text.split())
    if words > STATE_WORD_CEILING:
        problems.append(f"STATE.md over ceiling - {words} words; prune, do not append")
    return problems


def rules_pointer_health() -> list[str]:
    problems = []
    if not POINTER.exists():
        problems.append(f"rules pointer MISSING - {POINTER}")
    elif POINTER_IMPORT not in POINTER.read_text(encoding="utf-8"):
        problems.append(f"rules pointer STALE - no {POINTER_IMPORT}")
    return problems


def ledger_health() -> list[str]:
    """Three-state counts + PENDING + staleness (G6). Fenced blocks are schema
    examples, not records - same rule as the gate and summary parsers."""
    if not LEDGER.exists():
        return ["LEDGER: missing"]
    text = LEDGER.read_text(encoding="utf-8")
    counts = {"approved": 0, "rejected": 0, "deferred": 0}
    pending, last_active, current_active, current_status = 0, "", False, None
    in_fence = False
    for line in text.splitlines() + ["## L-999999 sentinel"]:  # son kaydı da kapatır
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## L-"):
            if current_status is not None:
                if current_active and APPROVED_DATE.fullmatch(current_active):
                    counts[current_status] = counts.get(current_status, 0) + 1
                    last_active = max(last_active, current_active)
                else:
                    pending += 1
            current_status, current_active = None, None
        elif line.startswith("- **status:**"):
            current_status = line.split("**status:**")[1].strip()
        elif line.startswith("- **active:**"):
            current_active = line.split("**active:**")[1].strip()
    out = [f"LEDGER: approved {counts['approved']} · rejected {counts['rejected']} · "
           f"deferred {counts['deferred']} · PENDING {pending}"]
    if last_active:
        gap = days_since(last_active)
        if gap > STALE_LEDGER_DAYS:
            out[0] += f"  STALE - last activation {gap}d ago (beslenmeyen kütük ölür)"
    return out


def gate_recency() -> list[str]:
    """Did the gate actually fire recently? (the 'working mechanism needs proof' lesson)"""
    events = last_events(source="gate", limit=500)
    if not events:
        return ["GATE: hiç ateşlenmemiş - kuruldu mu? canlı test gerekli"]
    last = events[-1]
    ts = last.get("ts", "")[:16]
    return [f"GATE: son olay {ts} {last.get('event', '')}"]


def token_trend() -> list[str]:
    events = [e for e in last_events(source="context_cost", event_prefix="MEASURED", limit=3)]
    if not events:
        return []
    last = events[-1]
    return [f"CONTEXT: son açılış {last.get('lines', '?')} satır (hedef ≤446, bazal 892)"]


def research_health() -> list[str]:
    """Rapor tazeliği: tetiği geçmiş raporlar bayat sinyali verir (F10 v2)."""
    rdir = AIOS_DIR / "research"
    if not (rdir / "README.md").exists():
        return ["RESEARCH: hat yok"]
    today = date.today().isoformat()
    stale, fresh = [], 0
    for rp in sorted(rdir.glob("R-*.md")):
        text = rp.read_text(encoding="utf-8")
        m = re.search(r"\|\s*\*{0,2}tetik\*{0,2}\s*\|\s*(\d{4}-\d{2}-\d{2})", text)
        rid_m = re.search(r"\|\s*\*{0,2}id\*{0,2}\s*\|\s*([^|]+?)\s*\|", text)
        rid = (rid_m.group(1) if rid_m else rp.stem)[:12]
        if m and m.group(1) < today:
            stale.append(f"{rid} ({m.group(1)})")
        else:
            fresh += 1
    out = [f"RESEARCH: {fresh} taze" + (f" · STALE: {', '.join(stale)}" if stale else "")]
    return out


def summarise(full: bool) -> int:
    entries = parse_decisions()
    if not entries:
        print("DECISIONS.md is empty or unreadable.")
        return 1

    # Aynı-gün kararı kaçırma düzeltmesi: tarih-dizisi karşılaştırması yerine
    # dosya-sırası (append-only garantisi) — son 'Gözden geçirildi' girişinden
    # SONRAKİ her şey yeni sayılır.
    review_indices = [i for i, e in enumerate(entries) if e["title"] == REVIEW_TITLE]
    if review_indices:
        cut = review_indices[-1]
        last_review = entries[cut]["date"]
        since = [e for e in entries[cut + 1:] if e["title"] != REVIEW_TITLE]
    else:
        last_review = None
        since = [e for e in entries if e["title"] != REVIEW_TITLE]

    lines = [f"REVIEW · {date.today().isoformat()}"]
    if last_review:
        gap = days_since(last_review)
        overdue = "  OVERDUE" if gap > REVIEW_DUE_DAYS else ""
        lines.append(f"Last review: {last_review} ({gap} days ago){overdue} · "
                     f"{len(since)} new decisions since")
        if gap > REVIEW_DUE_DAYS * 2:
            lines.append("Two reviews missed - T-A WIP limit drops to 1.")
    else:
        lines.append(f"No review recorded yet · {len(since)} decisions in the log")

    counts = {t: sum(1 for e in since if e["tier"] == t) for t in ("T-A", "T-B", "T-C")}
    lines.append(f"Tiers: T-A {counts['T-A']} · T-B {counts['T-B']} · T-C {counts['T-C']}")

    closed = closed_keys(entries)
    pending = [e for e in entries if e["title"] != REVIEW_TITLE and is_pending(e, closed)]
    if pending:
        lines.append(f"AWAITING APPROVAL ({len(pending)}):")
        for e in pending:
            lines.append(f"  * {e['date']} · {e['tier']} · {e['title']}")
    else:
        lines.append("Awaiting approval: none")

    dangling = dangling_links(entries, closed)
    if dangling:
        lines.append(f"DANGLING kapatır ({len(dangling)}) - these close nothing:")
        for key in dangling:
            lines.append(f"  ? {key}")

    lines.extend(handoff_health(entries))
    lines.extend(rules_pointer_health())
    lines.extend(ledger_health())
    lines.extend(gate_recency())
    lines.extend(token_trend())
    lines.extend(research_health())

    for line in lines:
        print(line)
    if len(lines) > LINE_BUDGET:
        print(f"\n[{len(lines)} lines, budget {LINE_BUDGET}] "
              "Over budget means decisions are piling up, not that the budget is wrong.")

    if full and pending:
        print("\n--- pending items in full ---")
        for e in pending:
            print(f"\n## {e['date']} · {e['title']} · {e['tier']}")
            print("\n".join(e["body"]).strip())
    return 0


def mark_done(_) -> int:
    entries = parse_decisions()
    review_indices = [i for i, e in enumerate(entries) if e["title"] == REVIEW_TITLE]
    if review_indices:
        cut = review_indices[-1]
        since = [e for e in entries[cut + 1:] if e["title"] != REVIEW_TITLE]
    else:
        since = [e for e in entries if e["title"] != REVIEW_TITLE]
    closed = closed_keys(entries)
    pending = [e for e in entries if e["title"] != REVIEW_TITLE and is_pending(e, closed)]

    today = date.today().isoformat()
    block = [
        f"\n## {today} · {REVIEW_TITLE} · T-C\n",
        f"- **Kapsam:** {len(since)} karar gözden geçirildi.",
        f"- **Onay bekleyen:** {len(pending)}"
        + (f" — {', '.join(e['title'][:40] for e in pending)}" if pending else " (yok)"),
        "- **Kanıt:** `[gözlendi]` — `tools/review.py --done`",
        "",
    ]
    with DECISIONS.open("a", encoding="utf-8") as f:
        f.write("\n".join(block))
    print(f"Review recorded for {today}: {len(since)} decisions, {len(pending)} pending.")
    if pending:
        print("Note: pending items stay pending. Recording a review is not approving them.")
    return 0


def fingerprints(_) -> int:
    """Short digest of every tracked file - catches stale copies in one line."""
    for name in TRACKED:
        path = AIOS_DIR / name
        if not path.exists():
            print(f"{name:42} MISSING")
            continue
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()[:8]
        lines = raw.count(b"\n") + 1
        print(f"{name:42} {digest}  {lines:5} lines")
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    p = argparse.ArgumentParser(description="Weekly decision review")
    p.add_argument("--full", action="store_true", help="show pending items in full")
    p.add_argument("--done", action="store_true", help="record that a review happened")
    p.add_argument("--files", action="store_true", help="digest of every tracked file")
    a = p.parse_args()
    if a.files:
        return fingerprints(a)
    return mark_done(a) if a.done else summarise(a.full)


if __name__ == "__main__":
    sys.exit(main())
