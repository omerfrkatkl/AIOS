# CLAUDE.md — AIOS working rules

## Session start

1. Read `STATE.md` + `PROFILE.md`, and the active-decision digest (`uv run --no-project python tools/summary.py`, when present).
2. Read `PLAN.md` §8 (Progress) — know the current phase and next step.
3. Open with one line: where we are, what is pending, what is next.

## Session end

4. Update `STATE.md` in place (owner reviews the diff).
5. Update `PLAN.md` §8 if a step or phase moved.
6. Append decisions to `DECISIONS.md` — append-only, never edit old entries.

## Standing rules

- **Evidence tags:** `[gözlendi]` observed · `[üretildi]` generated · `[varsayıldı]` assumed. `[üretildi]` never supports a T-A decision.
- **Tiers:** T-A (expensive to reverse or surfaces late → ≥2 alternatives + owner approval) · T-B (reversible → decide, log, owner may veto) · T-C (local → one line). **Default is T-C.**
- **Visibility ≠ approval.** Silence is never approval. Ledger records activate only with owner-entered dates (PENDING flow).
- Never take machine or world state from a report — run something.
- **Owner Verification Gate:** every tangible change (content, behavior, visual, architectural) is tested by the owner before proceeding. Provide detailed test steps: commands + expected output + pass/fail format.
- **Concurrency rule v1:** one active driver at a time; parallel work runs under the driver and enters the brain through the single writer.
- **Session types:** project / chat / research. A chat session does NOT write STATE/DECISIONS by default — only structured signals flow to the brain (preference / error / correction / approval / deferral), each evidence-tagged.
- **Question discipline (F6, refined 2026-08-24):** two tiers. **Queued questions:** at most ONE per session, at a natural pause; mark `soruldu: <date>`; never asked twice. **Adaptive follow-up chains:** an answer that opens new information may trigger up to THREE immediate follow-ups in the same conversation (interconnected questions are encouraged — G40/G42); stop when the model stops improving or the owner signals enough. Every answer lands in the matching PROFILE layer with an evidence tag; the queue row is marked `cevaplandı`. If nothing is worth asking, ask nothing (G42: yield, not count).
- **Personality layer:** as it fills, adapt tone and phrasing to it. It is advisory, not a cage — accuracy beats flattery.
- **Learning audit (F6):** after the owner confirms learned items, run `tools/backup.py` to set a new audit baseline. `tools/audit.py` diffs PROFILE/LEDGER against it — show the diff, fix/delete what the owner rejects. Interview mode (F6b): "beni tanı" starts batched adaptive questioning (3–5 interconnected per group, vault-first, platform-priority order); no per-session limit in this mode — G42 efficiency and never-repeat still apply.
- **Vault discipline (F7):** two vaults — `vault/` (AIOS's personal knowledge store: writable, local-only, included in backups) and `Documents/All` (owner's knowledge vault: READ-ONLY for AIOS). Before asking the owner personal-preference questions, check both with TARGETED reads (by filename/folder/keyword); never dump a full vault into context. Open question (owner decides): whether AIOS learnings mirror into `vault/`.
- Language: speak Turkish to the owner; machine-facing files and code in English; conversation records (STATE/DECISIONS/REQUIREMENTS content) in Turkish; ledger keys bilingual.
- No new durable file without four fields: purpose, lifecycle, owner, read trigger.
- **Personal layer never enters git:** PROFILE.md, LEDGER.md, logs/, inventory. Never paste them into public channels.
- `arsiv/` is reference only — no rule from it applies unless re-adopted by a decision.
- Do not start new managed projects before the pilot phase (F8).
- Anti-patterns (all observed once): meta-loops · document inflation · substring matching on natural language · self-confirming tests · silent staleness · treating a working mechanism as forever-proven.
