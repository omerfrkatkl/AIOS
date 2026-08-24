#!/usr/bin/env python3
"""
Active-decision digest for session opening (G26 token contract).

Reads DECISIONS.md and LEDGER.md, prints the still-binding slice:

- DECISIONS : entries from the last ACTIVE_DAYS days. Older entries are
              settled history; `why.py` (F4) searches the full log.
- LEDGER    : active records only (an `active:` date exists). PENDING
              records are counted, never shown as binding.

Prints only; never writes. Idempotent. Content is Turkish (conversation
record), code and CLI are English (language rule).
"""

import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "DECISIONS.md"
LEDGER = ROOT / "LEDGER.md"
ACTIVE_DAYS = 14

DEC_HEAD = re.compile(
    r"^##\s+(?P<date>\d{4}-\d{2}-\d{2})\s+·\s+(?P<title>.+?)(?:\s+·\s+T-[ABC].*)?$"
)
LED_HEAD = re.compile(r"^##\s+(?P<id>L-\d+)\s+·\s+(?P<title>.+?)\s*$")
FIELD = re.compile(r"^-\s+\*\*(?P<key>[a-z]+):\*\*\s*(?P<val>.*)$")


def decisions_section(today: date) -> None:
    print("KARARLAR (son %d gün):" % ACTIVE_DAYS)
    if not DECISIONS.exists():
        print("  DECISIONS.md yok")
        return
    cutoff = today - timedelta(days=ACTIVE_DAYS)
    shown = 0
    for line in DECISIONS.read_text(encoding="utf-8").splitlines():
        m = DEC_HEAD.match(line)
        if not m:
            continue
        d = datetime.strptime(m.group("date"), "%Y-%m-%d").date()
        if d >= cutoff:
            print(f"  [{m.group('date')}] {m.group('title')}")
            shown += 1
    if shown == 0:
        print(f"  (son {ACTIVE_DAYS} günde karar girişi yok)")


def ledger_section(today: date) -> None:
    print("KÜTÜK (aktif kayıtlar):")
    if not LEDGER.exists():
        print("  LEDGER.md yok")
        return
    text = LEDGER.read_text(encoding="utf-8")
    records, block, in_fence = [], None, False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence  # şema örneği kayıt değildir
            continue
        if in_fence:
            continue
        if line.startswith("## L-"):
            if block is not None:
                records.append(block)
            block = {"head": line[3:].strip(), "fields": {}}
        elif block is not None:
            m = FIELD.match(line)
            if m:
                block["fields"][m.group("key")] = m.group("val").strip()
    if block is not None:
        records.append(block)

    active, pending = [], []
    for rec in records:
        f = rec["fields"]
        if f.get("active"):
            entry = f"  {rec['head']} · {f.get('status', '?')}"
            if f.get("status") == "deferred":
                if f.get("revisit"):
                    try:
                        rv = datetime.strptime(f["revisit"], "%Y-%m-%d").date()
                        entry += f" · revisit {f['revisit']}" + (
                            "" if rv >= today else " (revisit geçti - sessiz)")
                    except ValueError:
                        entry += f" · revisit {f['revisit']} (biçim hatalı)"
                else:
                    entry += " · revisit tarihi yok (hatalı kayıt)"
            active.append(entry)
        else:
            pending.append(rec["head"])
    for e in active:
        print(e)
    if not active:
        print("  (aktif kayıt yok)")
    if pending:
        print(f"  PENDING (kapıda etkisiz, sahibin tarihi bekler): {len(pending)}")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    today = date.today()
    print(f"AKTİF KARAR ÖZETİ · {today.isoformat()}")
    decisions_section(today)
    ledger_section(today)
    return 0


if __name__ == "__main__":
    sys.exit(main())
