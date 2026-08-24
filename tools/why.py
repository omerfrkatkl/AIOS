#!/usr/bin/env python3
"""
why.py - "Neden böyle?" komutu (G17/G25).

Searches the active brain AND the archive for the query terms and prints
matching lines with file:line. Turkish folding applied to both sides.

Usage:
  uv run --no-project python tools/why.py topoloji
  uv run --no-project python tools/why.py knowledge graph
"""

import sys
import unicodedata
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
TARGETS = [
    AIOS_DIR / "DECISIONS.md",
    AIOS_DIR / "LEDGER.md",
    AIOS_DIR / "REQUIREMENTS.md",
    AIOS_DIR / "CLAUDE.md",
    AIOS_DIR / "PLAN.md",
    AIOS_DIR / "vision.md",
    AIOS_DIR / "arsiv" / "DECISIONS.md",
    AIOS_DIR / "arsiv" / "REJECTED.md",
    AIOS_DIR / "arsiv" / "vision.md",
]


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("İ", "i").replace("I", "i")
    return text.lower().replace("ı", "i")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    terms = [fold(t) for t in sys.argv[1:] if t.strip()]
    if not terms:
        print("Kullanım: uv run --no-project python tools/why.py <terimler...>")
        return 1

    hits = 0
    for path in TARGETS:
        if not path.exists():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception as exc:
            print(f"{path.name}: okunamadı ({exc})")
            continue
        rel = path.relative_to(AIOS_DIR)
        for i, line in enumerate(lines, 1):
            folded = fold(line)
            if all(t in folded for t in terms):
                print(f"{rel}:{i}: {line.strip()[:110]}")
                hits += 1

    print(f"\n{hits} eşleşme." + ("" if hits else " Arşivde de yok - bu konuda kayıt yok."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
