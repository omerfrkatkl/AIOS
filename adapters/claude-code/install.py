#!/usr/bin/env python3
"""
Installs the AIOS gate adapter for Claude Code.

What it does : merges adapters/claude-code/hook.json into ~/.claude/settings.json.
What it avoids: overwriting any existing key. Everything else is preserved.

Usage:
  uv run --no-project python adapters/claude-code/install.py            # install
  uv run --no-project python adapters/claude-code/install.py --dry-run  # show only
  uv run --no-project python adapters/claude-code/install.py --uninstall # remove gate
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

ADAPTER_DIR = Path(__file__).resolve().parent
AIOS_DIR = ADAPTER_DIR.parents[1]
sys.path.insert(0, str(AIOS_DIR / "tools"))
from aioslog import log_event, user_error  # noqa: E402

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
    """Add the AIOS entry under hooks.Stop; touch nothing else."""
    result = json.loads(json.dumps(settings))
    hooks = result.setdefault("hooks", {})
    for event, entries in hook_block.items():
        existing = hooks.setdefault(event, [])
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
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    dry_run = "--dry-run" in sys.argv
    uninstall = "--uninstall" in sys.argv

    gate = AIOS_DIR / "hooks" / "gate.py"
    if not gate.exists():
        user_error(f"{gate} bulunamadı", "Adaptör dosyaları eksik yerleştirilmiş",
                   "Depoyu tam çek: git pull, sonra install.py'yi yeniden koş")
        return 1

    try:
        current = load_json(TARGET)
    except Exception as exc:
        user_error(f"{TARGET} okunamadı", str(exc), "Dosyayı elle incele; bozuksa .bak-* yedeğinden dön")
        return 1

    if uninstall:
        updated, action = remove(current), "kaldırılacak"
    else:
        hook_block = {k: v for k, v in load_json(HOOK_SRC).items() if not k.startswith("_")}
        updated = merge(current, hook_block["hooks"])
        action = "kurulacak"

    print(f"Hedef   : {TARGET}")
    print(f"Mevcut  : {len(current)} anahtar -> {', '.join(current) or '(boş)'}")
    print(f"Sonra   : {len(updated)} anahtar -> {', '.join(updated) or '(boş)'}")
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
    log_event("install", "UNINSTALLED" if uninstall else "INSTALLED", "info",
              f"claude-code gate {action}", target=str(TARGET))
    print("Tamam. Aracı yeniden başlat.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
