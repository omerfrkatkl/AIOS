#!/usr/bin/env python3
"""
registry.py (F12a): Kanal Sozlesmesi kayit defteri + yonlendirici v1.

Kart = Kanal Sozlesmesi (G47): tur/parametre/girdi/limit/yetenek/enforcement/
dosya-erisimi bildirir; yonlendirici ve dogrulama bu kartlardan cizer (G11).
Envanter YEREL bolgededir (G10): registry/ git'e girmez.

Kart semasi (registry/cards/*.json):
  id            str   benzersiz
  kanal         cli|api|web|yerel
  saglayici     str
  model         str
  gizlilik      bulut|yerel|hibrit        (gizlilik bolgesi)
  yetenekler    [str] bos olamaz           (kod, arastirma, metin, gorsel...)
  limitler      {kota,hiz,not} opsiyonel
  maliyet       str
  enforcement   str    kapinin bu kanaldaki durumu (G47)
  dosya_erisimi str    okuma-yazma kapsami (G47)
  durum         aktif|pasif
  dogrulanma    YYYY-MM-DD  son dogrulanma tarihi (G10)
  kanit         str    R-id veya gozlem notu — PROVENSANS ZORUNLU (G51)

Alt-komutlar:
  init                       registry/ iskeleti + ornek kart
  validate                   tum kartlari semaya gore denetler
  list                       kart tablosu
  route --task "..."         gorev -> kanal onerisi + GEREKCE (G11)
  update <id>                sozlu-bildirim akisi icin isaret (ajan doldurur)
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
REGISTRY = AIOS_DIR / "registry"
CARDS = REGISTRY / "cards"

REQUIRED = ("id", "kanal", "saglayici", "model", "gizlilik", "yetenekler",
            "durum", "dogrulanma", "kanit")
ENUMS = {"kanal": {"cli", "api", "web", "yerel"},
         "gizlilik": {"bulut", "yerel", "hibrit"},
         "durum": {"aktif", "pasif"}}

# route v1: yetenek -> ipucu sozcukler (deterministik, G11 gerekceli)
HINTS = {
    "kod": ["kod", "refactor", "debug", "agent"],
    "arastirma": ["arastir", "benchmark", "karsilastir", "web"],
    "metin": ["yaz", "duzenle", "cevir", "ozet"],
}

EXAMPLE_CARD = {
    "id": "ORNEK-kanal",
    "kanal": "api",
    "saglayici": "Ornek Saglayici",
    "model": "ornek-model-v1",
    "gizlilik": "bulut",
    "yetenekler": ["kod", "metin"],
    "limitler": {"kota": "belirsiz", "hiz": "-", "not": "envanter oturumunda doldurulur"},
    "maliyet": "-",
    "enforcement": "kapi bu kanalda tetiklenmiyor - not dusuldu",
    "dosya_erisimi": "yalniz proje dizini",
    "durum": "pasif",
    "dogrulanma": "2026-01-01",
    "kanit": "R-000 veya 'gozlem 2026-AA-GG'",
}


def _fail(msg: str) -> int:
    print(f"HATA: {msg}", file=sys.stderr)
    return 1


def load_cards() -> list[dict]:
    if not CARDS.exists():
        return []
    out = []
    for p in sorted(CARDS.glob("*.json")):
        if p.name.startswith("_"):
            continue  # şema örneği gerçek kart değildir
        try:
            out.append(json.loads(p.read_text(encoding="utf-8-sig")))  # utf-8-sig: Windows BOM toleransı
        except json.JSONDecodeError as e:
            print(f"UYARI: {p.name} JSON bozuk: {e}", file=sys.stderr)
    return out


def cmd_init(_) -> int:
    CARDS.mkdir(parents=True, exist_ok=True)
    ex = CARDS / "_ornek.json"
    if not ex.exists():
        ex.write_text(json.dumps(EXAMPLE_CARD, ensure_ascii=False, indent=2), encoding="utf-8")
    gi = AIOS_DIR / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.exists() else ""
    if "registry/" not in text:
        gi.write_text(text.rstrip() + "\n\n# --- Envanter (yerel katman, G10) ---\nregistry/\n",
                      encoding="utf-8")
        print(".gitignore'a registry/ eklendi (yerel bolge)")
    print(f"Registry hazir: {CARDS} (_ornek.json sema ornegi)")
    return 0


def validate_card(card: dict, seen_ids: set) -> list[str]:
    errs = []
    cid = card.get("id", "<id-yok>")
    for key in REQUIRED:
        if key not in card or card[key] in ("", None, []):
            errs.append(f"{cid}: zorunlu alan bos: {key}")
    for field, allowed in ENUMS.items():
        if field in card and card[field] not in allowed:
            errs.append(f"{cid}: {field}={card[field]!r} disinda ({sorted(allowed)})")
    if "dogrulanma" in card and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(card["dogrulanma"])):
        errs.append(f"{cid}: dogrulanma YYYY-MM-DD degil: {card['dogrulanma']}")
    elif "dogrulanma" in card and str(card["dogrulanma"]) > date.today().isoformat():
        errs.append(f"{cid}: dogrulanma gelecekte olamaz: {card['dogrulanma']}")
    if "yetenekler" in card and (not isinstance(card["yetenekler"], list) or not card["yetenekler"]):
        errs.append(f"{cid}: yetenekler bos liste olamaz (G47)")
    if cid != "<id-yok>":
        if cid in seen_ids:
            errs.append(f"{cid}: id tekrari")
        seen_ids.add(cid)
    return errs


def cmd_validate(_) -> int:
    cards = load_cards()
    real = [c for c in cards if not c.get("id", "").startswith("_")]
    seen: set = set()
    all_errs: list[str] = []
    for c in real:
        all_errs.extend(validate_card(c, seen))
    if not real:
        return _fail("kart yok — once 'init', sonra envanter oturumu")
    if all_errs:
        for e in all_errs:
            print(f"[HATA] {e}")
        print(f"\nvalidate: {len(real)} kart, {len(all_errs)} hata")
        return 2
    print(f"validate: {len(real)} kart TEMIZ (sema + provensans + tarih)")
    return 0


def cmd_list(_) -> int:
    cards = [c for c in load_cards() if not c.get("id", "").startswith("_")]
    if not cards:
        return _fail("kart yok")
    for c in cards:
        caps = ",".join(c.get("yetenekler", []))
        print(f"{c['id']:22} {c.get('kanal','?'):6} {c.get('gizlilik','?'):7} "
              f"{c.get('durum','?'):6} dogr:{c.get('dogrulanma','?')} [{caps}]")
    return 0


def dolu_kanallar() -> set[str]:
    """G46: kotasını dolduran kanallar yönlendirmeye girmez.
    Pencere matematiği tek gerçek kaynaktan alınır (kotu.window_bounds)."""
    usage_p = AIOS_DIR / "registry" / "usage.jsonl"
    if not usage_p.exists():
        return set()
    try:
        entries = [json.loads(l) for l in usage_p.read_text(encoding="utf-8-sig").splitlines()
                   if l.strip()]
    except json.JSONDecodeError:
        return set()
    from kotu import window_bounds  # tek gerçek kaynak
    out = set()
    today = date.today()
    for c in load_cards():
        km = c.get("kota_model")
        if not km:
            continue
        cid = c.get("id", "")
        gun = int(km.get("pencere", {}).get("baslangic-gunu", 1))
        start, end = window_bounds(today, gun)
        used = sum(float(e.get("miktar", 0)) for e in entries
                   if e.get("kanal") == cid and e.get("birim") == km.get("birim", "istek")
                   and start.isoformat() <= str(e.get("ts", ""))[:10] <= end.isoformat())
        miktar = float(km.get("miktar", 0))
        if miktar and used >= miktar:
            out.add(cid)
    return out


def cmd_route(args) -> int:
    task = args.task.lower()
    needed = set()
    for cap, words in HINTS.items():
        if any(w in task for w in words):
            needed.add(cap)
    if args.gizli:
        needed.add("__gizli__")
    if not needed:
        return _fail(f"gorevden yetenek cikaramadim: {args.task!r} (bilinen ipuclari: "
                     f"{sorted({w for ws in HINTS.values() for w in ws})})")
    gizli = "__gizli__" in needed
    needed.discard("__gizli__")

    cards = [c for c in load_cards()
             if c.get("durum") == "aktif" and not c.get("id", "").startswith("_")]
    dolu = dolu_kanallar()
    atlanan = []
    if dolu:
        aktifler = {c.get("id") for c in cards}
        atlanan = sorted(dolu & aktifler)
        cards = [c for c in cards if c.get("id") not in dolu]
    hits = []
    for c in cards:
        matched = needed & set(c.get("yetenekler", []))
        if not matched:
            continue
        if gizli and c.get("gizlilik") == "bulut":
            continue
        hits.append((c, matched))
    if not hits:
        print(f"Oneri YOK: {'gizlilik filtresiyle ' if gizli else ''}uygun aktif kanal yok "
              f"(gereken: {sorted(needed)}). G13 notu: eksik yetenek arac-takviyesi ile kapatilabilir.")
        return 1
    hits.sort(key=lambda x: (-len(x[1]), x[0].get("gizlilik") == "yerel"))
    best, best_matched = hits[0]
    print(f"ONERI: {best['id']} ({best['saglayici']} · {best['model']})")
    print(f"GEREKCE: yetenek eslesmesi {sorted(best_matched)} · gizlilik={best['gizlilik']}"
          f"{' (gorev gizlilik-isaretli, yerel tercih edildi)' if gizli else ''}"
          f" · dogrulanma={best.get('dogrulanma')} · kanit={best.get('kanit')}")
    if atlanan:
        print(f"KOTA NOTU: dolu kanal atlandi: {', '.join(atlanan)} (G46)")
    if len(hits) > 1:
        alts = ", ".join(c["id"] for c, _ in hits[1:3])
        print(f"ALTERNATIF: {alts}")
    return 0


def cmd_update(args) -> int:
    p = CARDS / f"{args.card_id}.json"
    if not p.exists():
        return _fail(f"kart yok: {args.card_id}")
    print("Sozlu-bildirim akisi: sahibin sohbette soyledigi degisiklik bu komutun cagrisiyla "
          "AJAN tarafindan karta yazilir; bu stub yalniz iz bırakır.")
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="F12a Kanal Sozlesmesi kayit defteri")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("validate")
    sub.add_parser("list")
    r = sub.add_parser("route")
    r.add_argument("--task", required=True)
    r.add_argument("--gizli", action="store_true", help="gizlilik-hassas gorev: yalniz yerel/hibrit")
    u = sub.add_parser("update")
    u.add_argument("card_id")
    a = ap.parse_args()
    return {"init": cmd_init, "validate": cmd_validate, "list": cmd_list,
            "route": cmd_route, "update": cmd_update}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
