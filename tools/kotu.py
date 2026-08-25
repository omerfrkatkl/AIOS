#!/usr/bin/env python3
"""
kotu.py (F12c): kanal-basina kullanim defteri + yenileme pencere modeli (G46).

Kural: TUKENMIS kanala yonlendirme YAPILMAZ — registry route dolu kanallari eler.

Kart semasi eki (opsiyonel alan):
  "kota_model": {"miktar": 100, "birim": "istek",
                 "pencere": {"tur": "aylik", "baslangic-gunu": 1}}
Kota modeli olmayan kart "tanimsiz" sayilir — engellemez, yalniz raporlar.

Kullanim girisi: SAHIP sohbette kullanim belirtince AJAN bu araci kosar
(sahibin arayuzu sohbet, CLI ajanin aracidir).

Alt-komutlar:
  kayit <kanal> <miktar> [--birim istek|token|TL] [--not "..."]
        Kullanim girdisi ekler (registry/usage.jsonl).
  durum  Kanal basina: pencere sinirlari + pencere-ici kullanim + durum
        (saglikli <80 · uyari >=80 · DOLU >=100 · tanimsiz).
  gorev-kur [--kos]
        Task Scheduler komutlarini uretir (kesif poll gunde bir).
        --kos ILE SISTEME GOREV YAZILIR — devreye alma sahibin onayina tabidir.

Pencere matematiği saf fonksiyonlardadır: window_bounds(bugun, gun) ve
status_for(yuzde) test edilir.
"""

import argparse
import json
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
USAGE = AIOS_DIR / "registry" / "usage.jsonl"
CARDS = AIOS_DIR / "registry" / "cards"
TASK_NAME = "AIOS-kesif-poll"

sys.path.insert(0, str(AIOS_DIR / "tools"))


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def load_card(card_id: str) -> dict | None:
    for p in sorted(CARDS.glob("*.json")):
        if p.name.startswith("_"):
            continue
        try:
            c = json.loads(p.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            continue
        if c.get("id") == card_id:
            return c
    return None


def _month_add(y: int, m: int, delta: int) -> tuple[int, int]:
    t = y * 12 + (m - 1) + delta
    return t // 12, t % 12 + 1


def _safe_day(y: int, m: int, day: int) -> date:
    """O ayda 'day' yoksa (orn. 31 Subat'ta) ayin son gunu."""
    ny, nm = _month_add(y, m, 1)
    last = (date(ny, nm, 1) - __import__("datetime").timedelta(days=1)).day
    return date(y, m, min(day, last))


def window_bounds(today: date, start_day: int) -> tuple[date, date]:
    """Aylik pencere: bugune en yakin gecmis 'start_day' -> sonraki 'start_day' - 1.
    Gun o ayda yoksa (31/Subat) ayin son gununa kestirilir (clamp).
    Saf fonksiyon."""
    td = __import__("datetime").timedelta(days=1)
    if today.day >= start_day:
        start = _safe_day(today.year, today.month, start_day)
    else:
        py, pm = _month_add(today.year, today.month, -1)
        start = _safe_day(py, pm, start_day)
    ny, nm = _month_add(start.year, start.month, 1)
    next_start = _safe_day(ny, nm, start_day)
    return start, next_start - td


def status_for(pct: float | None) -> str:
    """Saf: yuzde -> durum etiketi."""
    if pct is None:
        return "tanimsiz"
    if pct >= 100:
        return "DOLU"
    if pct >= 80:
        return "uyari"
    return "saglikli"


def cmd_kayit(args) -> int:
    card = load_card(args.kanal)
    row = {"ts": now_iso(), "kanal": args.kanal,
           "miktar": args.miktar, "birim": args.birim, "not": args.not_ or ""}
    if card is None:
        print(f"UYARI: '{args.kanal}' diye kart yok — kayit yine de yazildi.", file=sys.stderr)
    append_jsonl(USAGE, row)
    print(f"kullanim kaydi: {args.kanal} +{args.miktar} {args.birim}")
    return 0


def cmd_durum(_) -> int:
    cards = []
    for p in sorted(CARDS.glob("*.json")):
        if p.name.startswith("_"):
            continue
        try:
            cards.append(json.loads(p.read_text(encoding="utf-8-sig")))
        except json.JSONDecodeError:
            pass
    entries = read_jsonl(USAGE)
    today = date.today()
    any_dolu = False
    for c in cards:
        cid = c.get("id", "?")
        km = c.get("kota_model")
        if not km:
            print(f"{cid:24} tanimsiz (kota_model yok — envanter oturumu bekliyor)")
            continue
        miktar = float(km.get("miktar", 0))
        pencere = km.get("pencere", {})
        gun = int(pencere.get("baslangic-gunu", 1))
        start, end = window_bounds(today, gun)
        used = sum(float(e.get("miktar", 0)) for e in entries
                   if e.get("kanal") == cid and e.get("birim") == km.get("birim", "istek")
                   and start.isoformat() <= str(e.get("ts", ""))[:10] <= end.isoformat())
        pct = round(100 * used / miktar, 1) if miktar else None
        st = status_for(pct)
        flag = " <-- YONLENDIRME DIŞI (G46)" if st == "DOLU" else ""
        if st == "DOLU":
            any_dolu = True
        print(f"{cid:24} {st:9} {used:g}/{miktar:g} {km.get('birim','istek')} "
              f"(%{pct}) pencere {start}..{end}{flag}")
    if not cards:
        print("kart yok")
    return 1 if any_dolu else 0


BAT_PATH = AIOS_DIR / "tools" / "_zamanli.bat"


def build_bat() -> str:
    lines = ["@echo off",
             f"cd /d {AIOS_DIR}",
             "uv run --no-project python tools\\kesif.py poll >> logs\\kesif-zamanli.log 2>&1"]
    BAT_PATH.write_text("\r\n".join(lines), encoding="utf-8")
    return str(BAT_PATH)


def cmd_gorev(args) -> int:
    bat = build_bat()
    cmd = f'schtasks /Create /TN "{TASK_NAME}" /TR "{bat}" /SC DAILY /ST 09:15 /F'
    print("Task Scheduler komutu:")
    print(f"  {cmd}")
    print("(gunde bir 09:15 UTC yerel saatte kesif poll; log: logs/kesif-zamanli.log)")
    if args.kos:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip())
        print("GOREV KAYDEDILDI — silmek icin: schtasks /Delete /TN "
              f"\"{TASK_NAME}\" /F")
        return r.returncode
    print("--kos verilmedi: sisteme yazilmadi (devreye alma sahibin onayina tabi).")
    return 0


