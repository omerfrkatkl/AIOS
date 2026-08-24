#!/usr/bin/env python3
"""
Bundle the AIOS state into one markdown file for chat handoff.

Hybrid privacy (2026-08-23): PROFILE.md and LEDGER.md are LOCAL-ONLY and
EXCLUDED by default - a bundle may be shared in public channels. Only an
explicit --personal (owner's call) includes them.

Usage:
  uv run --no-project python tools/bundle.py            docs + code -> handoff.md
  uv run --no-project python tools/bundle.py --docs     documents only
  uv run --no-project python tools/bundle.py --personal include local layer
  uv run --no-project python tools/bundle.py -o FILE
"""

import argparse
import hashlib
import sys
from datetime import datetime
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]

DOCS = ["STATE.md", "CLAUDE.md", "PROJECT-INSTRUCTIONS.md", "DECISIONS.md",
        "REQUIREMENTS.md", "vision.md", "PLAN.md", "README.md"]
LOCAL = ["PROFILE.md", "LEDGER.md"]
CODE = [
    "hooks/gate.py",
    "tools/summary.py", "tools/context_cost.py", "tools/aioslog.py",
    "tools/review.py", "tools/decide.py", "tools/ledger.py", "tools/why.py",
    "tools/bundle.py", "tools/milestone.py",
    "tests/test_gate.py",
    "adapters/claude-code/install.py", "adapters/claude-code/hook.json",
    "adapters/opencode/install.py", "adapters/opencode/gate-plugin.js",
]

FENCE = "`" * 4
LANG = {".md": "markdown", ".py": "python", ".json": "json", ".js": "javascript"}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()[:8]


def build(names: list[str]) -> str:
    present = [(n, AIOS_DIR / n) for n in names]
    missing = [n for n, p in present if not p.exists()]
    out = [
        "# AIOS — handoff bundle", "",
        f"Üretildi: {datetime.now().isoformat(timespec='seconds')} · kaynak: `{AIOS_DIR}`", "",
        "> `tools/bundle.py` üretimi. Elle düzenlenmez.",
        "> Parmak izleri `tools/review.py --files` çıktısıyla eşleşmelidir.", "",
        "| Dosya | sha256[:8] | satır |", "|---|---|",
    ]
    for name, path in present:
        if not path.exists():
            out.append(f"| `{name}` | **MISSING** | — |")
            continue
        raw = path.read_bytes()
        out.append(f"| `{name}` | `{digest(raw)}` | {raw.count(b(chr(10))) + 1 if False else raw.count(bytes([10])) + 1} |")
    if missing:
        out += ["", f"**Eksik dosyalar:** {', '.join(missing)}"]
    out.append("")
    for name, path in present:
        if not path.exists():
            continue
        out += ["---", "", f"## `{name}`", "", FENCE + LANG.get(path.suffix, ""),
                path.read_text(encoding="utf-8").rstrip(), FENCE, ""]
    return "\n".join(out) + "\n"


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    p = argparse.ArgumentParser(description="Bundle AIOS state into one markdown file")
    p.add_argument("--docs", action="store_true", help="documents only, no code")
    p.add_argument("--personal", action="store_true",
                   help="include PROFILE/LEDGER (owner's call - never share publicly)")
    p.add_argument("-o", "--out", default="handoff.md")
    a = p.parse_args()

    names = DOCS if a.docs else DOCS + CODE
    if a.personal:
        names = names + LOCAL
    text = build(names)
    target = AIOS_DIR / a.out
    target.write_text(text, encoding="utf-8")
    print(f"Wrote {target}")
    print(f"{len(names)} dosya · {len(text.splitlines()):,} satır · {len(text):,} bayt")
    if not a.personal:
        print("Not: kişisel katman (PROFILE/LEDGER) dışarıda — --personal ile eklenir.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
