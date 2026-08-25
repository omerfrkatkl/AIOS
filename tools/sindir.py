#!/usr/bin/env python3
"""
sindir.py (F10): web arastirma ciktisini yutar -> kanit zincirine cevirir.

Isler:
  digest  : ham metni sindirir — kaynak kutugune yazar, cache'e snapshot alir,
            aday bulgulari cikarir, LEDGER aktif kayitlariyla eslestirir,
            rapora eklenecek markdown parcasi uretir.
  badge   : raporun provenance rozetini kaynak kutugunden hesaplar.
  lookup  : ayni soru daha once arastirildi mi? (G14 onbellek-once)

Kullanim:
  uv run --no-project python tools/sindir.py digest <dosya> --url URL --title "..."
           [--report R-001] [--question "soru"]
  uv run --no-project python tools/sindir.py badge R-001
  uv run --no-project python tools/sindir.py lookup "model benchmark karsilastirmasi"
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
RESEARCH = AIOS_DIR / "research"
CACHE = RESEARCH / "cache"
INDEX = CACHE / "index.jsonl"
SOURCES = CACHE / "sources.jsonl"

sys.path.insert(0, str(AIOS_DIR / "tools"))
try:
    from aioslog import log_event
except Exception:
    def log_event(*a, **k):
        pass

BENCH_PAT = re.compile(
    r"(SWE[- ]?bench|LiveCodeBench|AIME|GPQA|MMLU|HumanEval|Terminal[- ]?Bench|"
    r"Aider? Polyglot|tau[- ]?bench|BrowseComp|ARC[- ]?AGI)", re.I)
RANK_WORDS = re.compile(
    r"\b(top|best|leads?|leading|outperforms?|state[- ]of[- ]the[- ]art|first|"
    r"en güçlü|lider|önde|geçiyor|kırıyor)\b", re.I)


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _fold(s: str) -> str:
    return (s.lower().replace("ç", "c").replace("ğ", "g").replace("ı", "i")
            .replace("ö", "o").replace("ş", "s").replace("ü", "u"))


def qhash(question: str) -> str:
    stop = {"the", "a", "an", "ve", "ile", "icin", "ne", "what", "which",
            "hangi", "en", "of", "in", "to"}
    words = [w for w in re.findall(r"[a-z0-9]+", _fold(question))
             if w not in stop and len(w) > 2]
    return hashlib.sha256(" ".join(sorted(words)).encode()).hexdigest()[:12]


def load_ledger_active() -> list[dict]:
    """Aktif kütük kayıtları (her durum; rejected dahil — hepsi 'ilgili' olabilir)."""
    text = ""
    p = AIOS_DIR / "LEDGER.md"
    if p.exists():
        text = p.read_text(encoding="utf-8")
    out, cur = [], None
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## L-"):
            if cur:
                out.append(cur)
            head = line[3:].split("·")
            cur = {"id": head[0].strip(), "title": head[1].strip() if len(head) > 1 else "",
                   "status": "", "keywords": set()}
        elif cur is not None:
            m = re.match(r"- \*\*(\w+):\*\*\s*(.*)", line.strip())
            if m and m.group(1) == "status":
                cur["status"] = m.group(2).strip()
            elif line.strip() and not line.startswith("#"):
                cur["keywords"].update(
                    w.lower() for w in re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü]{4,}", line))
    if cur:
        out.append(cur)
    return out


def match_ledger(text_lower: str) -> list[str]:
    """Başlık-kelimesi eşleşmesi zorunlu (tek anahtar-kelime yanıltmasın):
    ≥1 başlık kelimesi vuran VE toplam skoru ≥4 olan kayıtlar döner."""
    hits = []
    for entry in load_ledger_active():
        title_words = [w for w in re.findall(r"[a-zçğıöşü]{5,}", entry["title"].lower())]
        t_hits = sum(1 for w in title_words if _fold(w) in _fold(text_lower))
        if t_hits == 0:
            continue
        kw_hits = sum(1 for k in entry["keywords"] if k in text_lower)
        if not (t_hits >= 2 or kw_hits >= 4):
            continue
        score = kw_hits + 2 * t_hits
        if score >= 4:
            hits.append(f"{entry['id']} ({entry['status']}) — {entry['title']} [eşleşme:{score}]")
    return hits


def extract_claims(lines: list[str], limit: int = 8) -> list[str]:
    scored = []
    for ln in lines:
        s = len(BENCH_PAT.findall(ln)) * 3 + len(RANK_WORDS.findall(ln)) * 2
        s += min(len(re.findall(r"\d+(?:\.\d+)?%", ln)), 3)
        if len(ln.strip()) > 40:
            scored.append((s, ln.strip()))
    scored.sort(key=lambda x: -x[0])
    return [t for s, t in scored[:limit] if s > 0]


def cmd_digest(args) -> int:
    src = Path(args.file)
    if not src.exists():
        print(f"HATA: dosya yok: {src}", file=sys.stderr)
        return 1
    raw = src.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    sha = hashlib.sha256(raw).hexdigest()
    ts = now()

    CACHE.mkdir(parents=True, exist_ok=True)
    snap_name = f"{ts.replace(':', '')[:15]}_{sha[:10]}.txt"
    (CACHE / snap_name).write_text(text, encoding="utf-8")

    rec = {"ts": ts, "url": args.url, "title": args.title, "sha256": sha,
           "bytes": len(raw), "snapshot": snap_name,
           "report": args.report or "", "question_hash": qhash(args.question or "")}
    with SOURCES.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    if args.question:
        with INDEX.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"qhash": rec["question_hash"], "question": args.question,
                                "report": args.report or "", "ts": ts}, ensure_ascii=False) + "\n")

    lines = [l for l in text.splitlines() if l.strip()]
    claims = extract_claims(lines)
    ledger_hits = match_ledger(text.lower())

    out = []
    out.append(f"<!-- sindir {ts} · sha256:{sha[:10]} · {len(raw)} bayt -->")
    if claims:
        out.append("**Aday bulgular (sindir çıktısı — doğrulanmadan bulgu sayılmaz):**")
        for c in claims:
            out.append(f"- {c[:300]}")
    else:
        out.append("**Aday bulgu çıkmadı** (ölçüt: benchmark adı / sıralama fiili / % verisi)")
    if ledger_hits:
        out.append("\n**LEDGER eşleşmesi:**")
        out.extend(f"- {h}" for h in ledger_hits)
    print("\n".join(out))

    log_event("sindir", "DIGESTED", "info",
              f"report={args.report} sha={sha[:10]} claims={len(claims)} ledger={len(ledger_hits)}")
    return 0


def cmd_badge(args) -> int:
    rid = args.report_id
    if not SOURCES.exists():
        print(f"[kanıt: 0 kaynak]", end="")
        return 1
    rows = [json.loads(l) for l in SOURCES.read_text(encoding="utf-8").splitlines() if l.strip()]
    mine = [r for r in rows if r.get("report") == rid]
    if not mine:
        print(f"[kanıt: 0 kaynak]", end="")
        return 1
    fresh = max(r["ts"] for r in mine)[:10]
    urls = {r["url"] for r in mine}
    print(f"[kanıt: {len(urls)} kaynak ({len(mine)} getiri) · en taze {fresh}]", end="")
    return 0


def cmd_lookup(args) -> int:
    h = qhash(args.question)
    if INDEX.exists():
        for line in INDEX.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row["qhash"] == h:
                print(f"ÖNBELLEK VURDU: {row['report'] or '(raporsuz)'} · {row['ts']} · \"{row['question']}\"")
                print("→ G14: yeni araştırma açmadan raporu oku/tazele.")
                return 0
    print(f"Önbellek boş (qhash {h}) → yeni araştırma açılabilir.")
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="F10 sindirme hattı")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("digest")
    d.add_argument("file")
    d.add_argument("--url", required=True)
    d.add_argument("--title", required=True)
    d.add_argument("--report")
    d.add_argument("--question")

    b = sub.add_parser("badge")
    b.add_argument("report_id")

    lk = sub.add_parser("lookup")
    lk.add_argument("question")

    args = ap.parse_args()
    return {"digest": cmd_digest, "badge": cmd_badge, "lookup": cmd_lookup}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
