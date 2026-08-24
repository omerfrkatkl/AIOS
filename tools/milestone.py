#!/usr/bin/env python3
"""
Brain milestones (F5): named snapshots of the brain via annotated git tags.

Usage:
  uv run --no-project python tools/milestone.py <name>    # create ms/<name>
  uv run --no-project python tools/milestone.py --list    # list milestones
"""

import subprocess
import sys
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AIOS_DIR / "tools"))
from aioslog import log_event, user_error  # noqa: E402


def git(*args: str) -> tuple[int, str]:
    r = subprocess.run(["git", *args], cwd=AIOS_DIR, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def create(name: str) -> int:
    safe = "".join(c for c in name if c.isalnum() or c in "-_").strip("-_")
    if not safe:
        user_error("Geçersiz isim", "yalnızca harf/rakam/-/_ kalmalı",
                   "örnek: uv run --no-project python tools/milestone.py pilot-öncesi")
        return 1
    code, out = git("rev-parse", "--is-inside-work-tree")
    if code != 0 or out.strip() != "true":
        user_error("git deposu bulunamadı", f"cwd={AIOS_DIR}",
                   "AIOS klasöründe koş")
        return 1
    tag = f"ms/{safe}"
    code, out = git("tag", "-a", tag, "-m", f"beyin kilometre taşı: {safe}")
    if code != 0:
        if "already exists" in out:
            user_error(f"{tag} zaten var", "aynı isimli kilometre taşı mevcut",
                       "farklı bir isim seç veya --list ile listele")
        else:
            user_error("tag oluşturulamadı", out.strip(), "git durumunu kontrol et")
        return 1
    log_event("milestone", "CREATED", "info", tag)
    print(f"Kilometre taşı: {tag}")
    print("Not: tag'ler yereldir; uzakta görünmesi için: git push origin " + tag)
    return 0


def listing() -> int:
    code, out = git("tag", "-l", "ms/*")
    tags = [t for t in out.splitlines() if t.strip()]
    if not tags:
        print("Henüz kilometre taşı yok.")
        return 0
    for t in tags:
        _, desc = git("tag", "-l", t, "-n1")
        print(desc.strip() or t)
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    args = [a for a in sys.argv[1:] if a != "--list"]
    if "--list" in sys.argv:
        return listing()
    if args:
        return create(" ".join(args))
    print("Kullanım: uv run --no-project python tools/milestone.py <isim> | --list")
    return 1


if __name__ == "__main__":
    sys.exit(main())