def parse_openrouter_key(payload: dict) -> dict:
    """R-004: GET /api/v1/key cevabindan kota-bilinci cikarimi (saf fonksiyon).
    NOT: OpenRouter istek-sayisi vermez; gunluk kapak is_free_tier'den belirlenir
    (ucretsiz=50/gun; hic $10+ kredi alindiysa 1000/gun). Istek sayaci usage.jsonl'dir."""
    d = payload.get("data", {})
    free = bool(d.get("is_free_tier"))
    return {
        "is_free_tier": free,
        "gunluk_kapak_istek": 50 if free else 1000,
        "kullanim_bugun_kredi": d.get("usage_daily"),
        "kalan_limit": d.get("limit_remaining"),
    }


def cmd_orkey(args) -> int:
    import os
    import urllib.request

    name = args.env_var
    key = os.environ.get(name)
    if not key:
        print(f"HATA: {name} ortam-degiskeni yok — anahtari once tanimla.",
              file=sys.stderr)
        return 1
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/key",
        headers={"Authorization": f"Bearer {key}", "User-Agent": "AIOS-kotu/1"})
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as r:
            payload = json.loads(r.read().decode("utf-8"))
    except Exception as exc:
        print(f"HATA: sorgu basarisiz: {exc}", file=sys.stderr)
        return 1
    b = parse_openrouter_key(payload)
    print(f"OPENROUTER KOTA (gerçek okuma)")
    print(f"  hesap türü      : {'ücretsiz' if b['is_free_tier'] else 'kredili'}")
    print(f"  günlük kapak    : {b['gunluk_kapak_istek']} istek/gün (:free modeller)")
    print(f"  bugün kredi     : {b['kullanim_bugun_kredi']}")
    print(f"  anahtar limiti  : {b['kalan_limit'] if b['kalan_limit'] is not None else 'sınırsız'}")
    print("  NOT: API istek-sayısı vermez → gerçek istek sayacı usage.jsonl (kotu kayit).")
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="F12c kota takipçisi (G46)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    k = sub.add_parser("kayit")
    k.add_argument("kanal")
    k.add_argument("miktar", type=float)
    k.add_argument("--birim", default="istek", choices=("istek", "token", "TL"))
    k.add_argument("--not", dest="not_", default="")

    sub.add_parser("durum")

    g = sub.add_parser("gorev-kur")
    g.add_argument("--kos", action="store_true",
                   help="sisteme gorev yazar (SAHIBIN ONAYIYLA kosulur)")

    o = sub.add_parser("openrouter-kota")
    o.add_argument("--env-var", default="OPENROUTER_API_KEY",
                   help="anahtarın ortam-değişkeni adı")
    o.add_argument("--timeout", type=int, default=15)

    a = ap.parse_args()
    return {"kayit": cmd_kayit, "durum": cmd_durum, "gorev-kur": cmd_gorev,
            "openrouter-kota": cmd_orkey}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
