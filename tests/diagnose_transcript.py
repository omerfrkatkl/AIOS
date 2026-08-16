#!/usr/bin/env python3
"""
Transcript teşhisi — kapı yanıtı neden okuyamıyor?

Claude Code transcript'lerinin GERÇEK yapısını raporlar. Tahmin etmek yerine ölçer.

Kullanım:
    python tests\\diagnose_transcript.py
    python tests\\diagnose_transcript.py "C:\\yol\\transcript.jsonl"   # belirli dosya
"""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks"))
from gate import last_assistant_text, _is_assistant, _collect_text  # noqa: E402


def newest_transcript() -> Path | None:
    root = Path.home() / ".claude" / "projects"
    if not root.exists():
        return None
    files = sorted(root.rglob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def describe(node, depth: int = 0, max_depth: int = 3) -> str:
    pad = "  " * depth
    if depth >= max_depth:
        return f"{pad}..."
    if isinstance(node, dict):
        lines = []
        for k, v in list(node.items())[:12]:
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}{k}:")
                lines.append(describe(v, depth + 1, max_depth))
            else:
                s = repr(v)
                lines.append(f"{pad}{k} = {s[:60]}{'...' if len(s) > 60 else ''}")
        return "\n".join(lines)
    if isinstance(node, list):
        if not node:
            return f"{pad}[] (boş)"
        return f"{pad}[{len(node)} öğe] ilk öğe:\n" + describe(node[0], depth + 1, max_depth)
    s = repr(node)
    return f"{pad}{s[:60]}"


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else newest_transcript()
    if not path or not path.exists():
        print("Transcript bulunamadı. ~/.claude/projects altında .jsonl yok.")
        print("Claude Code'da bir konuşma yapıp tekrar dene.")
        return 1

    print(f"Dosya : {path}")
    print(f"Boyut : {path.stat().st_size:,} bayt\n")

    entries, bozuk = [], 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            bozuk += 1

    print(f"Satır : {len(entries)} geçerli, {bozuk} ayrıştırılamayan")
    print(f"type  : {dict(Counter(e.get('type', '(yok)') for e in entries))}")
    print(f"role  : {dict(Counter(e.get('role', '(yok)') for e in entries))}")

    asistanlar = [e for e in entries if _is_assistant(e)]
    print(f"\nAsistan olarak tanınan girdi: {len(asistanlar)}")

    if not asistanlar:
        print("\n>>> SORUN BURADA: hiçbir girdi asistan mesajı olarak tanınmıyor.")
        print(">>> Son girdinin yapısı:\n")
        if entries:
            print(describe(entries[-1]))
        return 2

    son = asistanlar[-1]
    print(f"Üst anahtarlar: {list(son)}")
    parcalar = _collect_text(son.get("message", son))
    dolu = [p for p in parcalar if p.strip()]
    print(f"Çıkarılan metin bloğu: {len(parcalar)} ({len(dolu)} dolu)")

    sonuc = last_assistant_text(str(path))
    if sonuc.strip():
        print(f"\nSONUÇ: OKUNDU — {len(sonuc)} karakter")
        print(f"  ilk 200: {sonuc[:200]!r}")
        print("\nKapı artık yanıtı okuyabiliyor. Sorun yarış koşuluydu ya da eski ayrıştırıcıydı.")
        return 0

    print("\n>>> SORUN: asistan girdisi tanındı ama metin çıkarılamadı.")
    print(">>> Son asistan girdisinin yapısı:\n")
    print(describe(son))
    return 3


if __name__ == "__main__":
    sys.exit(main())
