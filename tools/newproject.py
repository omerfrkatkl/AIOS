#!/usr/bin/env python3
"""
New-project ritual (F8): one command -> managed project scaffold.

Creates (or --augment adds to an existing folder):
  BRIEF.md   four-field skeleton (owner fills the vision)
  git init + first commit
  LICENSE    MIT (copied from AIOS)
  README.md  name + placeholder
  CHANGELOG  Keep-a-Changelog skeleton
  STATE.md   four-field skeleton
  .aios      gate opt-in marker (scope filter reads this)

Usage:
  uv run --no-project python tools/newproject.py <name>              # create Projects/<name>
  uv run --no-project python tools/newproject.py <name> --augment    # fill gaps in existing folder
"""

import argparse
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
PROJECTS = AIOS_DIR.parent
sys.path.insert(0, str(AIOS_DIR / "tools"))
from aioslog import log_event, user_error  # noqa: E402

BRIEF = """# BRIEF — {name}

| | |
|---|---|
| **Amaç** | Projenin ne olduğunu ve ne olmadığını tek yerde tutmak |
| **Yaşam döngüsü** | Yerinde güncellenir; vizyon değişmedikçe dokunulmaz. Plan burada tutulmaz |
| **Sahip** | Proje sahibi |
| **Okuma tetikleyicisi** | Her oturum açılışı |

## Ne isteniyor

(Sahip buraya vizyonu yazar — ne, neden; nasıl DEĞİL.)

## Kapsam dışı

-
"""

STATE_SKEL = """# STATE — {name}

| | |
|---|---|
| **Amaç** | Şu an neyin doğru olduğunu tek yerde tutmak |
| **Yaşam döngüsü** | Yerinde yeniden yazılır; eskiyen satır silinir |
| **Sahip** | Proje sahibi; Claude yazar, sahip diff'i onaylar |
| **Okuma tetikleyicisi** | Her oturum açılışı |
| **Son güncelleme** | {today} |

## Durum

- Proje ritüelle açıldı ({today}); ilk dilim belirlenmedi.

## Sıradaki

1. İlk dilimi tanımla (yanlışlanabilir testiyle)

## Açık riskler

| Risk | Erken sinyal |
|---|---|
"""


def write_if_missing(root: Path, rel: str, content: str) -> str:
    target = root / rel
    if target.exists():
        return f"  = var, dokunulmadı: {rel}"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"  + yazıldı: {rel}"


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    p = argparse.ArgumentParser(description="Managed project ritual")
    p.add_argument("name")
    p.add_argument("--augment", action="store_true",
                   help="mevcut klasördeki eksikleri tamamla (var olanlara dokunma)")
    a = p.parse_args()

    root = PROJECTS / a.name
    if not root.exists() and a.augment:
        user_error(f"{root} bulunamadı", "--augment mevcut klasör ister",
                   f"Yeni proje için: tools/newproject.py {a.name} (--augment olmadan)")
        return 1

    today = date.today().isoformat()
    actions = []
    if not root.exists():
        root.mkdir(parents=True)
        actions.append(f"  + klasör: {root}")
    elif not a.augment:
        user_error(f"{root} zaten var", "üstüne yazma riski",
                   "--augment kullan veya farklı isim seç")
        return 1

    actions.append(write_if_missing(root, "BRIEF.md", BRIEF.format(name=a.name)))
    actions.append(write_if_missing(root, "STATE.md", STATE_SKEL.format(name=a.name, today=today)))
    actions.append(write_if_missing(root, "README.md",
                                    f"# {a.name}\n\n(AIOS ile geliştirilen yönetilen proje.)\n"))
    actions.append(write_if_missing(root, "CHANGELOG.md",
                                    f"# Changelog\n\n## [0.1.0] — {today}\n- Proje iskeleti (AIOS ritüeli).\n"))
    lic = AIOS_DIR / "LICENSE"
    if lic.exists():
        actions.append(write_if_missing(root, "LICENSE", lic.read_text(encoding="utf-8")))
    actions.append(write_if_missing(root, ".aios",
                                    f"AIOS managed project — gate opt-in ({today})\n"))

    if not (root / ".git").exists():
        code = subprocess.run(["git", "init"], cwd=root, capture_output=True, text=True)
        actions.append("  + git init" if code.returncode == 0 else f"  ! git init hatası: {code.stderr}")

    for line in actions:
        print(line)
    subprocess.run(["git", "add", "-A"], cwd=root, capture_output=True)
    subprocess.run(["git", "commit", "-m", "ritüel iskeleti (AIOS newproject)"],
                   cwd=root, capture_output=True)
    log_event("ritual", "RUN", "info", a.name, augment=a.augment)
    print(f"\nRitüel tamam: {root}")
    print("Sonraki adım: BRIEF.md'ye vizyonu yaz, ilk dilimi STATE'e işle.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
