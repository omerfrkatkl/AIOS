#!/usr/bin/env python3
"""
Weekly review - the owner's single touchpoint for decision visibility.

Answers three questions in at most 7 lines: what was decided since the last
review, what is waiting for approval, and what has gone stale.

Design decisions:
  - The "last review" marker is an append-only entry in DECISIONS.md, not a
    new state file. Nothing to keep in sync, and the review itself becomes
    part of the record.
  - Output is capped at 7 lines (a [dikkat] parameter in STATE.md). Attention
    is a resource; a summary nobody reads is worse than no summary.
  - Pending approvals are always listed in full. They are the actionable part;
    hiding them behind a flag is how decisions become invisible.

Usage:
  python tools/review.py            summary
  python tools/review.py --full     summary plus the full text of pending items
  python tools/review.py --done     record that a review happened
"""

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
DECISIONS = AIOS_DIR / "DECISIONS.md"
LEDGER = AIOS_DIR / "REJECTED.md"

REVIEW_TITLE = "Gözden geçirildi"
LINE_BUDGET = 7
REVIEW_DUE_DAYS = 7
STALE_LEDGER_DAYS = 21
PENDING_MARKERS = ("onaya açık", "onay bekliyor", "incelenmedi")
# Append-only log: an entry's status changes in a LATER entry, never in place.
# A closing entry carries `- **kapatır:** <date>/<title>` lines, which is a
# lightweight supersession link. Without it the log silently goes stale.
CLOSES = re.compile(r"^\s*-\s+\*\*kapatır:\*\*\s*(\d{4}-\d{2}-\d{2})/(.+?)\s*$")
# Whoever writes a closing line copies the header, so the tier/status suffix
# comes along. Tolerate it instead of documenting a rule nobody will re-read.
SUFFIX = re.compile(r"\s*·\s*T-[ABC]\b.*$")
TIER = re.compile(r"^T-[ABC]$")
APPROVED_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def parse_decisions() -> list[dict]:
    """Read DECISIONS.md entries. Titles may contain '·', so the tier token
    is located by pattern rather than by position."""
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
    """Every `kapatır:` reference found anywhere in the log."""
    keys = set()
    for entry in entries:
        for line in entry["body"]:
            hit = CLOSES.match(line)
            if hit:
                title = SUFFIX.sub("", hit.group(2)).strip()
                keys.add(f"{hit.group(1)}/{title}")
    return keys


def dangling_links(entries: list[dict], closed: set[str]) -> list[str]:
    """References that match no entry.

    The key is `date/title` where title excludes the tier and status suffix.
    Getting it wrong is easy and currently silent: the link simply does nothing
    and the log keeps lying. Observed on the first real use of the convention,
    so it must be reported rather than trusted.
    """
    real = {f"{e['date']}/{e['title']}" for e in entries}
    return sorted(k for k in closed if k not in real)


def is_pending(entry: dict, closed: set[str]) -> bool:
    """Status is read from the HEADER only, never from the body.

    Scanning the body matched entries that merely *described* approval in
    prose ("which decisions are awaiting approval") - the same substring
    fragility already fixed in the gate. If something needs approval, the
    header says so.
    """
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
STATE_WORD_CEILING = 900  # the 2-page [dikkat] parameter, roughly


def handoff_health(entries: list[dict]) -> list[str]:
    """Is STATE.md still trustworthy as the handoff surface?

    G13 asks for a handoff that is *verifiable*. STATE.md already carries the
    content; what was missing is anything that says whether it still holds.
    It once sat stale for weeks while decisions kept flowing, and only a
    human reading it caught that. These checks stay silent when healthy.
    """
    problems = []
    if not STATE.exists():
        return ["STATE.md MISSING - no handoff surface"]

    text = STATE.read_text(encoding="utf-8")
    stamp = STATE_UPDATED.search(text)
    latest = max((e["date"] for e in entries), default=None)

    if not stamp:
        problems.append("STATE.md has no 'Son güncelleme' stamp - staleness cannot be checked")
    elif latest and stamp.group(1) < latest:
        gap = (datetime.strptime(latest, "%Y-%m-%d")
               - datetime.strptime(stamp.group(1), "%Y-%m-%d")).days
        problems.append(
            f"STATE.md STALE - stamped {stamp.group(1)}, decisions run to {latest} ({gap}d behind)")

    words = len(text.split())
    if words > STATE_WORD_CEILING:
        problems.append(f"STATE.md over ceiling - {words} words (limit ~{STATE_WORD_CEILING}); prune, do not append")
    return problems


def ledger_health() -> str:
    if not LEDGER.exists():
        return "REJECTED: ledger missing"
    text = LEDGER.read_text(encoding="utf-8")
    approved = APPROVED_DATE.findall(
        "\n".join(l for l in text.splitlines() if "**approved:**" in l)
    )
    if not approved:
        return "REJECTED: 0 active records"
    gap = days_since(max(approved))
    flag = "  STALE" if gap > STALE_LEDGER_DAYS else ""
    return f"REJECTED: {len(approved)} active · last record {gap} days ago{flag}"


def summarise(full: bool) -> int:
    entries = parse_decisions()
    if not entries:
        print("DECISIONS.md is empty or unreadable.")
        return 1

    reviews = [e for e in entries if e["title"] == REVIEW_TITLE]
    last_review = reviews[-1]["date"] if reviews else None
    since = [e for e in entries if e["title"] != REVIEW_TITLE
             and (last_review is None or e["date"] > last_review)]

    lines = [f"REVIEW · {date.today().isoformat()}"]

    if last_review:
        gap = days_since(last_review)
        overdue = "  OVERDUE" if gap > REVIEW_DUE_DAYS else ""
        lines.append(f"Last review: {last_review} ({gap} days ago){overdue} · "
                     f"{len(since)} new decisions since")
        if gap > REVIEW_DUE_DAYS * 2:
            lines.append("Two reviews missed - T-A WIP limit drops to 1 (STATE rule).")
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
    lines.append(ledger_health())

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
    reviews = [e for e in entries if e["title"] == REVIEW_TITLE]
    since = [e for e in entries if e["title"] != REVIEW_TITLE
             and (not reviews or e["date"] > reviews[-1]["date"])]
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


TRACKED = [
    "CLAUDE.md", "STATE.md", "DECISIONS.md", "REJECTED.md", "REQUIREMENTS.md",
    "PROJECT-INSTRUCTIONS.md", "PROFILE.md",
    "hooks/gate.py", "tools/reject.py", "tools/review.py", "tools/bundle.py", "tools/decide.py",
    "tests/test_gate.py", "tests/diagnose_transcript.py",
    "adapters/claude-code/install.py", "adapters/claude-code/hook.json",
]


def fingerprints(_) -> int:
    """Short digest of every tracked file.

    Files are exchanged by hand between the chat and this machine, and a stale
    copy reports confidently wrong things. Comparing digests catches that in
    one line instead of two turns.
    """
    import hashlib
    for name in TRACKED:
        path = AIOS_DIR / name
        if not path.exists():
            print(f"{name:38} MISSING")
            continue
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()[:8]
        lines = raw.count(b"\n") + 1
        print(f"{name:38} {digest}  {lines:5} lines")
    return 0


def main() -> int:
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
