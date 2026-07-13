---
name: projects
description: Handling projects inside the CitrateNetwork federation. Use when starting new work in a federation repo, adding a cross-repo dependency, bumping manifest pins, writing a handoff or work order, dispatching parallel agent lanes, creating a new federation repo, or closing work that spans repos.
metadata:
  version: "0.1.0"
---

# Running projects in the federation

Every project in the federation is an Agentile project (use the `agentile` plugin for the method itself). This skill covers what the federation adds on top: the manifest, drift discipline, handoffs, dispatch, and repo lifecycle.

## Starting work

1. **Find the owning repo** (`citrate-federation:navigate`). One source of truth per topic (Rule 9), applied to work: one *coordinating* sprint per piece of work — if it spans repos, the other repos get linked WPs, not clone sprints.
2. **Check what's already in flight:** `citrate-federation/agentile/CURRENT.md` + the repo's `.agentile/sprints/active/`. Don't open a second sprint for work an active one covers.
3. **Kick off per Agentile** (`agentile` master skill): sprint directory, baseline snapshot, WPs with data-sourced criteria.
4. **Register it:** add/update the row in `CURRENT.md` so the federation-level view stays true.
5. **Work red-test-first, keep tests monotone, log daily in the sprint file.** Status lives there — not in chat (Rule 4).

## Cross-repo dependencies (Rules 11 & 12 — the order matters)

`citrate-federation/manifest.toml` is the single source of truth for which SHA of each repo is current. Per-repo divergence loses to the manifest.

**Adding a dependency on another repo:**
1. **First** add the `[[drift]]` entry to `manifest.toml`:
   ```toml
   [[drift]]
   consumer = "citrate-native"
   dep_repo = "citrate-chain"
   file = "Cargo.toml"
   pin_field = "citrate-wallet-core"   # the dependency name in the consumer's file whose rev pin drift-check verifies
   ```
2. **Then** add the dependency to Cargo.toml / package.json, pinned to the manifest's `rev` for that repo.

**Shipping upstream changes to consumers:**
1. Land and merge the upstream change; note the new SHA.
2. Bump that repo's `rev` in `manifest.toml` (annotate the rev comment with what closed — existing entries show the register).
3. Run `citrate-federation/scripts/pin-bump.sh <repo>` — opens PRs in every consumer.
4. Merge consumer PRs when their CI is green.
5. Nightly `drift-check.sh` verifies propagation; a red drift-check is a stop-the-line signal, not a warning.

Never "fix" drift by pulling a consumer to a branch tip — fetch the exact pinned object and detach onto it (fail closed).

## Handoffs (session-to-session and human work orders)

Handoffs live in `citrate-labs/handoffs/`, named `<TOPIC>_<YYYY-MM-DD>.md`, with Rule-12 frontmatter (canonical Rule 5) plus `audience:`. Structure that works (see `ALF_PORTAL_DEVOPS_HANDOFF_2026-07-07.md` as the exemplar):

1. **One-line ask** — what the recipient is being asked to stand up, in one sentence.
2. **Blockers table** — which downstream work each task gates (`D-1 blocks ALF-S1 …`).
3. **Numbered operator tasks** — discrete, ordered, each with exact steps (files to edit, env vars, commands) and a **Verify:** line (a command whose output proves the task done).
4. **Coordination seams** — the interfaces between this work and others', stated as contracts.

Handoffs are *dated context, not truth* — a handoff reader verifies against code/manifest before acting on facts inside it; a handoff writer dates every claim.

## Parallel agent dispatch (multi-lane work)

For work too big for one context, dispatch lanes (exemplar: `handoffs/AGENT_HANDOFFS_2026-06-11/`):

- `00_README.md` — the dispatch table: one lane per agent, each lane owns named repos. Lanes own **disjoint** write-surfaces; overlap is a design error.
- **"Verified federation state"** section — facts checked live at dispatch time, marked *do not re-litigate*, so lanes don't burn context re-deriving them.
- **Shared rules of engagement** — red-test-first, test monotonicity, security sign-off on auth/keys/money paths before deploy.
- **Coordination seams table** — producer lane, consumer lane, and the interface contract for every cross-lane dependency. These are the *only* permitted cross-lane couplings.
- One `AGENT_<X>_<LANE>.md` brief per lane: scope, repos, sprint IDs, exit criteria.

## Creating a new federation repo

- [ ] Create the repo under `citrate-labs/` (independent git repo) with remote `github.com:CitrateNetwork/<name>.git`
- [ ] Scaffold `.agentile/` (the `agentile` skeleton repo's `bootstrap.sh` does this): `AGENT_ENTRY.md` with tier, `CLAUDE.md`, sprints/, templates
- [ ] Decide the tier honestly — T1 if it touches consensus, contracts, money, keys, identity, or partner-facing surfaces
- [ ] Register in `citrate-federation/manifest.toml`: `[repos.<name>]` with tier, role, visibility, `rev` = initial commit SHA, `default_branch`, `consumes_repos`/`consumed_by`, `publishes`, `audit_tier`
- [ ] Add the row to `citrate-labs/onboarding/FEDERATION_MAP.md` in the right concern group
- [ ] Visibility starts `private`; PRIVATE→PUBLIC on T1 requires federation-lead sign-off + ADR (Rule 13)

## Closing cross-repo work

- Exit criteria include: CI green **on every affected repo**, manifest pins bumped and propagated, drift-check green.
- Close the coordinating sprint per the Agentile ceremony (`agentile:retro`), then update `CURRENT.md`.
- If the work changed how the federation itself operates, that's a case-study or essay trigger — and possibly a FEDERATION_MAP/AGENTS.md update so the *map* stays a first-class artifact.

## Federation-specific cautions

- The one-human bus factor is real: write handoffs as if the reader has zero shared memory with you, because the next reader (human or agent) won't.
- Destructive git operations need explicit approval (Rule 10) — this includes anything in `citrate-journals/`, which has no remote and therefore no undo.
- Audits and closed sprints are immutable (Rule 3); federation history is an evidence chain, and its value is the unbroken chain.
