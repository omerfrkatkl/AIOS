#!/usr/bin/env python3
"""
sindir.py v2 (F10): web arastirma ciktisini yutar -> makine-denetlenebilir
kanit zincirine cevirir. Kriter kitabi: research/README.md (v2).

Alt-komutlar:
  digest  : ham metni sindirir — kaynak kutugu (+derece/gerekce/mod),
            snapshot, aday bulgular, LEDGER eslesmesi, sorgu-kutugu.
  claim   : yapilandirilmis sayisal iddia yazar (R-*.claims.jsonl).
            Yuzdesel degerler 0-100 normalize edilir; tekrar yazilamaz.
  badge   : raporun provenance rozeti (kaynak/derece/tazelik).
  lookup  : ayni soru daha once arastirildi mi? (G14 onbellek-once)
  check   : raporu kriter kitabina gore denetler. exit 0=temiz 1=uyari 2=hata.
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
SOURCES = RESEARCH / "sources.jsonl"
QUERIES = RESEARCH / "queries.jsonl"
ALIASES = RESEARCH / "aliases.jsonl"

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

TIERS = ("T1-nötr", "T1-kendi-beyanı", "T2", "T3")
HEADER_KEYS = ("id", "tarih", "tur", "tetik", "guven", "manşet", "kaynaklar")


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _fold(s: str) -> str:
    return (s.lower().replace("ç", "c").replace("ğ", "g").replace("ı", "i")
            .replace("ö", "o").replace("ş", "s").replace("ü", "u"))


def qhash(question: str) -> str:
    stop = {"the", "a", "an", "ve", "ile", "icin", "ne", "what", "which",
            "hangi", "en", "of", "in", "to"}
    words = [w for w in re.findall(r"[a-z0-9]+", _fold(question))
             if w not in stop and len(w) > 2]
    return hashlib.sha256(" ".join(sorted(words)).encode()).hexdigest()[:12]


def norm_percent(text: str) -> float | None:
    """'96%' / '0.950' / '96.0' -> 0-100 ölçeği (yaklaşım kuralı kodda sabit)."""
    t = text.strip().replace(",", ".").rstrip("%").strip()
    try:
        v = float(t)
    except ValueError:
        return None
    had_pct = "%" in text
    if not had_pct and 0 < v <= 1:
        v *= 100
    return round(v, 2)


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


def report_path(report_id: str) -> Path | None:
    m = re.fullmatch(r"R-(\d{3})", report_id)
    if not m:
        return None
    hits = sorted(RESEARCH.glob(f"R-{m.group(1)}-*.md"))
    return hits[0] if hits else None


def load_ledger_entries() -> list[dict]:
    """LEDGER.md kayitlarinin hepsi (ad 'aktif' degil — tum kayitlar taranir)."""
    p = AIOS_DIR / "LEDGER.md"
    text = p.read_text(encoding="utf-8") if p.exists() else ""
    out, cur, in_fence = [], None, False
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
    """Başlık-kelimesi eşleşmesi zorunlu: ≥1 başlık kelimesi vuran VE
    (t_hits≥2 veya kw_hits≥4) ve skor≥4 olan kayıtlar."""
    hits = []
    for entry in load_ledger_entries():
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
    scored, seen = [], set()
    for ln in lines:
        s = len(BENCH_PAT.findall(ln)) * 3 + len(RANK_WORDS.findall(ln)) * 2
        s += min(len(re.findall(r"\d+(?:\.\d+)?%", ln)), 3)
        key = ln.strip()[:120]
        if key in seen:
            continue
        seen.add(key)
        if len(ln.strip()) > 40:
            scored.append((s, ln.strip()))
    scored.sort(key=lambda x: -x[0])
    return [t for s, t in scored[:limit] if s > 0]


def cmd_digest(args) -> int:
    src = Path(args.file)
    if not src.exists():
        print(f"HATA: dosya yok: {src}", file=sys.stderr)
        return 1
    if args.report and not report_path(args.report):
        print(f"HATA: {args.report} diye rapor yok — öksüz kaynak kaydı açılmaz.", file=sys.stderr)
        return 1
    if args.tier and args.tier not in TIERS:
        print(f"HATA: derece {TIERS} içinden olmalı.", file=sys.stderr)
        return 1
    if args.tier and not args.gerekce:
        print("HATA: derece verildi ama gerekçe yok — kontrol-listesi gerekçesi zorunlu "
              "(README v2: derece ataması öznel değil, liste tabanlı).", file=sys.stderr)
        return 1

    raw = src.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    sha = hashlib.sha256(raw).hexdigest()
    ts = now()

    CACHE.mkdir(parents=True, exist_ok=True)
    snap_name = f"{ts.replace(':', '')[:15]}_{sha[:10]}.txt"
    (CACHE / snap_name).write_text(text, encoding="utf-8")

    rec = {"ts": ts, "url": args.url, "title": args.title, "sha256": sha,
           "bytes": len(raw), "snapshot": snap_name, "report": args.report or "",
           "question_hash": qhash(args.question or ""),
           "tier": args.tier or "", "gerekce": args.gerekce or "",
           "mode": args.mode}
    append_jsonl(SOURCES, rec)

    if args.query:
        append_jsonl(QUERIES, {"ts": ts, "query": args.query,
                               "kind": "counter" if args.counter else "ana",
                               "tool": args.tool, "report": args.report or ""})

    if args.question:
        append_jsonl(INDEX, {"qhash": rec["question_hash"], "question": args.question,
                             "report": args.report or "", "ts": ts})

    lines = [l for l in text.splitlines() if l.strip()]
    claims = extract_claims(lines)
    ledger_hits = match_ledger(text.lower())

    out = [f"<!-- sindir {ts} · sha256:{sha[:10]} · {len(raw)} bayt · "
           f"derece:{args.tier or '-'} · mod:{args.mode} -->"]
    if claims:
        out.append("**Aday bulgular (sindir çıktısı — doğrulanmadan bulgu sayılmaz):**")
        out.extend(f"- {c[:300]}" for c in claims)
    else:
        out.append("**Aday bulgu çıkmadı** (ölçüt: benchmark adı / sıralama fiili / % verisi)")
    if ledger_hits:
        out.append("\n**LEDGER eşleşmesi:**")
        out.extend(f"- {h}" for h in ledger_hits)
    print("\n".join(out))

    log_event("sindir", "DIGESTED", "info",
              f"report={args.report} sha={sha[:10]} claims={len(claims)} ledger={len(ledger_hits)}")
    return 0


def cmd_claim(args) -> int:
    rp = report_path(args.report)
    if not rp:
        print(f"HATA: {args.report} diye rapor yok.", file=sys.stderr)
        return 1
    val = norm_percent(args.deger)
    if val is None:
        print(f"HATA: değer sayısal değil: {args.deger!r}", file=sys.stderr)
        return 1
    if args.derece and args.derece not in TIERS:
        print(f"HATA: derece {TIERS} içinden olmalı.", file=sys.stderr)
        return 1
    claims_file = rp.with_name(rp.stem + ".claims.jsonl")
    existing = read_jsonl(claims_file)
    row = {"model": args.model, "metrik": args.metrik, "deger": val,
           "obs": args.obs or "", "harness": args.harness or "",
           "kaynak": args.kaynak or "", "derece": args.derece or "", "not": args.not_ or ""}
    key = (model_key(row["model"]), _fold(row["metrik"]), row["deger"], row["obs"])
    for e in existing:
        if (model_key(e.get("model", "")), _fold(e.get("metrik", "")),
                e.get("deger"), e.get("obs")) == key:
            print(f"ATLANDI (tekrar): aynı model+metrik+değer+obs zaten kayıtlı.")
            return 0
    append_jsonl(claims_file, row)
    print(f"iddia eklendi: {row['model']} · {row['metrik']} · {val} · obs={row['obs'] or '?'}"
          f" · {row['derece'] or '-'} ({len(existing)+1}. satır)")
    return 0


def parse_header(rp: Path) -> dict:
    hdr = {}
    for line in rp.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*\*{0,2}([^|*]+?)\*{0,2}\s*\|\s*([^|]+?)\s*\|\s*$", line)
        if m:
            hdr[_fold(m.group(1)).strip()] = m.group(2).strip()
    return hdr


def cmd_check(args) -> int:
    rp = report_path(args.report_id)
    if not rp:
        print(f"HATA: {args.report_id} diye rapor yok.", file=sys.stderr)
        return 2
    hdr_raw = parse_header(rp)
    hdr = {_fold(k): v for k, v in hdr_raw.items()}
    items = []

    def add(level, msg):
        items.append((level, msg))

    missing_keys = [k for k in HEADER_KEYS if _fold(k) not in hdr]
    if missing_keys:
        add(2, f"başlık anahtarları eksik: {', '.join(missing_keys)}")
    else:
        add(0, f"başlık anahtarları tam (tur={hdr['tur']}, tetik={hdr['tetik']}, güven={hdr['guven']})")

    srcs = [r for r in read_jsonl(SOURCES) if r.get("report") == args.report_id]
    urls = {r["url"] for r in srcs}
    tiers, tiers_full = {}, {}
    for r in srcs:
        if not r.get("tier"):
            add(1, f"kaynak derecesiz: {r['title']}")
        elif not r.get("gerekce"):
            add(1, f"derece gerekçesiz: {r['title']}")
        else:
            tiers.setdefault(r["tier"], set()).add(r["url"])
            if r.get("mode") == "tam":
                tiers_full.setdefault(r["tier"], set()).add(r["url"])
    if not srcs:
        add(2, "kayıtlı kaynak yok")
    support = (len(tiers_full.get("T1-nötr", set())) >= 1
               or len(tiers_full.get("T2", set())) >= 3)
    if support:
        add(0, "manşet desteği: kural sağlandı "
               f"(tam-çekim T1-nötr={len(tiers_full.get('T1-nötr', set()))}, "
               f"T2={len(tiers_full.get('T2', set()))})")
    else:
        add(2, "manşet desteği YOK: ≥1×T1-nötr veya ≥3×T2 tam-çekim kaynak gerekli")

    qs = [q for q in read_jsonl(QUERIES) if q.get("report") == args.report_id]
    if not any(q.get("kind") == "counter" for q in qs):
        add(2, "karşıt-kanıt sorgusu kaydı yok (negatif-arama protokolü)")
    else:
        add(0, "karşıt-kanıt sorgusu kayıtlı")

    claims = read_jsonl(rp.with_name(rp.stem + ".claims.jsonl"))
    conflicts = detect_conflicts(claims)
    if conflicts:
        for c in conflicts:
            add(1, f"çelişki adayı: {c}")
    elif claims:
        add(0, "iddia katmanı tutarlı (çelişki yok)")
    else:
        add(1, "iddia katmanı boş — sayısal bulgular yapılandırılmamış")

    stale = False
    if "tetik" in hdr:
        stale = hdr["tetik"] < today()
        add(1 if stale else 0, "rapor STALE (tetik geçti)" if stale else "tazelik: geçerli")

    comp = compute_guven(support, stale, bool(conflicts), tiers)
    if "guven" in hdr:
        order = {"yüksek": 3, "orta": 2, "düşük": 1}
        dec = order.get(hdr["guven"], 0)
        cmp_ = order[comp]
        if dec > cmp_:
            add(2, f"güven şişirme: bildirilen {hdr['guven']} > hesaplanan {comp}")
        elif dec < cmp_:
            add(1, f"güven aşağıda: bildirilen {hdr['guven']} < hesaplanan {comp} (konservatif, sorun değil)")
        else:
            add(0, f"güven etiketi tutarlı ({comp})")

    worst = max((lvl for lvl, _ in items), default=0)
    icons = {0: "[OK]", 1: "[UYARI]", 2: "[HATA]"}
    for lvl, msg in items:
        print(f"{icons[lvl]} {msg}")
    label = {0: "TEMİZ", 1: "UYARILI", 2: "HATALI"}[worst]
    print(f"\ncheck sonucu: {label} (exit {worst}) · kaynak {len(urls)} URL · iddia {len(claims)}")
    return worst


def compute_guven(support, stale, conflicts, tiers) -> str:
    t3_only = bool(tiers) and set(tiers) <= {"T3", "T1-kendi-beyanı"}
    if t3_only or stale or conflicts:
        return "düşük"
    if support:
        return "yüksek"
    return "orta"


def model_key(s: str) -> str:
    """Model kimliği anahtarı: fold + ayırıcı temizliği ('Opus 5'=='Opus5'=='opus-5')."""
    return re.sub(r"[^a-z0-9]", "", _fold(s))


def detect_conflicts(claims) -> list[str]:
    groups = {}
    for c in claims:
        key = (model_key(c.get("model", "")), _fold(c.get("metrik", "")))
        groups.setdefault(key, []).append(c)
    out = []
    for (model, metrik), rows in groups.items():
        vals = [(r.get("deger"), r.get("harness", ""), r.get("obs", ""))
                for r in rows if isinstance(r.get("deger"), (int, float))]
        for i in range(len(vals)):
            for j in range(i + 1, len(vals)):
                (v1, h1, o1), (v2, h2, o2) = vals[i], vals[j]
                same_harness = (not h1 or not h2 or _fold(h1) == _fold(h2))
                if same_harness and abs(v1 - v2) > 3:
                    out.append(f"{rows[0]['model']}·{metrik}: {v1} vs {v2} "
                               f"({h1 or 'harness?'}/{o1 or '?'}, {h2 or 'harness?'}/{o2 or '?'})")
    return out


def cmd_badge(args) -> int:
    rid = args.report_id
    mine = [r for r in read_jsonl(SOURCES) if r.get("report") == rid]
    if not mine:
        print("[kanıt: 0 kaynak]", end="")
        return 1
    fresh = max(r["ts"] for r in mine)[:10]
    urls = {r["url"] for r in mine}
    comp = {}
    for r in mine:
        if r.get("tier"):
            comp[r["tier"]] = comp.get(r["tier"], 0) + 1
    comp_s = " ".join(f"{k}×{v}" for k, v in sorted(comp.items())) or "derecesiz"
    print(f"[kanıt: {len(urls)} kaynak ({len(mine)} getiri) · en taze {fresh} · {comp_s}]", end="")
    return 0


def cmd_lookup(args) -> int:
    h = qhash(args.question)
    for row in read_jsonl(INDEX):
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
    ap = argparse.ArgumentParser(description="F10 sindirme hattı v2")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("digest")
    d.add_argument("file")
    d.add_argument("--url", required=True)
    d.add_argument("--title", required=True)
    d.add_argument("--report")
    d.add_argument("--question")
    d.add_argument("--tier", help=f"{TIERS}")
    d.add_argument("--gerekce", help="derece kontrol-listesi gerekçesi")
    d.add_argument("--mode", choices=("tam", "ozet"), default="ozet")
    d.add_argument("--query", help="bu kaynağı getiren arama sorgusu")
    d.add_argument("--tool", default="websearch")
    d.add_argument("--counter", action="store_true", help="karşıt-kanıt sorgusu olarak kaydet")

    c = sub.add_parser("claim")
    c.add_argument("--report", required=True)
    c.add_argument("--model", required=True)
    c.add_argument("--metrik", required=True)
    c.add_argument("--deger", required=True)
    c.add_argument("--obs", default="")
    c.add_argument("--harness", default="")
    c.add_argument("--kaynak", default="")
    c.add_argument("--derece", default="")
    c.add_argument("--not", dest="not_", default="")

    b = sub.add_parser("badge")
    b.add_argument("report_id")

    lk = sub.add_parser("lookup")
    lk.add_argument("question")

    ck = sub.add_parser("check")
    ck.add_argument("report_id")

    args = ap.parse_args()
    fn = {"digest": cmd_digest, "claim": cmd_claim, "badge": cmd_badge,
          "lookup": cmd_lookup, "check": cmd_check}[args.cmd]
    return fn(args)


if __name__ == "__main__":
    sys.exit(main())
