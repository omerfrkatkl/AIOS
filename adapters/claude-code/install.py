#!/usr/bin/env python3
"""
AIOS kapısının Claude Code adaptörünü kurar.

Ne yapar : adapters/claude-code/hook.json içindeki hooks bloğunu
           ~/.claude/settings.json dosyasına BİRLEŞTİRİR.
Ne yapmaz: mevcut ayarların üzerine yazmaz. Var olan her anahtar korunur.

Kullanım:
    python adapters/claude-code/install.py            # kur
    python adapters/claude-code/install.py --dry-run  # sadece göster
    python adapters/claude-code/install.py --uninstall # kapıyı kaldır
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

ADAPTER_DIR = Path(__file__).resolve().parent
AIOS_DIR = ADAPTER_DIR.parents[1]
HOOK_SRC = ADAPTER_DIR / "hook.json"
TARGET = Path.home() / ".claude" / "settings.json"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8").strip()
    return json.loads(text) if text else {}


def is_aios_hook(entry: dict) -> bool:
    return any(
        "gate.py" in h.get("command", "")
        for h in entry.get("hooks", [])
        if isinstance(h, dict)
    )


def merge(settings: dict, hook_block: dict) -> dict:
    """hooks.Stop listesine AIOS girdisini ekle; diğer her şeye dokunma."""
    result = json.loads(json.dumps(settings))  # derin kopya
    hooks = result.setdefault("hooks", {})
    for event, entries in hook_block.items():
        existing = hooks.setdefault(event, [])
        # Aynı kapı iki kez kurulmasın
        existing[:] = [e for e in existing if not is_aios_hook(e)]
        existing.extend(entries)
    return result


def remove(settings: dict) -> dict:
    result = json.loads(json.dumps(settings))
    hooks = result.get("hooks", {})
    for event in list(hooks):
        hooks[event] = [e for e in hooks[event] if not is_aios_hook(e)]
        if not hooks[event]:
            del hooks[event]
    if not hooks:
        result.pop("hooks", None)
    return result


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    uninstall = "--uninstall" in sys.argv

    gate = AIOS_DIR / "hooks" / "gate.py"
    if not gate.exists():
        print(f"HATA: {gate} bulunamadı. Önce dosyaları yerleştir.")
        return 1

    current = load_json(TARGET)
    if uninstall:
        updated, action = remove(current), "kaldırılacak"
    else:
        hook_block = {k: v for k, v in load_json(HOOK_SRC).items() if not k.startswith("_")}
        updated = merge(current, hook_block["hooks"])
        action = "kurulacak"

    print(f"Hedef   : {TARGET}")
    print(f"Mevcut  : {len(current)} anahtar -> {', '.join(current) or '(boş)'}")
    print(f"Sonra   : {len(updated)} anahtar -> {', '.join(updated)}")
    print(f"Kapı    : {action}\n")

    if dry_run:
        print(json.dumps(updated, indent=2, ensure_ascii=False))
        print("\n--dry-run: hiçbir şey yazılmadı.")
        return 0

    if TARGET.exists():
        backup = TARGET.with_suffix(f".json.bak-{datetime.now():%Y%m%d-%H%M%S}")
        shutil.copy2(TARGET, backup)
        print(f"Yedek   : {backup.name}")

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Tamam. Claude Code'u yeniden başlat.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
