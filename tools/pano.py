#!/usr/bin/env python3
"""
HTML Panosu (F9.5): brain'den statik durum sayfası üretir.

Format: SplitWire-referanslı — sol sidebar navigasyon, üst durum çipleri
(renkli noktalı), kart grid'i. Koyu tema + amber vurgu. Tek dosya, harici
bağımlılık yok. Çıktı: pano.html (yerel, gitignored). Oturum sonunda tazelenir.

Kullanım: uv run --no-project python tools/pano.py
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

AIOS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AIOS_DIR / "tools"))
from aioslog import last_events, log_event  # noqa: E402

PANO = AIOS_DIR / "pano.html"


def read(name: str) -> str:
    p = AIOS_DIR / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


def section(text: str, header: str) -> list[str]:
    lines, grab = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            grab = line.strip().lower().startswith("## " + header.lower())
            continue
        if grab and line.strip():
            lines.append(line.strip())
    return lines


def decisions_timeline(limit: int = 12) -> str:
    text = read("DECISIONS.md")
    rows, cur = [], None
    for line in text.splitlines():
        if line.startswith("## 2"):
            if cur:
                rows.append(cur)
            parts = [p.strip() for p in line[3:].split("·")]
            cur = {"date": parts[0] if parts else "?",
                   "title": parts[1] if len(parts) > 1 else "?",
                   "meta": " · ".join(parts[2:]) if len(parts) > 2 else ""}
    if cur:
        rows.append(cur)
    rows = rows[-limit:][::-1]
    return "".join(
        f'<div class="row"><span class="date">{r["date"]}</span>'
        f'<span class="title">{r["title"]}</span>'
        f'<span class="meta">{r["meta"]}</span></div>'
        for r in rows
    ) or '<div class="empty">kayıt yok</div>'


def ledger_counts() -> dict:
    text = read("LEDGER.md")
    counts = {"approved": 0, "rejected": 0, "deferred": 0}
    pending, in_fence = 0, False
    status = active = None
    for line in text.splitlines() + ["## L-999999 · sentinel"]:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## L-"):
            if status is not None:
                if active:
                    counts[status] = counts.get(status, 0) + 1
                else:
                    pending += 1
            status, active = None, None
        elif line.startswith("- **status:**"):
            status = line.split("**status:**")[1].strip()
        elif line.startswith("- **active:**"):
            active = line.split("**active:**")[1].strip()
    counts["pending"] = pending
    return counts


def coverage_rows() -> str:
    text = read("PROFILE.md")
    line = next((l for l in text.splitlines() if "Kapsam güncelleme" in l), "")
    m = re.findall(r"([\wçğıöşü/ ]+?) ~%(\d+)", line)
    if not m:
        return '<div class="empty">kapsam haritası henüz yok</div>'
    out = ""
    for name, pct in m:
        pct = int(pct)
        out += (f'<div class="bar-row"><span class="bar-name">{name.strip()}</span>'
                f'<div class="bar"><div class="fill" style="width:{pct}%"></div></div>'
                f'<span class="bar-pct">%{pct}</span></div>')
    return out


def context_chip() -> str:
    evs = last_events(source="context_cost", limit=1)
    lines = evs[-1].get("lines") if evs else None
    if isinstance(lines, int):
        ok = lines <= 446
        return (f'<span class="chip"><span class="dot {"ok" if ok else "bad"}"></span>'
                f'Açılış: {lines} satır</span>')
    return '<span class="chip"><span class="dot"></span>Açılış: ölçüm yok</span>'


def gate_chip() -> str:
    evs = last_events(source="gate", limit=1)
    if not evs:
        return '<span class="chip"><span class="dot bad"></span>Kapı: hiç ateşlenmedi</span>'
    e = evs[-1]
    ev = e.get("event", "?")
    cls = "ok" if ev in ("FIRED", "clean") or "FIRED" in ev else ("warn" if "BLOCK" in ev else "")
    return (f'<span class="chip"><span class="dot {cls}"></span>'
            f'Kapı: {ev} ({e.get("ts", "")[:16][11:]})</span>')


CSS = """
*{box-sizing:border-box;margin:0}
body{background:#141414;color:#d4d4d4;font-family:'Segoe UI',system-ui,sans-serif;
     display:flex;min-height:100vh}
aside{width:200px;background:#1c1c1c;border-right:1px solid #2a2a2a;position:fixed;
      top:0;bottom:0;left:0;display:flex;flex-direction:column}
