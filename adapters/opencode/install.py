#!/usr/bin/env python3
"""
Installs the AIOS gate plugin for opencode (v1 - detection only).

Merges the plugin entry into ~/.config/opencode/opencode.json(.c). Backup is
taken before write. Idempotent: a second run adds nothing.

Usage:
  uv run --no-project python adapters/opencode/install.py             # install
  uv run --no-project python adapters/opencode/install.py --dry-run   # show only
  uv run --no-project python adapters/opencode/install.py --uninstall # remove
"""

import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

ADAPTER_DIR = Path(__file__).resolve().parent
AIOS_DIR = ADAPTER_DIR.parents[1]
sys.path.insert(0, str(AIOS_DIR / "tools"))
from aioslog import log_event, user_error  # noqa: E402

PLUGIN = ADAPTER_DIR / "gate-plugin.js"
TARGETS = [Path.home() / ".config" / "opencode" / "opencode.json",
           Path.home() / ".config" / "opencode" / "opencode.jsonc"]
ENTRY = "file:///" + str(PLUGIN).replace("\\", "/")


def find_target() -> Path | None:
    for t in TARGETS:
        if t.exists():
            return t
    return TARGETS[0]  # default: create .json


def load_jsonc(path: Path) -> dict:
    """Tolerant JSONC load: line/block comments and trailing commas stripped.
    The owner's file is .jsonc; opencode itself accepts these relaxations."""
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return {}
    out, i, in_str = [], 0, False
    while i < len(text):
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < len(text):
                out.append(text[i + 1]); i += 2; continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True; out.append(c); i += 1; continue
        if c == "/" and i + 1 < len(text) and text[i + 1] == "/":
            while i < len(text) and text[i] != "\n":
                i += 1
            continue
        if c == "/" and i + 1 < len(text) and text[i + 1] == "*":
            i += 2
            while i + 1 < len(text) and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        out.append(c); i += 1
    cleaned = re.sub(r",\s*([}\]])", r"\1", "".join(out))
    return json.loads(cleaned)


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    dry_run = "--dry-run" in sys.argv
    uninstall = "--uninstall" in sys.argv

    if not PLUGIN.exists():
        user_error(f"{PLUGIN} bulunamadı", "Adaptör dosyası eksik",
                   "git pull ile depoyu tazele, install.py'yi yeniden koş")
        return 1

    target = find_target()
    try:
        current = load_jsonc(target) if target.exists() else {}
    except Exception as exc:
        user_error(f"{target} ayrıştırılamadı", str(exc),
                   "Dosyada yorum satırları varsa elle ekle: "
                   f'"plugin": ["{ENTRY}"]')
        return 1

    plugins = list(current.get("plugin", []))
    before = len(plugins)
    if uninstall:
        plugins = [p for p in plugins if ENTRY not in str(p)]
        action = "kaldırılacak"
    else:
        if not any(ENTRY in str(p) for p in plugins):
            plugins.append(ENTRY)
        action = "kurulacak"
    updated = dict(current)
    if plugins:
        updated["plugin"] = plugins
    else:
        updated.pop("plugin", None)
    changed = plugins != current.get("plugin", []) or (uninstall and "plugin" in current)

    print(f"Hedef    : {target}")
    print(f"Eklenti  : {ENTRY}")
    print(f"İşlem    : {action} (değişiklik: {changed})\n")

    if dry_run:
        print(json.dumps(updated, indent=2, ensure_ascii=False))
        print("\n--dry-run: hiçbir şey yazılmadı.")
        return 0

    if not changed:
        print("Zaten istenen durumda - yazılmadı.")
        return 0

    if target.exists():
        backup = target.with_suffix(f".bak-{datetime.now():%Y%m%d-%H%M%S}")
        shutil.copy2(target, backup)
        print(f"Yedek    : {backup.name}")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log_event("install", "UNINSTALLED" if uninstall else "INSTALLED", "info",
              f"opencode gate plugin {action}", target=str(target))
    print("Tamam. opencode'u yeniden başlat.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
