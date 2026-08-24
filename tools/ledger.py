#!/usr/bin/env python3
"""
The ledger tool (G6): draft, activate and inspect LEDGER.md records.

A record is born PENDING (no `active:` date) and is INERT at the gate. Only
the OWNER may activate a record (CLAUDE.md rule: the agent may not activate).
Activation is a mechanical field-fill, not a content edit.

Usage:
  uv run --no-project python tools/ledger.py --add --title "..." \\
      --status rejected|approved|deferred --keys "türkçe|english" \\
      --reason "..." --scope "..." [--strength firm|partial] \\
      [--alternative "..."] [--revisit YYYY-MM-DD]        # -> PENDING record
  uv run --no-project python tools/ledger.py --activate L-NNN [--date YYYY-MM-DD]
  uv run --no-project python tools/ledger.py --status
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AIOS_DIR / "tools"))
from aioslog import log_event, user_error  # noqa: E402

LEDGER = AIOS_DIR / "LEDGER.md"
HEAD = re.compile(r"^##\s+(L-\d+)\s*·\s*(.+?)\s*$")


def next_id(text: str) -> str:
    ids = [int(m.group(1)[2:]) for m in map(HEAD.match, text.splitlines()) if m]
    return f"L-{max(ids) + 1:03d}" if ids else "L-001"


def add_record(a) -> int:
    text = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
    lid = next_id(text)
    lines = [f"\n## {lid} · {a.title}", ""]
    for key in ("status", "keys", "reason", "scope", "strength", "alternative", "revisit"):
        val = getattr(a, key)
        if val:
            lines.append(f"- **{key}:** {val}")
    lines.append("")
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log_event("ledger", "ADDED", "info", f"{lid} {a.title} (PENDING)", status=a.status)
    print(f"Eklendi: {lid} · {a.title} · {a.status} · PENDING (kapıda etkisiz)")
    print(f"Aktifleştirme (yalnız SAHİP koşar): "
          f"uv run --no-project python tools/ledger.py --activate {lid}")
    return 0


def activate(lid: str, day: str) -> int:
    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    in_block, found, changed = False, False, False
    out = []
    for line in lines:
        head = HEAD.match(line)
        if head:
            if in_block and not changed:
                out.append(f"- **active:** {day}")  # block ended without the field
                changed = True
            in_block = head.group(1) == lid
            if in_block:
                found = True
        elif in_block and re.match(r"^\s*-\s+\*\*active:\*\*", line):
            line = f"- **active:** {day}"
            changed = True
        out.append(line)
    if in_block and not changed:
        out.append(f"- **active:** {day}")
        changed = True
    if not found:
        user_error(f"{lid} bulunamadı", "Kütükte böyle bir kayıt yok",
                   "uv run --no-project python tools/ledger.py --status ile listele")
        return 1
    if not changed:
        user_error(f"{lid} alanına tarih yazılamadı", "Blok yapısı beklenmedik",
                   "Kaydı elle incele: LEDGER.md")
        return 1
    LEDGER.write_text("\n".join(out) + "\n", encoding="utf-8")
    log_event("ledger", "ACTIVATED", "info", f"{lid} @ {day}")
    print(f"Aktifleştirildi: {lid} · active: {day}")
    return 0


def status() -> int:
    if not LEDGER.exists():
        print("LEDGER.md yok.")
        return 1
    text = LEDGER.read_text(encoding="utf-8")
    counts = {"approved": 0, "rejected": 0, "deferred": 0}
    pending, last_active = 0, ""
    current_status, current_active, in_block, in_fence = None, None, False, False
    for line in text.splitlines() + ["## L-999999 · sentinel"]:  # son kaydı da kapatır
        if line.strip().startswith("```"):
            in_fence = not in_fence  # şema örneği kayıt değildir
            continue
        if in_fence:
            continue
        head = HEAD.match(line)
        if head:
            if in_block and current_status is not None:
                if current_active and re.fullmatch(r"\d{4}-\d{2}-\d{2}", current_active):
                    counts[current_status] = counts.get(current_status, 0) + 1
                    last_active = max(last_active, current_active)
                else:
                    pending += 1
            in_block, current_status, current_active = True, None, None
        elif in_block:
            if line.startswith("- **status:**"):
                current_status = line.split("**status:**")[1].strip()
            elif line.startswith("- **active:**"):
                current_active = line.split("**active:**")[1].strip()
    print(f"LEDGER: approved {counts['approved']} · rejected {counts['rejected']} · "
          f"deferred {counts['deferred']} · PENDING {pending}")
    if last_active:
        from datetime import datetime
        gap = (date.today() - datetime.strptime(last_active, "%Y-%m-%d").date()).days
        flag = "  STALE (21 gün)" if gap > 21 else ""
        print(f"Son aktifleştirme: {last_active} ({gap} gün önce){flag}")
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    p = argparse.ArgumentParser(description="LEDGER.md records")
    p.add_argument("--add", action="store_true")
    p.add_argument("--title")
    p.add_argument("--record-status", dest="record_status",
                   choices=["approved", "rejected", "deferred"])
    p.add_argument("--keys")
    p.add_argument("--reason")
    p.add_argument("--scope")
    p.add_argument("--strength", default="firm", choices=["firm", "partial"])
    p.add_argument("--alternative", default="")
    p.add_argument("--revisit", default="")
    p.add_argument("--activate", metavar="L-NNN")
    p.add_argument("--date", default=date.today().isoformat())
    p.add_argument("--status", action="store_true", help="kütük sağlığı")
    a = p.parse_args()

    if a.activate:
        return activate(a.activate, a.date)
    if a.status:
        return status()
    if a.add:
        missing = [k for k in ("title", "record_status", "keys", "reason", "scope")
                   if not getattr(a, k)]
        if missing:
            user_error("Eksik alanlar", f"Gerekli: {', '.join(missing)}",
                       "--help ile alanları gör; scope zorunludur (kütük veto listesi değildir)")
            return 1
        if a.record_status == "deferred" and not a.revisit:
            user_error("deferred kayıt revisit tarihi istiyor",
                       "Erteleme tarihsiz olursa kapı süresiz uyarır",
                       "--revisit YYYY-MM-DD ekle")
            return 1
        a.status = a.record_status
        return add_record(a)
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
