#!/usr/bin/env python3
"""Learning audit (G50): diff PROFILE.md/LEDGER.md against the newest
backups/aios-local-*.zip so wrong learning can be corrected (unlearning).
Keep = do nothing; fix/delete = edit the file or tell the agent.
The next backup becomes the new baseline."""

import difflib
import sys
import zipfile
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AIOS_DIR / "tools"))
from aioslog import log_event, user_error  # noqa: E402

BACKUP_DIR = AIOS_DIR / "backups"
FILES = ["PROFILE.md", "LEDGER.md"]


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    archives = sorted(BACKUP_DIR.glob("aios-local-*.zip"))
    if not archives:
        user_error("Yedek bulunamadı", "backups/ boş", "Önce: tools/backup.py")
        return 1
    newest = archives[-1]
    added = removed = 0
    with zipfile.ZipFile(newest) as z:
        for name in FILES:
            old = z.read(name).decode("utf-8").splitlines() if name in z.namelist() else []
            new = (AIOS_DIR / name).read_text(encoding="utf-8").splitlines()
            diff = [l for l in difflib.unified_diff(old, new, lineterm="", n=0)
                    if l[:1] in "+-" and l[:3] not in ("+++", "---")]
            if not diff:
                continue
            print(f"--- {name} (taban: {newest.name})")
            for l in diff:
                print(("  ÖĞRENİLDİ  " if l[0] == "+" else "  KALDIRILDI") + " " + l[1:].strip()[:100])
                added, removed = added + (l[0] == "+"), removed + (l[0] == "-")
    if added or removed:
        print(f"\nToplam: {added} yeni öğrenme, {removed} kaldırma.")
        print("Yanlış olanı söyle → düzeltirim; onaylıyorsan hiçbir şey yapma (sonraki backup taban olur).")
    else:
        print(f"Yeni öğrenme yok (taban: {newest.name}).")
    log_event("audit", "RUN", "info", f"added={added} removed={removed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
