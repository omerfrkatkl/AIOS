#!/usr/bin/env python3
"""
Add, approve and audit records in the REJECTED ledger.

Design principle: the model may draft freely, but a record stays inert until
the OWNER approves it (the gate ignores records whose 'approved' field is not
a date). This stops a confabulated rule from silently becoming permanent.

Kullanım:
  python tools/reject.py --add --title "..." --keys "a|b|c" \\
         --reason "..." [--scope "..."] [--strength firm|partial] [--alternative "..."]

  python tools/reject.py --approve R-006
  python tools/reject.py --status
"""

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
LEDGER = AIOS_DIR / "REJECTED.md"
STALE_DAYS = 21  # warn if no record has been added for this long


def read_records() -> list[dict]:
    if not LEDGER.exists():
        return []
    records, current = [], None
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
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
    return records


def is_approved(record: dict) -> bool:
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", (record.get("approved") or "").strip()))


def next_id(records: list[dict]) -> str:
    highest = max((int(r["id"].split("-")[1]) for r in records), default=0)
    return f"R-{highest + 1:03d}"


def is_ascii(phrase: str) -> bool:
    return all(ord(c) < 128 for c in phrase)


def add(a) -> int:
    keys = [k.strip() for k in a.keys.split("|") if k.strip()]
    if len(keys) < 3:
        print(f"ERROR: at least 3 keys required, got {len(keys)}.")
        print("Keys must be bilingual - the model sometimes answers in English.")
        return 1
    if not any(is_ascii(k) for k in keys):
        print("WARNING: no ASCII key. An English paraphrase could slip through.")

    records = read_records()
    new_id = next_id(records)

    block = [
        f"\n## {new_id} · {a.title}\n",
        f"- **keys:** {' | '.join(keys)}",
        f"- **reason:** {a.reason}",
        f"- **scope:** {a.scope}",
        f"- **strength:** {a.strength}",
        f"- **alternative:** {a.alternative}",
        "- **approved:** PENDING",
        "",
    ]
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write("\n".join(block))

    print(f"{new_id} added as a draft - INERT AT THE GATE.")
    print(f"To approve: python tools/reject.py --approve {new_id}")
    return 0


def approve(a) -> int:
    target = a.approve.upper()
    text = LEDGER.read_text(encoding="utf-8")
    records = {r["id"]: r for r in read_records()}

    if target not in records:
        print(f"ERROR: {target} not found. Available: {', '.join(records) or '(none)'}")
        return 1
    if is_approved(records[target]):
        print(f"{target} is already approved ({records[target]['approved']}).")
        return 0

    record = records[target]
    print(f"\n{target} · {record['title']}")
    for field in ("keys", "reason", "scope", "strength", "alternative"):
        print(f"  {field:12}: {record.get(field, '(none)')}")

    if input("\nApprove? (y/n) ").strip().lower() not in ("y", "yes", "e", "evet"):
        print("Cancelled.")
        return 1

    today = date.today().isoformat()
    pattern = re.compile(rf"(##\s+{target}\s+·.*?- \*\*approved:\*\* )PENDING", re.S)
    updated, count = pattern.subn(rf"\g<1>{today}", text)
    if not count:
        print("ERROR: approved line not found, fix by hand.")
        return 1
    LEDGER.write_text(updated, encoding="utf-8")
    print(f"{target} approved ({today}). The gate now sees this record.")
    return 0


def status(_) -> int:
    records = read_records()
    active = [r for r in records if is_approved(r)]
    pending = [r for r in records if not is_approved(r)]

    print(f"Total records : {len(records)}")
    print(f"Active        : {len(active)}  (visible to the gate)")
    print(f"Pending       : {len(pending)}")

    for r in pending:
        print(f"  ! {r['id']} · {r['title']}")

    monolingual = [r for r in active
                   if not any(is_ascii(k.strip()) for k in r["keys"].split("|"))]
    if monolingual:
        print(f"\nMonolingual keys ({len(monolingual)}) - English paraphrase may slip through:")
        for r in monolingual:
            print(f"  ~ {r['id']} · {r['title']}")

    if active:
        latest = max(r["approved"] for r in active)
        days = (date.today() - datetime.strptime(latest, "%Y-%m-%d").date()).days
        print(f"\nLatest approved record: {latest} ({days} days ago)")
        if days > STALE_DAYS:
            print(f"STALENESS WARNING: nothing added for over {STALE_DAYS} days.")
            print("A ledger with no feeding path dies. Was there really no rejection?")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="REJECTED ledger tool")
    p.add_argument("--add", action="store_true")
    p.add_argument("--approve", metavar="R-NNN")
    p.add_argument("--status", action="store_true")
    p.add_argument("--title", default="")
    p.add_argument("--keys", default="")
    p.add_argument("--reason", default="")
    p.add_argument("--scope", default="Not specified.")
    p.add_argument("--strength", default="firm", choices=["firm", "partial"])
    p.add_argument("--alternative", default="(none)")
    a = p.parse_args()

    if a.approve:
        return approve(a)
    if a.status:
        return status(a)
    if a.add:
        if not (a.title and a.keys and a.reason):
            print("ERROR: --title, --keys and --reason are required.")
            return 1
        return add(a)
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
