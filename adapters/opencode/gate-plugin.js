// AIOS gate adapter for opencode (v1 - DETECTION ONLY).
//
// SPIKE RESULT (2026-08-24, F4 step 2): opencode's documented hook surface
// (event / tool.execute.before / permission.ask) has NO Stop-hook equivalent
// that can block a completed response. Therefore enforcement here is
// detect + log (weak enforcement). The Claude Code adapter remains the only
// full-block channel. If opencode ships a blocking surface, upgrade this file.
//
// Behaviour: on session.idle (turn finished) it extracts the latest assistant
// text, writes it to logs/opencode-last.txt and runs the AIOS gate in
// --scan-file mode. Matches are logged to logs/aios.jsonl (source=gate,
// surface=opencode) and surfaced by tools/review.py. Everything is guarded:
// a failure must never break the session.

const fs = require("fs")
const path = require("path")
const { spawnSync } = require("child_process")

const AIOS = "C:\\Users\\Atakul\\Documents\\Projects\\AIOS"
const LOG_DIR = path.join(AIOS, "logs")
const LAST_FILE = path.join(LOG_DIR, "opencode-last.txt")
const GATE = path.join(AIOS, "hooks", "gate.py")

function aiosLog(event, severity, msg) {
  try {
    fs.mkdirSync(LOG_DIR, { recursive: true })
    const rec = {
      ts: new Date().toISOString(),
      source: "gate-opencode",
      event,
      severity,
      msg,
    }
    fs.appendFileSync(path.join(LOG_DIR, "aios.jsonl"), JSON.stringify(rec) + "\n")
  } catch {}
}

function collectText(node, out) {
  if (typeof node === "string") out.push(node)
  else if (Array.isArray(node)) node.forEach((n) => collectText(n, out))
  else if (node && typeof node === "object") {
    if (node.type === "text" && typeof node.text === "string") out.push(node.text)
    else if (typeof node.text === "string" && !("type" in node)) out.push(node.text)
    else for (const k of ["content", "message", "parts"]) if (k in node) collectText(node[k], out)
  }
}

async function lastAssistantText(client, sessionID) {
  // Tolerant of SDK shape drift: try the documented call, then fall back.
  let messages
  try {
    const res = await client.session.messages({ sessionID })
    messages = res.data ?? res
  } catch {
    try {
      const res = await client.session.chat({ sessionID })
      messages = res.data ?? res
    } catch (e) {
      aiosLog("ERROR", "error", "message fetch failed: " + (e?.message ?? String(e)))
      return ""
    }
  }
  if (!Array.isArray(messages)) return ""
  for (let i = messages.length - 1; i >= 0; i--) {
    const m = messages[i]
    const role = m?.role ?? m?.info?.role
    if (role !== "assistant") continue
    const out = []
    collectText(m?.parts ?? m?.content ?? m?.info?.parts ?? m, out)
    const text = out.filter((s) => s && s.trim()).join("\n")
    if (text.trim()) return text
  }
  return ""
}

export default async ({ client }) => {
  return {
    event: async ({ event }) => {
      try {
        const type = event?.type ?? event?.name
        if (type !== "session.idle") return
        const sessionID =
          event?.properties?.sessionID ?? event?.sessionID ?? event?.properties?.sessionID
        if (!sessionID) return
        const text = await lastAssistantText(client, sessionID)
        if (!text.trim()) {
          aiosLog("FIRED", "info", "empty response")
          return
        }
        fs.mkdirSync(LOG_DIR, { recursive: true })
        fs.writeFileSync(LAST_FILE, text, "utf-8")
        const r = spawnSync(
          "uv",
          ["run", "--no-project", "python", GATE, "--scan-file", LAST_FILE, "--surface", "opencode"],
          { cwd: AIOS, encoding: "utf-8", timeout: 15_000 },
        )
        if (r.error) aiosLog("ERROR", "error", "gate spawn failed: " + String(r.error))
      } catch (e) {
        aiosLog("ERROR", "error", "fail-open: " + (e?.message ?? String(e)))
      }
    },
  }
}
