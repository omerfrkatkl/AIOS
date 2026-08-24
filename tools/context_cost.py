#!/usr/bin/env python3
"""
Session-opening context measurement (G26/G27 token contract).

Primary metric: lines + bytes of the opening contract files
  STATE.md + PROFILE.md + the summary.py output (the active-decision digest).

Baseline (2026-08-23, pre-restructure): 892 lines / 77,447 bytes.
Target (G27): <= 50% of baseline lines (<= 446).

Prints only; never writes. Idempotent.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from aioslog import log_event  # noqa: E402

BASELINE_LINES = 892
BASELINE_BYTES = 77_447
TARGET_LINES = BASELINE_LINES // 2  # 446


def count(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    return text.count("\n") + 1, len(text.encode("utf-8"))


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    total_lines, total_bytes = 0, 0
    print("AÇILIŞ BAĞLAMI (G26 sözleşmesi):")
    for name in ("STATE.md", "PROFILE.md"):
        p = ROOT / name
        if not p.exists():
            print(f"  {name:12} EKSİK")
            continue
        l, b = count(p)
        total_lines += l
        total_bytes += b
        print(f"  {name:12} {l:4} satır {b:6} bayt")

    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "summary.py")],
        capture_output=True, text=True, encoding="utf-8",
    )
    out = r.stdout or ""
    l = out.count("\n") + (1 if out.strip() else 0)
    b = len(out.encode("utf-8"))
    total_lines += l
    total_bytes += b
    print(f"  {'özet':12} {l:4} satır {b:6} bayt")

    print(f"  {'TOPLAM':12} {total_lines:4} satır {total_bytes:6} bayt")
    print(f"BAZAL : {BASELINE_LINES} satır / {BASELINE_BYTES} bayt")
    verdict = "HEDEF TUTTU" if total_lines <= TARGET_LINES else "HEDEF AŞILDI"
    print(f"HEDEF : <= {TARGET_LINES} satır (bazalın %50'si) -> {verdict}")
    log_event("context_cost", "MEASURED", "info", f"{total_lines} satır / {total_bytes} bayt",
              lines=total_lines, bytes=total_bytes, verdict=verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
