---
created: 2026-07-12T00:00:00Z
branch: main
author: Saul Loveman + Claude Fable 5
status: active
sprint: SKILLS-S0
---

# Sprint SKILLS-S0: Package Agentile as a skills marketplace

## Sprint Metadata

| Field | Value |
|-------|-------|
| **Sprint ID** | SKILLS-S0 |
| **Sprint Name** | Package Agentile as a skills marketplace |
| **Goal** | Any agent that installs the `agentile` plugin can run the full method (spec → planset → test-plan → red-green → refactor-mutate → document → retro → journal/essay/case-study) without reading the federation. |
| **Branch** | `main` |
| **Start Date** | 2026-07-12 |
| **End Date (target)** | 2026-07-19 |
| **Status** | `IN PROGRESS` |
| **Planset** | — (single-sprint scope; planset not warranted) |
| **Predecessors** | `agentile` skeleton repo (templates), FWA remediation (rules canon) |

## Why this sprint

The method lives in the federation's heads and files; employees and fresh agent sessions re-derive it at full cost every time. Packaging it as installable skills makes fluency the default instead of the achievement.

## Deliverables

- `.claude-plugin/marketplace.json` + 2 plugins (`agentile`, `citrate-federation`)
- 13 SKILL.md files with vendored canonical templates
- Tier-1 registration: `manifest.toml` row + FEDERATION_MAP row
- This repo's own `.agentile/` scaffold (dogfood)

## Test Baseline (start of sprint)

| Metric | Count | Captured | Canonical command |
|--------|-------|----------|-------------------|
| **Tests** | 0 | 2026-07-12 | none yet — see WP-3 (validation harness is the open follow-up) |
| **Formal specs** | 0 | 2026-07-12 | n/a (doc repo) |
| **CI tripwires** | 0 | 2026-07-12 | none yet — WP-3 |
| **Frontmatter coverage** | 3/3 | 2026-07-12 | `grep -rL '^---' .agentile --include='*.md'` |

## Work Packages

### WP-1: Marketplace structure + methodology plugin (11 skills)

| Field | Value |
|-------|-------|
| **Status** | `[x] COMPLETE` |
| **Estimated effort** | L |
| **Commit(s)** | initial commit |

**Scope:** marketplace.json, plugin.json, and SKILL.md for: agentile (master), feature-spec, planset, test-plan, red-green, refactor-mutate, document-pass, retro, journal, essay, case-study. Templates vendored from `agentile/.agentile/templates/`.

**Acceptance Criteria**

- [x] Every skill description is a trigger condition ("Use when…") — verified by read-through of all 13 frontmatter blocks
- [x] Templates byte-identical to skeleton source — data source: `agentile/.agentile/templates/`, copied with `cp`
- [x] Method claims traceable to canon (CORE_RULES.md, AGENTILE_WORKFLOW.md, audit standard) — no invented rules

### WP-2: Federation plugin (navigate, projects)

| Field | Value |
|-------|-------|
| **Status** | `[x] COMPLETE` |
| **Estimated effort** | M |
| **Commit(s)** | initial commit |

**Scope:** orientation sequence, truth hierarchy, tier semantics, manifest/drift discipline, handoff + dispatch formats, new-repo checklist.

**Acceptance Criteria**

- [x] Every file path cited in the skills exists in the federation — data sources: `onboarding/FEDERATION_MAP.md`, `citrate-federation/manifest.toml`, `handoffs/`
- [x] Truth hierarchy matches `onboarding/AGENTS.md` ordering

### WP-3: Validation harness

| Field | Value |
|-------|-------|
| **Status** | `[x] COMPLETE` |
| **Estimated effort** | M |
| **Commit(s)** | see close note |

**Scope:** CI that validates marketplace.json/plugin.json against schema, lints SKILL.md frontmatter (name matches dir, description contains a trigger phrase), and diffs vendored templates against the skeleton source. This is the repo's first ratchet.

**Acceptance Criteria**

- [x] `marketplace.json` + both `plugin.json` files schema-validated in CI — data source: this repo's `.claude-plugin/` files, via `scripts/validate.py` + `.github/workflows/validate.yml`
- [x] Frontmatter lint fails on any SKILL.md whose `name` ≠ directory name — data source: `plugins/**/skills/*/SKILL.md`; seen red 2026-07-12 (seeded `retro`→`retrospective` mismatch, caught)
- [x] Template-drift tripwire fails when a vendored `*_TEMPLATE.md` differs from `../agentile/.agentile/templates/` — data source: `templates.lock` (sha256, works in CI) + byte-diff vs skeleton (local); seen red 2026-07-12 (seeded in-place edit, caught by both layers)
- [x] Rule-12 frontmatter lint on all `.agentile/**/*.md` — seen red 2026-07-12 (seeded missing `branch` field, caught)

**Tests added:** `scripts/validate.py` — 154 checks; canonical command `python3 scripts/validate.py`; each tripwire class demonstrated red then restored green.

### WP-4: Tier-1 registration

| Field | Value |
|-------|-------|
| **Status** | `[x] COMPLETE` |
| **Estimated effort** | S |

**Acceptance Criteria**

- [x] `[repos.agentile-skills]` in `citrate-federation/manifest.toml` with initial-commit rev — committed `4d1b677` on `planset/core-beta-wiring`, pushed (owner-reviewed 2026-07-12; lands on main via that branch's merge)
- [x] Row in `onboarding/FEDERATION_MAP.md` — committed `8b67eb5` on citrate-labs `main`, pushed
- [x] GitHub remote created and pushed — `https://github.com/CitrateNetwork/agentile-skills` (private, Rule 13), `main` at `cad16b4`

## Dependencies

| Dependency | Status | Impact if blocked |
|------------|--------|-------------------|
| GitHub repo creation (owner action) | Blocked on human | WP-4 push; marketplace installability |

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Skill text drifts from method canon over time | Med | High | WP-3 template-drift tripwire; CLAUDE.md rule |
| Descriptions too vague to trigger | Low | Med | Trigger-phrase lint in WP-3 |

## Daily updates

- 2026-07-12 — kickoff. WP-1 and WP-2 written and closed in one session (13 skills, 7 vendored templates). WP-4 registration edits staged in citrate-federation + onboarding, uncommitted pending review. WP-3 (validation harness) is the open work: the repo currently has zero tripwires, which is an honest violation of its own method until closed.
- 2026-07-12 (later) — owner reviewed. WP-4 closed: manifest commit `4d1b677`, map commit `8b67eb5`, repo pushed to CitrateNetwork/agentile-skills. WP-3 closed: `scripts/validate.py` (154 checks) + `validate.yml` CI + `templates.lock`; all three tripwire classes seeded red and restored green. Awaiting first CI run for sprint close.

## Notes

The repo ships with tests=0, tripwires=0 — the method says that's not done, and the sprint file says so out loud rather than hiding it. WP-3 is the difference between "packaged the method" and "practices it."
