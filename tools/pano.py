#!/usr/bin/env python3
"""
HTML Panosu (F9.5): brain'den statik durum sayfası üretir.

Kaynak: STATE.md, DECISIONS.md (son 10), LEDGER.md, PROFILE.md (kapsam+otonom),
logs/aios.jsonl (context_cost son ölçüm). Çıktı: pano.html (yerel, gitignored).

Tasarım: koyu / minimal modern (vault/Preferences/design-taste.md — sahibin zevki).
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
    """STATE benzeri dosyadan '## header' bölümünün gövdesini döndürür."""
    lines, grab = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            grab = line.strip().lower().startswith("## " + header.lower())
            continue
        if grab and line.strip():
            lines.append(line.strip())
    return lines


def decisions_timeline(limit: int = 10) -> str:
    text = read("DECISIONS.md")
    rows, cur = [], None
    for line in text.splitlines():
        if line.startswith("## 2"):
            if cur:
                rows.append(cur)
            parts = [p.strip() for p in line[3:].split("·")]
            cur = {"date": parts[0] if parts else "?", "title": parts[1] if len(parts) > 1 else "?",
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


def ledger_block() -> str:
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
    return (f'<div class="chips">'
            f'<span class="chip ok">approved {counts["approved"]}</span>'
            f'<span class="chip bad">rejected {counts["rejected"]}</span>'
            f'<span class="chip warn">deferred {counts["deferred"]}</span>'
            f'<span class="chip">PENDING {pending}</span></div>')


def coverage_block() -> str:
    text = read("PROFILE.md")
    line = next((l for l in text.splitlines() if "Kapsam güncelleme" in l), "")
    m = re.findall(r"([\wçğıöşü/ ]+?) ~%(\d+)", line)
    if not m:
        return '<div class="empty">kapsam haritası henüz yok</div>'
    bars = ""
    for name, pct in m:
        pct = int(pct)
        bars += (f'<div class="bar-row"><span class="bar-name">{name.strip()}</span>'
                 f'<div class="bar"><div class="fill" style="width:{pct}%"></div></div>'
                 f'<span class="bar-pct">%{pct}</span></div>')
    return bars


def context_block() -> str:
    evs = [e for e in last_events(source="context_cost", limit=1)]
    if not evs:
        return '<div class="empty">ölçüm yok</div>'
    e = evs[-1]
    lines = e.get("lines", "?")
    color = "#3fb950" if isinstance(lines, int) and lines <= 446 else "#f85149"
    return (f'<div class="big" style="color:{color}">{lines} satır</div>'
            f'<div class="sub">hedef ≤446 · bazal 892</div>')


def gate_block() -> str:
    evs = [e for e in last_events(source="gate", limit=1)]
    if not evs:
        return '<div class="empty">kapı hiç ateşlenmedi</div>'
    e = evs[-1]
    return (f'<div class="big">{e.get("event", "?")}</div>'
            f'<div class="sub">{e.get("ts", "")[:19].replace("T", " ")} UTC</div>')


CSS = """
body{background:#0d1117;color:#c9d1d9;font-family:'Segoe UI',system-ui,sans-serif;
     margin:0;padding:24px;max-width:960px;margin-inline:auto}
h1{font-size:22px;font-weight:600;color:#e6edf3;margin:0 0 4px}
h2{font-size:13px;text-transform:uppercase;letter-spacing:1px;color:#8b949e;
   margin:28px 0 10px;border-bottom:1px solid #21262d;padding-bottom:6px}
.sub{color:#8b949e;font-size:12px}.date{color:#8b949e;margin-right:12px;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.card{background:#161b22;border:1px solid #21262d;border-radius:8px;padding:14px 16px}
.card h3{margin:0 0 8px;font-size:12px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px}
.big{font-size:26px;font-weight:600;color:#e6edf3}
.row{display:flex;gap:8px;padding:5px 0;border-bottom:1px solid #161b22;font-size:13px;align-items:baseline}
.title{flex:1}.meta{color:#8b949e;font-size:12px}
.chips{display:flex;gap:8px;flex-wrap:wrap}
.chip{background:#21262d;border-radius:12px;padding:3px 10px;font-size:12px}
.chip.ok{color:#3fb950}.chip.bad{color:#f85149}.chip.warn{color:#d29922}
.bar-row{display:flex;align-items:center;gap:10px;margin:6px 0;font-size:13px}
.bar-name{width:180px;color:#c9d1d9}.bar-pct{width:44px;color:#8b949e;text-align:right}
.bar{flex:1;background:#21262d;border-radius:4px;height:8px;overflow:hidden}
.fill{height:100%;background:#58a6ff;border-radius:4px}
ul{margin:4px 0;padding-left:18px;font-size:13px;line-height:1.7}
li::marker{color:#58a6ff}.empty{color:#8b949e;font-size:13px;font-style:italic}
.footer{margin-top:32px;color:#484f58;font-size:11px;text-align:center}
"""


def build() -> str:
    state = read("STATE.md")
    durum = section(state, "Durum")
    siradaki = section(state, "Sıradaki")
    profile = read("PROFILE.md")
    otonom_lines = [
        l for l in profile.splitlines()
        if l.strip().startswith("|") and "— " not in l and "Seviye" not in l
        and "---" not in l and l.strip() != "| | |"
    ]
    otonom = "".join(f'<div class="row"><span class="title">{l.strip().strip("|")}</span></div>'
                     for l in otonom_lines[:8]) or '<div class="empty">—</div>'
    durum_html = "".join(f"<li>{re.sub(r'^- ', '', d)}</li>" for d in durum) or "<li>—</li>"
    sira_html = "".join(f"<li>{re.sub(r'^\\d+\\.\\s*', '', s)}</li>" for s in siradaki) or "<li>—</li>"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8">
<title>AIOS Panosu</title><style>{CSS}</style></head><body>
<h1>AIOS Panosu</h1><div class="sub">üretim: {now} · tools/pano.py · elle düzenlenmez</div>

<h2>Sıradaki</h2><ul>{sira_html}</ul>

<h2>Ölçümler</h2>
<div class="grid">
<div class="card"><h3>Açılış bağlamı</h3>{context_block()}</div>
<div class="card"><h3>Kapı (son olay)</h3>{gate_block()}</div>
</div>

<h2>Kütük (LEDGER)</h2>{ledger_block()}

<h2>Karar zaman çizelgesi (son 10)</h2>{decisions_timeline()}

<h2>Tanıma kapsamı</h2>{coverage_block()}

<h2>Otonom seviyeleri</h2>{otonom}

<h2>Sistem durumu</h2><ul>{durum_html}</ul>

<div class="footer">AIOS · yerel panosu · kaynak: brain dosyaları · bu dosya git'e girmez</div>
</body></html>"""


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
