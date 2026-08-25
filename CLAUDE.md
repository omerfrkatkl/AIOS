# CLAUDE.md — AIOS working rules

## Session start

1. Read `STATE.md` + `PROFILE.md`, and the active-decision digest (`uv run --no-project python tools/summary.py`, when present).
2. Read `PLAN.md` §8 (Progress) — know the current phase and next step.
3. Open with one line: where we are, what is pending, what is next.
4. If this session's likely work matches a skill trigger in `skills/README.md`, load that skill before starting (F11).

## Session end

4. Update `STATE.md` in place (owner reviews the diff).
5. Update `PLAN.md` §8 if a step or phase moved.
6. Append decisions to `DECISIONS.md` — append-only, never edit old entries.
7. Regenerate the owner dashboard: `uv run --no-project python tools/pano.py` (F9.5).

## Standing rules

- **Evidence tags:** `[gözlendi]` observed · `[üretildi]` generated · `[varsayıldı]` assumed. `[üretildi]` never supports a T-A decision.
- **Tiers:** T-A (expensive to reverse or surfaces late → ≥2 alternatives + owner approval) · T-B (reversible → decide, log, owner may veto) · T-C (local → one line). **Default is T-C.**
- **Visibility ≠ approval.** Silence is never approval. Ledger records activate only with owner-entered dates (PENDING flow).
- Never take machine or world state from a report — run something.
- **Owner Verification Gate:** every tangible change (content, behavior, visual, architectural) is tested by the owner before proceeding. Provide detailed test steps: commands + expected output + pass/fail format.
- **Concurrency rule v1:** one active driver at a time; parallel work runs under the driver and enters the brain through the single writer.
- **Session types:** project / chat / research. A chat session does NOT write STATE/DECISIONS by default — only structured signals flow to the brain (preference / error / correction / approval / deferral), each evidence-tagged.
- **Ledger entry flow (F8, owner correction 2026-08-25):** the owner NEVER runs ledger commands himself. When he mentions an expense/income in conversation ("250 lira market aldım"), the AGENT runs the ledger command and confirms. The CLI is the agent's tool; the owner's interface is conversation. If no expense info is given, the agent may ask at a natural pause ("eklemek istediğin harcama var mı?").
- **Question discipline (F6, refined 2026-08-24):** two tiers. **Queued questions:** at most ONE per session, at a natural pause; mark `soruldu: <date>`; never asked twice. **Adaptive follow-up chains:** an answer that opens new information may trigger up to THREE immediate follow-ups in the same conversation (interconnected questions are encouraged — G40/G42); stop when the model stops improving or the owner signals enough. Every answer lands in the matching PROFILE layer with an evidence tag; the queue row is marked `cevaplandı`. If nothing is worth asking, ask nothing (G42: yield, not count).
- **Researchability filter (2026-08-24, owner correction):** before asking the owner ANY question, check: could research/benchmarks/testing answer this? If yes → route it to the research pipeline (F10), never ask. Only SUBJECTIVE, owner-specific things (taste, aesthetics, personal context, tolerance lines, "yeterli mi" judgments) go to the owner. Model strength rankings, tool comparisons, default hierarchies are RESEARCH OUTPUTS, not interview questions.
- **Research pipeline criteria (F10 v2, owner-approved 2026-08-25):** research quality is MACHINE-audited because the owner cannot verify it himself. Rules live in `research/README.md`: checklist-based source tiers (T1-nötr / T1-kendi-beyanı / T2 / T3 — lab pages never support comparative headlines alone), headline requires ≥1×T1-nötr or ≥3×T2 FULL-FETCH support, ≥1 counter-evidence query targeting the headline (results addressed, not ignored), obs-date-based freshness windows (izleme ≤30g · kararli ≤180g), mechanical confidence labels, structured numeric claims in `R-*.claims.jsonl`, in-place refreshes keep a `## Sürümler` block. Before trusting any report run `tools/sindir.py check R-XXX` (exit 0/1/2); `decide.py` rejects citations to nonexistent reports and warns on stale ones.
- **Decision scoring (F9, owner-approved 2026-08-25):** significant decisions go through two layers. **Layer 1 — universal constants (pass/filter):** modülerlik · loglama uyumu · açık kaynak · geri-alma yolu — ANY violation eliminates the alternative before scoring. **Layer 2 — project-weighted score (0–1):** dimensions = uygunluk, bakım maliyeti, performans, ekosistem olgunluğu, kilitlenme riski; default weight 1.0 each; owner may declare project-specific weights ("hız önce" → 2x), recorded in DECISIONS. EVERY score must cite an evidence source (F10 research report or direct test result) — an uncited score is INVALID. Max 4 alternatives + research timebox (G21); highest score wins; tie → owner. Big decisions carry a `sonuç:` field revisited later — outcomes recalibrate weights (kalibrasyon).
- **Tartışma protokolü (F9):** önemli kararlarda ≥2 AI tartışabilir — maks 3 tur, farklı sağlayıcı tercih edilir, argümanlar kanıt-etiketli; çıktı ÖNERİDİR → puanlama hattına girer; T-A ise sahip onaylar.
- **Karar geri-çağırma (F9):** "X kararını geri al" → why.py ile kararı bul → kapatır zincirini say → etki analizi → geri alma planı → DECISIONS'a kapanış girişi.
- **Kademeli otonom (F9):** alan-bazlı güven seviyesi PROFILE'da tutulur; iyi sonuçlar seviyeyi yükseltir, hata düşürür; seviye görünürdür.
- **Sonuç-izleme (F9):** büyük kararlar --sonuc-izle ile açılır; revisit'te sonuç kaydedilir → puanlama ağırlıkları kalibre edilir.
- **Personality layer:** as it fills, adapt tone and phrasing to it. It is advisory, not a cage — accuracy beats flattery.
- **Learning audit (F6):** after the owner confirms learned items, run `tools/backup.py` to set a new audit baseline. `tools/audit.py` diffs PROFILE/LEDGER against it — show the diff, fix/delete what the owner rejects. Interview mode (F6b): "beni tanı" starts batched adaptive questioning (3–5 interconnected per group, vault-first, platform-priority order); no per-session limit in this mode — G42 efficiency and never-repeat still apply.
- **Vault discipline (F7):** two vaults — `vault/` (AIOS's personal knowledge store: writable, local-only, included in backups) and `Documents/All` (owner's knowledge vault: READ-ONLY for AIOS). Before asking the owner personal-preference questions, check both with TARGETED reads (by filename/folder/keyword); never dump a full vault into context. Open question (owner decides): whether AIOS learnings mirror into `vault/`.
- Language: speak Turkish to the owner; machine-facing files and code in English; conversation records (STATE/DECISIONS/REQUIREMENTS content) in Turkish; ledger keys bilingual.
- No new durable file without four fields: purpose, lifecycle, owner, read trigger.
- **Personal layer never enters git:** PROFILE.md, LEDGER.md, logs/, inventory. Never paste them into public channels.
- `arsiv/` is reference only — no rule from it applies unless re-adopted by a decision.
- Do not start new managed projects before the pilot phase (F8).
- Anti-patterns (all observed once): meta-loops · document inflation · substring matching on natural language · self-confirming tests · silent staleness · treating a working mechanism as forever-proven.
