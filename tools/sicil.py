"""F12d kanal sicili v1 — kanal x gorev basari kaydi (empirik zekanin ham verisi).

Dort alan: Amaç kanal/gorev basari verisini biriktirmek · Yaşam döngüsü append-only
JSONL (registry/sicil.jsonl, yerel bölge) · Sahip: kayitlari AJAN sohbetten yazar,
sahip dogrular · Okuma tetikleyici: 'ozet' komutu + F12d tahminci/arena.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
SICIL = AIOS_DIR / "registry" / "sicil.jsonl"
GOREVLER = {"kod", "arastirma", "metin", "ozet"}
SONUCLAR = {"basari", "kismi", "hata"}
MIN_N = 5  # bu altindaki oran istatistik olarak sunulmaz


def _load() -> list[dict]:
    if not SICIL.exists():
        return []
    out = []
    for line in SICIL.read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def cmd_ekle(args) -> int:
    if args.gorev not in GOREVLER:
        print(f"HATA: gorev {args.gorev!r} disinda ({sorted(GOREVLER)})", file=sys.stderr)
        return 2
    if args.sonuc not in SONUCLAR:
        print(f"HATA: sonuc {args.sonuc!r} disinda ({sorted(SONUCLAR)})", file=sys.stderr)
        return 2
    row = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "kanal": args.kanal,
        "gorev": args.gorev,
        "sonuc": args.sonuc,
        "sure_saniye": args.sure,
        "not": args.not_ or "",
        "etiket": "TEST" if args.test else "gercek",
        "kaynak": args.kaynak,
    }
    SICIL.parent.mkdir(parents=True, exist_ok=True)
    with SICIL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    tag = " [TEST]" if args.test else ""
    print(f"kayit: {args.kanal} x {args.gorev} -> {args.sonuc}{tag}")
    return 0


def _pivot(rows: list[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for r in rows:
        ch = out.setdefault(r["kanal"], {"toplam": 0, "basari": 0, "gorevler": {}})
        ch["toplam"] += 1
        if r["sonuc"] == "basari":
            ch["basari"] += 1
        g = ch["gorevler"].setdefault(r["gorev"], {"n": 0, "basari": 0})
        g["n"] += 1
        if r["sonuc"] == "basari":
            g["basari"] += 1
    return out


def cmd_ozet(args) -> int:
    rows = _load()
    rows = [r for r in rows if (r.get("etiket") == "TEST") == bool(getattr(args, "test", False))]
    if not rows:
        print("sicil bos — hic kayit yok.")
        return 0
    pivot = _pivot(rows)
    if getattr(args, "json", False):
        import json as _json

        payload = {}
        for kanal, ch in pivot.items():
            oran = (ch["basari"] / ch["toplam"]) if ch["toplam"] >= MIN_N else None
            payload[kanal] = {"toplam": ch["toplam"], "basari_orani": oran,
                              "yeterli_veri": ch["toplam"] >= MIN_N,
                              "gorevler": ch["gorevler"]}
        print(_json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(f"SICIL ÖZETİ ({len(rows)} kayıt, eşik n={MIN_N})")
    for kanal in sorted(pivot):
        ch = pivot[kanal]
        if ch["toplam"] >= MIN_N:
            oran = f"%{round(100 * ch['basari'] / ch['toplam'])}"
            guven = ""
        else:
            oran = "?"
            guven = " (yetersiz veri)"
        detay = ", ".join(f"{g}:{v['basari']}/{v['n']}" for g, v in sorted(ch["gorevler"].items()))
        print(f"  {kanal:<20} başarı {oran}{guven} · [{detay}]")
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="F12d kanal sicili v1")
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("ekle")
    e.add_argument("--kanal", required=True)
    e.add_argument("--gorev", required=True)
    e.add_argument("--sonuc", required=True)
    e.add_argument("--sure", type=int, default=None, help="saniye")
    e.add_argument("--not", dest="not_", default="")
    e.add_argument("--kaynak", default="sahip-beyani", choices=["sahip-beyani", "otomatik"])
    e.add_argument("--test", action="store_true",
                   help="TEST-etiketli kayıt (kişisel-veri dondurması uyumlu)")
    o = sub.add_parser("ozet")
    o.add_argument("--json", action="store_true")
    o.add_argument("--test", action="store_true", help="yalnız TEST-etiketli kayıtlar")
    a = ap.parse_args()
    return {"ekle": cmd_ekle, "ozet": cmd_ozet}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
