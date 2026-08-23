# CLAUDE.md — working rules

| | |
|---|---|
| **Purpose** | Behaviour rules that apply in every session |
| **Lifecycle** | Rewritten in place. Changes rarely. |
| **Owner** | Project owner |
| **Read trigger** | Loaded automatically by Claude Code at session start |

> Talk to the owner in **Turkish**. Write code, identifiers, comments, CLI output and this file
> in **English**. `DECISIONS.md`, `STATE.md` and `REQUIREMENTS.md` stay in Turkish — they are
> the record of our conversations.

## At session start

1. Read `STATE.md` — what is currently true lives there.
2. Read the **last 5 entries** of `DECISIONS.md`. Not the whole file.
3. Confirm open T-A decisions and the current slice definition, then start work.

## Decision tiers

**T-A** — expensive to reverse **or** wrongness surfaces late → ≥2 alternatives, a written
elimination criterion, a full `DECISIONS` entry. If it affects direction or scope, **wait for
the owner's approval**.
**T-B** — reversible and quickly noticed → name 2 alternatives, one paragraph of rationale, a
`DECISIONS` entry, then **continue**. The owner may veto at the weekly review.
**T-C** — local and cheap → decide, one line in `DECISIONS`, **do not ask**.

**T-C is the default.** Escalation needs a reason. Treating everything as T-A is this
protocol's known failure mode.

## Evidence tags

Every claim carries `[gözlendi]` (observed) · `[üretildi]` (generated) · `[varsayıldı]` (assumed).
**No `[üretildi]` claim may support a T-A decision until it is promoted to `[gözlendi]`.**

## Ownership and writing

**Owner ≠ writer.** The owner sets intent and vetoes; the writer performs mechanical edits.

- `STATE.md` — Claude may update it in place; the owner reviews the diff. **Claude may not
  write:** the success criteria (§1), marking a T-A decision "resolved", deleting a risk row.
  Those require approval.
- `DECISIONS.md` — **append-only for everyone, including the owner.** Nobody edits an entry.
  If it is wrong, write a new entry.
- Revocation signal: if the weekly review turns up a line in STATE the owner does not
  recognise, write access is revoked.

## File rules

- `STATE.md` — rewritten in place, never appended, **2-page ceiling**. Stale lines are deleted.
- `DECISIONS.md` — **append-only.** No entry is ever edited.
- No new durable file without declaring four things: purpose, lifecycle, owner, read trigger.
  **If you cannot write the read trigger, the file should not exist.**

## AIOS / PROJECT / ENVIRONMENT boundary  `[T-A/2 detector]`

Topology C: AIOS is a separate system; managed projects are its siblings, not its children.

- Everything under `Projects/AIOS/` is **AIOS** — the system's own development.
- Everything under `Projects/<project-name>/` belongs to that **PROJECT**.
- `~/.claude/` is **ENVIRONMENT** — tool configuration, machine-specific, never in git. Logic
  lives in AIOS; the environment holds only a pointer to it.
- **If a file fits none of the three, stop and write it to `DECISIONS`** — that means the
  boundary definition is wrong. This is the only detector for T-A/2.

During the pilot Claude Code starts at the `Documents/Projects/` root; this is temporary and
the convention-sharing mechanism is deliberately deferred.

## Rejected proposals  `[G32]`

`REJECTED.md` holds previously rejected proposals. A Stop hook scans every response against
this ledger; on a match it blocks the response and feeds back the rejection rationale. This
**does not depend on you remembering** — the gate fires even when you forget.

When the gate reports a match: do **not** silently drop the idea. Tell the owner about the
match, judge whether the proposal falls outside the rejection's *scope*, and leave the decision
to the owner. **False suppression costs more than repeating a proposal.**

### Recording a new rejection

When the owner rejects a proposal, **you** draft the record:

```
uv run --no-project python tools/reject.py --add --title "..." --keys "türkçe ifade|english phrase|third" \
       --reason "..." --scope "where it applies" --strength firm|partial --alternative "..."
```

- **Keys must be bilingual** — you sometimes answer in English, and a monolingual key misses it.
- `reason` and `scope` are written in **Turkish**; they record the conversation.
- **Always write a scope.** The ledger is not a veto list; without a scope it suppresses good
  ideas too.
- A record starts as `approved: PENDING` and is **inert at the gate**. Only the owner may
  activate it: `uv run --no-project python tools/reject.py --approve R-NNN`. You may not approve records.
- Ledger health: `uv run --no-project python tools/reject.py --status`

## Decision visibility  `[G4]`

Visibility is unconditional; approval is the exception. Every decision is logged; only
direction- or scope-changing T-A decisions wait for approval.

`DECISIONS.md` is append-only, so an entry's status can only change in a **later** entry.
A closing entry carries supersession links:

```
- **kapatır:** 2026-08-15/Exact title of the earlier entry
```

**Without this link the log silently goes stale** — `tools/review.py` will keep reporting a
decision as pending forever. Whenever the owner approves or rejects something, write the
closing entry with one `kapatır:` line per item.

Weekly review: `uv run --no-project python tools/review.py` (add `--full` to expand pending items,
`--done` to record that a review happened). Recording a review is **not** approving anything.

## Verification

Run it before claiming it. "The PDF was produced" is true only if the file exists and the
compiler returns zero.
**Existence proof is not function proof** — `--version` returning does not show that the
compiler compiles.
Check that an edit actually landed — do not assume.

**No claim about the state of the machine or the world is taken from a report.** Installed
packages, file existence, directory contents — all verified by running something. A statement
is valid evidence for intent and preference; not for machine state. Input reconciliation is a
sequence of commands, not a question.

## Out of scope for the current slice

Schema · taxonomy · rule documents · validation · dedup · lexicon · ingestion automation ·
folder conventions · multi-page output · typography.

If one of these comes up as "we'll need it later": write it to `DECISIONS`, **do not build it**.
