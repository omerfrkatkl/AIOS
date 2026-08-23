#!/usr/bin/env python3
"""
Bundle the AIOS state into a single markdown file for handoff to a chat session.

A chat conversation has no persistent access to this folder, and files added by
hand to project knowledge go stale silently - that cost two turns of wrong
reports. One generated file removes the manual assembly step, and the digest
table makes drift impossible to miss.

Read trigger: at the start of a new chat conversation.

Usage:
  python tools/bundle.py            docs + code  -> handoff.md
  python tools/bundle.py --docs     documents only
  python tools/bundle.py -o FILE    write somewhere else
"""

import argparse
import hashlib
import sys
from datetime import datetime
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]

DOCS = ["STATE.md", "CLAUDE.md", "PROJECT-INSTRUCTIONS.md", "DECISIONS.md",
        "REJECTED.md", "REQUIREMENTS.md", "PROFILE.md"]
CODE = [
    "hooks/gate.py",
    "tools/reject.py",
    "tools/review.py",
    "tools/bundle.py",
    "tools/decide.py",
    "tests/test_gate.py",
    "tests/diagnose_transcript.py",
    "adapters/claude-code/install.py",
    "adapters/claude-code/hook.json",
]

# Embedded files may contain triple-backtick fences, so the outer fence is longer.
FENCE = "`" * 4
LANG = {".md": "markdown", ".py": "python", ".json": "json"}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()[:8]


def build(names: list[str]) -> str:
    present = [(n, AIOS_DIR / n) for n in names]
    missing = [n for n, p in present if not p.exists()]

    out = [
        "# AIOS — handoff bundle",
        "",
        f"Üretildi: {datetime.now().isoformat(timespec='seconds')} · "
        f"kaynak: `{AIOS_DIR}`",
        "",
        "> Bu dosya `tools/bundle.py` tarafından üretildi. Elle düzenlenmez.",
        "> Aşağıdaki parmak izleri `python tools/review.py --files` çıktısıyla eşleşmelidir.",
        "",
        "| Dosya | sha256[:8] | satır |",
        "|---|---|---|",
    ]

    for name, path in present:
        if not path.exists():
            out.append(f"| `{name}` | **MISSING** | — |")
            continue
        raw = path.read_bytes()
        out.append(f"| `{name}` | `{digest(raw)}` | {raw.count(chr(10).encode()[0]) + 1} |")

    if missing:
        out += ["", f"**Eksik dosyalar:** {', '.join(missing)}"]

    out.append("")
    for name, path in present:
        if not path.exists():
            continue
        out += [
            "---",
            "",
            f"## `{name}`",
            "",
            FENCE + LANG.get(path.suffix, ""),
            path.read_text(encoding="utf-8").rstrip(),
            FENCE,
            "",
        ]
    return "\n".join(out) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description="Bundle AIOS state into one markdown file")
    p.add_argument("--docs", action="store_true", help="documents only, no code")
    p.add_argument("-o", "--out", default="handoff.md")
    a = p.parse_args()

    names = DOCS if a.docs else DOCS + CODE
    text = build(names)
    target = AIOS_DIR / a.out
    target.write_text(text, encoding="utf-8")

    print(f"Wrote {target}")
    print(f"{len(names)} files · {len(text.splitlines()):,} lines · {len(text):,} chars")
    if not a.docs:
        print("Tip: --docs leaves out the code when only the state matters.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
