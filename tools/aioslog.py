#!/usr/bin/env python3
"""
AIOS logging standard (G32) - the one logging module every tool uses.

One JSONL file: logs/aios.jsonl. One record per event:
  {"ts": "...", "source": "gate", "event": "BLOCKED", "severity": "warn", "msg": "...", ...ctx}

Rules:
- logs/ is LOCAL (gitignored) and is NEVER loaded into an agent context (G26).
- Rotated at MAX_BYTES, KEEP generations kept.
- Logging must never break the calling tool: all failures are swallowed.
- User-facing errors go through user_error(): exactly three lines (G33):
    what happened / why / what to do.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "aios.jsonl"
MAX_BYTES = 5_000_000
KEEP = 3


def _rotate() -> None:
    if LOG_FILE.exists() and LOG_FILE.stat().st_size > MAX_BYTES:
        for i in range(KEEP - 1, 0, -1):
            older = LOG_FILE.with_suffix(f".jsonl.{i}")
            newer = LOG_FILE.with_suffix(f".jsonl.{i + 1}")
            if older.exists():
                older.replace(newer)
        LOG_FILE.replace(LOG_FILE.with_suffix(".jsonl.1"))


def log_event(source: str, event: str, severity: str = "info", msg: str = "", **ctx) -> None:
    """Append one structured event. Never raises."""
    try:
        LOG_DIR.mkdir(exist_ok=True)
        _rotate()
        record = {
            "ts": datetime.now().isoformat(timespec="milliseconds"),
            "source": source,
            "event": event,
            "severity": severity,
            "msg": msg,
        }
        record.update(ctx)
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass


def user_error(what: str, why: str, todo: str) -> None:
    """Three-line user-facing error (G33)."""
    print(f"HATA: {what}\nNEDEN: {why}\nNE YAPMALI: {todo}", file=sys.stderr)


def last_events(source: str = None, event_prefix: str = None, limit: int = 5) -> list[dict]:
    """Read the last matching events (newest last). Never raises."""
    try:
        if not LOG_FILE.exists():
            return []
        out = []
        for line in LOG_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if source and rec.get("source") != source:
                continue
            if event_prefix and not str(rec.get("event", "")).startswith(event_prefix):
                continue
            out.append(rec)
        return out[-limit:]
    except Exception:
        return []
