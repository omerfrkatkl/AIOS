#!/usr/bin/env python3
"""
Append a decision entry to DECISIONS.md in the exact format review.py expects.

Ported from arsiv/tools/decide.py (unchanged interface). The owner approves
decisions but does not write them; structured fields go straight in.

Usage:
  uv run --no-project python tools/decide.py --tier T-B --title "..." \\
      --decision "..." --reason "..." [--alternatives "A (elendi: ...)|B"] \\
      [--reversal "..."] [--evidence observed|generated|assumed] \\
      [--pending] [--closes "2026-08-23/Exact earlier title"] [--dry-run]
"""

import argparse
import sys
from datetime import date
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AIOS_DIR / "tools"))
from aioslog import log_event  # noqa: E402

DECISIONS = AIOS_DIR / "DECISIONS.md"
# CLI token with diacritics is hostile to typing/pasting on Windows. Accept
# ASCII and English aliases, write the canonical Turkish form.
EVIDENCE = {
    "gözlendi": "gözlendi", "gozlendi": "gözlendi", "observed": "gözlendi",
    "üretildi": "üretildi", "uretildi": "üretildi", "generated": "üretildi",
    "varsayıldı": "varsayıldı", "varsayildi": "varsayıldı", "assumed": "varsayıldı",
}


def build_entry(a) -> str:
    status = " · onaya açık" if a.pending else ""
    lines = [f"\n## {date.today().isoformat()} · {a.title} · {a.tier}{status}\n"]

    lines.append(f"- **Karar:** {a.decision}")
    lines.append(f"- **Gerekçe:** {a.reason}")

    if a.alternatives:
        parts = [p.strip() for p in a.alternatives.split("|") if p.strip()]
        lines.append(f"- **Alternatifler:** {' · '.join(parts)}")
    if a.reversal:
        lines.append(f"- **Geri alma:** {a.reversal}")
    if a.scores:
        lines.append(f"- **Puanlama (0–1, kanıt-atıflı):** {a.scores}")
    if a.sonuc_izle:
        lines.append("- **sonuç:** (değerlendirilecek — 4 hafta sonra revisit; sonuç ağırlıkları kalibre eder)")
    for key in a.closes or []:
        lines.append(f"- **kapatır:** {key}")
    for key in a.ilgili or []:
        lines.append(f"- **ilgili:** {key}")

    lines.append(f"- **Kanıt:** `[{EVIDENCE[a.evidence]}]`" + (f" — {a.evidence_note}" if a.evidence_note else ""))
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    p = argparse.ArgumentParser(description="Append a decision to DECISIONS.md")
    p.add_argument("--tier", required=True, choices=["T-A", "T-B", "T-C"])
    p.add_argument("--title", required=True)
    p.add_argument("--decision", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--alternatives", default="")
    p.add_argument("--reversal", default="")
    p.add_argument("--evidence", default="uretildi", choices=sorted(EVIDENCE),
                   metavar="observed|generated|assumed")
    p.add_argument("--evidence-note", default="")
    p.add_argument("--pending", action="store_true")
    p.add_argument("--closes", action="append", metavar="DATE/TITLE")
    p.add_argument("--ilgili", action="append", metavar="DATE/TITLE",
                   help="bağlantılı karar (ADR 'related' alanı)")
    p.add_argument("--scores", default="",
                   help="puanlama özeti; her puan kanıt atfı taşır (ör: 'uygunluk 0.9 [gözlendi: F10 raporu] | maliyet 0.6 [gözlendi: test]')")
    p.add_argument("--sonuc-izle", action="store_true",
                   help="sonuç-izleme alanı ekler (büyük kararlar: X hafta sonra revisit → kalibrasyon)")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    if a.tier == "T-A" and not (a.alternatives and a.reversal):
        print("ERROR: a T-A decision needs --alternatives and --reversal.")
        print("If neither applies, it is probably not a T-A.")
        return 1
    if a.scores and "[" not in a.scores:
        print("ERROR: her puan kanıt atfı taşımmalı — köşeli parantez içinde kaynak yok (G15: atıfsız puan geçersiz).")
        print("Örnek: --scores \"uygunluk 0.9 [gözlendi: F10 raporu] | maliyet 0.6 [gözlendi: test]\"")
        return 1

    entry = build_entry(a)
    if a.dry_run:
        print(entry)
        return 0

    if not DECISIONS.exists():
        print(f"ERROR: {DECISIONS} not found.")
        return 1
    with DECISIONS.open("a", encoding="utf-8") as f:
        f.write(entry)

    log_event("decide", "APPENDED", "info", a.title, tier=a.tier,
              pending=bool(a.pending))
    print(f"Appended: {a.title} [{a.tier}]" + (" - AWAITING APPROVAL" if a.pending else ""))
    if a.closes:
        print(f"Closes: {', '.join(a.closes)}")
    print("Run `uv run --no-project python tools/review.py` to confirm.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
