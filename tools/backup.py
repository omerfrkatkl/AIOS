#!/usr/bin/env python3
"""
Local-layer backup (G42 / hybrid privacy): the personal brain files have NO git
copy, so this tool zips them on demand and keeps the last KEEP archives.

Usage:
  uv run --no-project python tools/backup.py             # zip PROFILE+LEDGER
  uv run --no-project python tools/backup.py --restore backups/aios-local-XXXX.zip
"""

import argparse
import sys
import zipfile
from datetime import datetime
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AIOS_DIR / "tools"))
from aioslog import log_event, user_error  # noqa: E402

BACKUP_DIR = AIOS_DIR / "backups"
LOCAL_FILES = ["PROFILE.md", "LEDGER.md"]
VAULT_DIR = AIOS_DIR / "vault"
KEEP = 5


def backup() -> int:
    missing = [f for f in LOCAL_FILES if not (AIOS_DIR / f).exists()]
    if missing:
        user_error("Yedeklenecek dosya eksik", f"bulunamayan: {', '.join(missing)}",
                   "Önce F3 beyin dosyalarının var olduğunu doğrula")
        return 1
    BACKUP_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = BACKUP_DIR / f"aios-local-{stamp}.zip"
    vault_files = [p for p in VAULT_DIR.rglob("*") if p.is_file()] if VAULT_DIR.exists() else []
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for f in LOCAL_FILES:
            z.write(AIOS_DIR / f, f)
        for p in vault_files:
            z.write(p, p.relative_to(AIOS_DIR))
    archives = sorted(BACKUP_DIR.glob("aios-local-*.zip"))
    for old in archives[:-KEEP]:
        old.unlink()
    log_event("backup", "CREATED", "info", target.name,
              files=len(LOCAL_FILES) + len(vault_files))
    print(f"Yedek: {target.relative_to(AIOS_DIR)} "
          f"({len(LOCAL_FILES) + len(vault_files)} dosya · {target.stat().st_size:,} bayt) · "
          f"arşivde {min(len(archives), KEEP)} kopya")
    return 0


def restore(zip_path: str) -> int:
    zp = Path(zip_path)
    if not zp.exists():
        user_error(f"{zp} bulunamadı", "Yedek dosyası yok",
                   "backups/ klasörünü listele: dir backups")
        return 1
    with zipfile.ZipFile(zp) as z:
        for f in LOCAL_FILES:
            if f in z.namelist():
                z.extract(f, AIOS_DIR)
                print(f"geri geldi: {f}")
    log_event("backup", "RESTORED", "info", zp.name)
    print("Yerel katman geri yüklendi.")
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    p = argparse.ArgumentParser(description="Local-layer backup (G42)")
    p.add_argument("--restore", metavar="ZIP")
    a = p.parse_args()
    if a.restore:
        return restore(a.restore)
    return backup()


if __name__ == "__main__":
    sys.exit(main())
