#!/usr/bin/env python3
"""
kesif.py (F12b): otomatik model kesfi — OpenRouter poller + diff raporu (G45).

OpenRouter'in acik modeller listesini ceker, son snapshot ile karsilastirir,
degisiklikleri merdivene gore siniflandirir:

  L1: her degisiklik diffs.jsonl'e loglanir ve raporlanir
  L2: yeni UCRETSIZ model veya buyuk saglayicidan yeni model -> arastirma
      tetikleyici notu ("R-tazeleme onerisi")
  L3: registry kartlarinin referans verdigi model KALDI -> kart-etki UYARISI (G53 ruhu)

Zamanlama F12c'de Task Scheduler ile gelir; v1 istek-uzerine kosar.
Snapshot'lar registry/discovery/ altinda (yerel bolge).

Alt-komutlar:
  poll    cek + snapshot al + diff uret
  show    son diff ozetini goster
"""

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
DISC = AIOS_DIR / "registry" / "discovery"
SNAPS = DISC / "snapshots"
DIFFS = DISC / "diffs.jsonl"
MODELS_URL = "https://openrouter.ai/api/v1/models"
KEEP_SNAPSHOTS = 10

sys.path.insert(0, str(AIOS_DIR / "tools"))

MAJOR = ("openai", "anthropic", "google", "deepseek", "meta", "qwen", "moonshot", "x-ai")


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_models(timeout: int = 30) -> list[dict]:
    req = urllib.request.Request(MODELS_URL, headers={"User-Agent": "AIOS-kesif/1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        payload = json.loads(r.read().decode("utf-8"))
    return [normalize(m) for m in payload.get("data", [])]


def normalize(m: dict) -> dict:
    pricing = m.get("pricing") or {}
    try:
        pp = float(pricing.get("prompt") or 0)
        cp = float(pricing.get("completion") or 0)
    except (TypeError, ValueError):
        pp = cp = -1.0
    return {"id": m.get("id", "?"), "name": m.get("name", "?"),
            "ctx": int(m.get("context_length") or 0),
            "pp": round(pp, 8), "cp": round(cp, 8), "free": pp == 0}


def load_latest_snapshot() -> tuple[str | None, list[dict]]:
    if not SNAPS.exists():
        return None, []
    files = sorted(SNAPS.glob("*.json"))
    if not files:
        return None, []
    data = json.loads(files[-1].read_text(encoding="utf-8-sig"))
    return data["ts"], data["models"]


def save_snapshot(models: list[dict]) -> str:
    SNAPS.mkdir(parents=True, exist_ok=True)
    ts = now()
    (SNAPS / f"{ts.replace(':', '')}.json").write_text(
        json.dumps({"ts": ts, "models": models}, ensure_ascii=False), encoding="utf-8")
    snaps = sorted(SNAPS.glob("*.json"))
    for old in snaps[:-KEEP_SNAPSHOTS]:
        old.unlink()
    return ts


def diff_snapshots(old: list[dict], new: list[dict]) -> list[dict]:
    """Saf fonksiyon — test edilebilir."""
    om = {m["id"]: m for m in old}
    nm = {m["id"]: m for m in new}
    out = []
    for mid in sorted(set(nm) - set(om)):
        out.append({"tur": "YENI", "id": mid, "detay": nm[mid]["name"],
                    "free": nm[mid]["free"], "ctx": nm[mid]["ctx"]})
    for mid in sorted(set(om) - set(nm)):
        out.append({"tur": "KALDI", "id": mid, "detay": om[mid]["name"]})
    for mid in sorted(set(om) & set(nm)):
        o, n = om[mid], nm[mid]
        if o["free"] and not n["free"]:
            out.append({"tur": "UCRETSIZLIK-BITTI", "id": mid, "detay": n["name"]})
        elif not o["free"] and n["free"]:
            out.append({"tur": "UCRETSIZ-OLDU", "id": mid, "detay": n["name"]})
        elif abs(o["pp"] - n["pp"]) > 1e-9 or abs(o["cp"] - n["cp"]) > 1e-9:
            out.append({"tur": "FIYAT", "id": mid,
                        "detay": f"pp {o['pp']}→{n['pp']} · cp {o['cp']}→{n['cp']}"})
        elif o["ctx"] != n["ctx"]:
            out.append({"tur": "CTX", "id": mid, "detay": f"{o['ctx']}→{n['ctx']}"})
    return out


def ladder(changes: list[dict], cards: list[dict]) -> list[str]:
    """Merdiven siniflandirmasi — saf fonksiyon."""
    notes = []
    for c in changes:
        if c["tur"] == "YENI" and (c.get("free") or any(c["id"].startswith(p) for p in MAJOR)):
            notes.append(f"L2 ARASTIRMA-TETIK: {c['id']} "
                         f"{'(ucretsiz)' if c.get('free') else '(buyuk saglayici)'} -> R-tazeleme degerlendirin")
        if c["tur"] == "KALDI":
            for card in cards:
                model_txt = str(card.get("model", "")).lower()
                cid = str(card.get("id", ""))
                frag = c["id"].split("/")[-1].lower()[:18]
                if frag and frag in model_txt:
                    notes.append(f"L3 KART-ETKI: {cid} karti kaldirilan modele referans veriyor: {c['id']} (G53)")
    return notes


def cmd_poll(_) -> int:
    try:
        models = fetch_models()
    except Exception as e:
        print(f"HATA: cekim basarisiz: {e}", file=sys.stderr)
        return 1
    last_ts, old = load_latest_snapshot()
    ts = save_snapshot(models)

    sys_path = AIOS_DIR / "registry" / "cards"
    cards = []
    for p in sorted(sys_path.glob("*.json")):
        if p.name.startswith("_"):
            continue
        try:
            cards.append(json.loads(p.read_text(encoding="utf-8-sig")))
        except json.JSONDecodeError:
            pass

    changes = diff_snapshots(old, models)
    ilk_poll = last_ts is None
    notes = [] if ilk_poll else ladder(changes, cards)

    DISC.mkdir(parents=True, exist_ok=True)
    entry = {"ts": ts, "onceki": last_ts, "model_sayisi": len(models),
             "degisiklik": len(changes)}
    with DIFFS.open("a", encoding="utf-8") as f:
        f.write(json.dumps({**entry, "changes": changes}, ensure_ascii=False) + "\n")

    if ilk_poll:
        print(f"ILK POLL {ts} · {len(models)} model · temel snapshot alindi "
              "(tetik uretilmez — sonraki poll'dan itibaren merdiven aktif)")
        return 0

    print(f"POLL {ts} · onceki={last_ts} · {len(models)} model · {len(changes)} degisiklik")
    for c in changes[:15]:
        print(f"  [{c['tur']}] {c['id']} — {c['detay']}")
    if len(changes) > 15:
        print(f"  … +{len(changes)-15} daha (diffs.jsonl)")
    for n in notes[:10]:
        print(f"  ** {n}")
    if len(notes) > 10:
        print(f"  … +{len(notes)-10} tetik daha (diffs.jsonl)")
    if not changes:
        print("  degisiklik yok — sessiz saglik")
    return 0


def cmd_show(_) -> int:
    if not DIFFS.exists():
        print("henuz poll yok")
        return 0
    rows = [json.loads(l) for l in DIFFS.read_text(encoding="utf-8").splitlines() if l.strip()]
    last = rows[-1]
    print(f"SON POLL: {last['ts']} · {last['model_sayisi']} model · {last['degisiklik']} degisiklik")
    total = sum(r["degisiklik"] for r in rows)
    print(f"GECMIS: {len(rows)} poll · toplam {total} degisiklik kaydi")
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="F12b model kesfi hatti")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("poll")
    sub.add_parser("show")
    a = ap.parse_args()
    return {"poll": cmd_poll, "show": cmd_show}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
