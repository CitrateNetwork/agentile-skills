---
created: 2026-07-12T22:30:00Z
branch: main
author: Claude Fable 5 + Saul Loveman
status: active
sprint: SKILLS-S1
---

# Sprint SKILLS-S1 — Retrospective

## Outcome

| Field | Value |
|-------|-------|
| **Goal achieved?** | YES |
| **WPs planned / closed** | 2 / 2 |
| **Carry-forward WPs** | none (one upstream-skeleton item, see sprint Notes) |
| **Closing branch** | `main` at the 0.1.1 commit (CI verified at close) |

## Metrics delta

| Axis | Start | End | Δ |
|------|-------|-----|----|
| Tests | 159 | 164 | +5 |
| CI tripwires | 3 classes | 3 classes | 0 |
| Frontmatter coverage | all | all | 0 |

No axis went down. (+5 is the harness counting this sprint's own docs — the ratchet feeding itself.)

## What worked

- **Independent reviewers with an explicit "don't touch the method" constraint.** All 23 findings were structure/consistency/reference defects, zero attempts to relitigate the methodology — the constraint in the prompt did that, not luck.
- **Verifying HIGH findings before editing.** Both federation HIGHs (rules path, `pin_field` shape) were re-checked against the live workspace before any edit. Both held, but the check cost one command and would have caught a hallucinated finding.
- **The harness as a regression net for the review pass itself:** 35 edits across 16 files, and one run proved no description lost its trigger phrase, no name drifted from its directory, no version mismatch.

## What didn't work

- **The 0.1.0 skills contradicted their own vendored templates in four places** (ADR naming, sprint-dir naming, journal status destination, missing template sections). Root cause: the skills were written from the *extracted* method report, the templates were copied from the skeleton, and nothing cross-checked prose against templates before 0.1.0 shipped. The reviewers were the first cross-check — one sprint late.
- **A broken canonical path (`agentile/rules/` vs `.agentile/rules/`) shipped in 5 places**, including the repo's own CLAUDE.md. The harness validates structure, not the truth of cited paths — a class gap, noted below.

## What surprised us

- The archive-vs-current rule numbering ("Rule 12 frontmatter" is canonically Rule 5) is a live trap the corpus itself carries; two reviewers found it independently from opposite directions. The fix was a numbering note, not a renumbering — canon keeps its scar tissue.
- The wrong rules path existed because the *extraction report* that seeded the skills contained it; errors inherited from research survive review-by-the-same-author indefinitely. Independent eyes were the only thing that caught it.

## Action items for next sprint

- [ ] Consider a harness check class: cited workspace paths in federation-plugin skills must exist (would have caught the HIGH pre-ship) — owner: next skills sprint
- [ ] Upstream skeleton template improvements + re-vendor (see SKILLS-S1 sprint Notes carry-forward) — owner: Saul / skeleton repo sprint

## Notes

Journal: `.agentile/docs/journals/2026-07-12T2230_the-reviewers-were-the-referee.md`. Essay considered: "errors inherited from research survive same-author review" is a real candidate but rests on n=1 incident; declined, revisit if it recurs. Case study considered: none warranted — no production break; findings were pre-ship defects caught by process working as designed.
