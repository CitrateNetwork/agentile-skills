---
created: 2026-07-12T20:30:00Z
branch: main
author: Claude Fable 5 + Saul Loveman
status: active
sprint: SKILLS-S0
---

# Sprint SKILLS-S0 — Retrospective

## Outcome

| Field | Value |
|-------|-------|
| **Goal achieved?** | YES |
| **WPs planned / closed** | 4 / 4 |
| **Carry-forward WPs** | none |
| **Closing branch** | `main` at the commit that archives this sprint (CI run 29216243206 green) |

## Metrics delta

| Axis | Start | End | Δ |
|------|-------|-----|----|
| Tests | 0 | 154 (`python3 scripts/validate.py`) | +154 |
| Formal specs | 0 | 0 | 0 (doc repo; none warranted) |
| CI tripwires | 0 | 3 classes (name/dir lint, Rule-12 lint, template integrity ×2 layers) | +3 |
| Frontmatter coverage | 3/3 | 4/4 | +1 |

No axis went down.

## What worked

- **Extracting before writing.** Four parallel explorations pulled the method as *practiced* (rules, templates, voice, marketplace format) before any skill was drafted; every skill claim traces to canon, and nothing had to be retracted on review.
- **The portable/federation split.** Deciding early that 11 skills must work outside the federation and 2 must not forced every methodology skill to shed Citrate-specific paths, which is what makes the marketplace publishable at all.
- **Seeding red before trusting green.** All three tripwire classes were made to fail on purpose before the harness was believed. The seeded template edit tripped two independent layers (lock + skeleton diff) — the layered design earned its keep on day one.

## What didn't work

- **The harness was built last, against the method's own ordering.** The repo existed for a review cycle with zero tripwires — the sprint file said so honestly, but "it's just docs" reasoning caused exactly the deferral the method warns about. Cost: one manual consistency loop that should have been CI from commit one.
- **The initial README documented an install path that didn't exist yet** (`saulbuilds/agentile-skills`; the remote was created under `CitrateNetwork`). By our own claim taxonomy that was UNSUPPORTED at the time of writing. Caught at push time, fixed in `cad16b4`. Cheap here; the habit is not.
- **The kickoff journal briefly contained an invented detail** (a lint catching mismatches that never happened) — caught and corrected before commit, but it is a live demonstration of the compounding-optimism failure mode this whole repo packages.

## What surprised us

- 154 checks fell out of only ~5 check categories — per-file granularity made the count a meaningful ratchet with no extra design.
- The manifest registration landed on `planset/core-beta-wiring` because that branch was checked out in citrate-federation; the method's "one home per topic" had no opinion on *which branch is checked out where*. Cross-repo commits inherit whatever branch state the workspace happens to be in — worth a tripwire or a checklist line someday.

## Carry-forward

| Item | Where it goes | Why deferred |
|------|---------------|--------------|
| PRIVATE→PUBLIC flip for marketplace distribution | backlog (needs Rule-13 ADR + owner sign-off) | Repo works for the team while private; publishing is a separate decision |
| Adversarial review of skill trigger phrases (do descriptions actually fire?) | backlog | Needs usage data from real sessions |

## Decisions ratified mid-sprint

- Templates are vendored copies with a lock + drift tripwire, bending Rule 9 for distribution surfaces — recorded in CLAUDE.md; formal ADR if the pattern recurs elsewhere.
- Remote lives under `CitrateNetwork` (federation convention), not `saulbuilds`.

## Action items for next sprint

- [ ] Owner: decide public/private for the marketplace; if public, write the Rule-13 ADR
- [ ] Run a reviewer pass (e.g. workflow-skill-reviewer) over all 13 skills and fold findings into a 0.1.1

## Notes

Journal for this sprint: `.agentile/docs/journals/2026-07-12T1200_packaging-the-method.md`. Essay considered: the vendored-templates/Rule-9 tension is a candidate but hasn't recurred enough to argue from; declined this sprint. Case study considered: none warranted — no break/fix incident; the seeded reds were deliberate.