.logo{padding:18px 20px;font-size:16px;font-weight:600;color:#e3a857;border-bottom:1px solid #2a2a2a}
nav{display:flex;flex-direction:column;padding:10px 0}
nav a{padding:10px 20px;color:#999;text-decoration:none;font-size:13px;border-left:3px solid transparent}
nav a:hover{color:#d4d4d4;background:#222}
nav a.active{color:#e3a857;border-left-color:#e3a857;background:#222}
main{margin-left:200px;flex:1;padding:0 28px 40px}
.topbar{display:flex;align-items:center;gap:14px;background:#1c1c1c;border-bottom:1px solid #2a2a2a;
        padding:14px 20px;margin:0 -28px 24px;position:sticky;top:0;z-index:2}
.chip{display:inline-flex;align-items:center;gap:7px;background:#222;border:1px solid #2a2a2a;
      border-radius:6px;padding:6px 12px;font-size:12px;color:#bbb}
.dot{width:8px;height:8px;border-radius:50%;background:#666;display:inline-block}
.dot.ok{background:#7ec96f}.dot.bad{background:#e05252}.dot.warn{background:#e3a857}
.refresh{margin-left:auto;background:#2a2a2a;border:1px solid #3a3a3a;color:#ccc;border-radius:6px;
         padding:6px 14px;cursor:pointer;font-size:12px}
.refresh:hover{background:#333}
h2{font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#e3a857;margin:26px 0 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px}
.card{background:#1e1e1e;border:1px solid #2c2c2c;border-radius:8px;padding:16px}
.card .label{font-size:11px;text-transform:uppercase;letter-spacing:.8px;color:#888;margin-bottom:8px}
.card .value{font-size:17px;font-weight:600;color:#e8e8e8}
.card .value.ok{color:#7ec96f}.card .value.warn{color:#e3a857}.card .value.bad{color:#e05252}
.card .desc{font-size:12px;color:#777;margin-top:6px}
.panel{background:#1e1e1e;border:1px solid #2c2c2c;border-radius:8px;padding:16px;margin-bottom:20px}
.row{display:flex;gap:10px;padding:7px 0;border-bottom:1px solid #262626;font-size:13px;align-items:baseline}
.row:last-child{border-bottom:none}
.date{color:#888;font-size:12px;min-width:78px}
.title{flex:1;color:#d4d4d4}
.meta{color:#888;font-size:12px}
.bar-row{display:flex;align-items:center;gap:12px;margin:8px 0;font-size:13px}
.bar-name{width:200px}.bar-pct{width:46px;color:#888;text-align:right}
.bar{flex:1;background:#2c2c2c;border-radius:4px;height:7px;overflow:hidden}
.fill{height:100%;background:#e3a857;border-radius:4px}
.chips{display:flex;gap:10px;flex-wrap:wrap}
.empty{color:#777;font-size:13px;font-style:italic}
.footer{margin-top:36px;color:#555;font-size:11px}
"""


def build() -> str:
    state = read("STATE.md")
    durum = section(state, "Durum")
    siradaki = section(state, "Sıradaki")
    profile = read("PROFILE.md")
    counts = ledger_counts()

    otonom_rows = [
        l.strip().strip("|") for l in profile.splitlines()
        if l.strip().startswith("|") and "→" in l and "Seviye" not in l and "---" not in l
    ]
    otonom_html = "".join(
        f'<div class="row"><span class="title">{re.sub(r"^", "", l.strip())}</span></div>'
        for l in otonom_rows[:8]
    ) or '<div class="empty">—</div>'

    durum_html = "".join(
        f"<li>{re.sub(r'^- ', '', d)}</li>" for d in durum
    ) or "<li>—</li>"
    sira_html = "".join(
        f"<li>{re.sub(r'^\\d+\\.\\s*', '', s)}</li>" for s in siradaki
    ) or "<li>—</li>"

    gate = gate_chip()
    ctx = context_chip()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><title>AIOS Panosu</title>
<style>{CSS}</style></head><body>

<aside>
  <div class="logo">AIOS</div>
  <nav>
    <a href="#durum" class="active">Durum</a>
    <a href="#kararlar">Kararlar</a>
    <a href="#kutuk">Kütük</a>
    <a href="#tanima">Tanıma</a>
    <a href="#olcumler">Ölçümler</a>
  </nav>
</aside>

<main>
  <div class="topbar">
    {gate}
    {ctx}
    <span class="chip"><span class="dot ok"></span>Pilot: aktif (ledger)</span>
    <span class="chip"><span class="dot ok"></span>Kütük: {counts['rejected']} rejected</span>
    <button class="refresh" onclick="location.reload()">Yenile</button>
  </div>

  <section id="durum">
    <h2>Durum</h2>
    <div class="panel"><ul>{durum_html}</ul></div>
    <h2 style="margin-top:18px">Sıradaki</h2>
    <div class="panel"><ul>{sira_html}</ul></div>
  </section>

  <section id="kararlar">
    <h2>Karar zaman çizelgesi (son 12)</h2>
    <div class="panel">{decisions_timeline()}</div>
  </section>

  <section id="kutuk">
    <h2>Kütük (LEDGER)</h2>
    <div class="grid">
      <div class="card"><div class="label">APPROVED</div><div class="value ok">{counts['approved']}</div></div>
      <div class="card"><div class="label">REJECTED</div><div class="value bad">{counts['rejected']}</div></div>
      <div class="card"><div class="label">DEFERRED</div><div class="value warn">{counts['deferred']}</div></div>
      <div class="card"><div class="label">PENDING</div><div class="value">{counts['pending']}</div></div>
    </div>
  </section>

  <section id="tanima">
    <h2>Tanıma kapsamı</h2>
    <div class="panel">{coverage_rows()}</div>
  </section>

  <section id="otonom">
    <h2>Otonom seviyeleri</h2>
    <div class="panel">{otonom_html}</div>
  </section>

  <section id="olcumler">
    <h2>Ölçümler</h2>
    <div class="panel">{ctx}<div class="sub" style="margin-top:8px">hedef ≤446 satır · bazal 892 · tools/context_cost.py ile ölçülür</div></div>
  </section>

  <div class="footer">AIOS panosu · {now} · tools/pano.py üretimi · yerel dosya, git'e girmez</div>
</main></body></html>"""


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    PANO.write_text(build(), encoding="utf-8")
    log_event("pano", "GENERATED", "info", str(PANO))
    print(f"Pano üretildi: {PANO}")
    print("Tarayıcıda aç: start pano.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
