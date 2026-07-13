---
created: 2026-07-12T22:30:00Z
branch: main
author: Claude Fable 5 + Saul Loveman
status: active
sprint: SKILLS-S1
---

# The reviewers were the referee

> A review pass by agents who didn't write the skills found the one thing the author could never have found: the errors the author's own research put there.

## Context

SKILLS-S1, same day as S0. Five reviewer agents over the 13 skills for a 0.1.1, with a hard constraint: flag structure and consistency, don't relitigate the method.

## What happened

The reviewers returned 23 real findings and two skills fully clean. Three clusters mattered. First, SKILL-vs-template contradictions: the prose skills and the vendored templates disagreed on ADR naming, sprint-directory naming, and where status updates live — because the skills were written from an extracted method report while the templates were copied from the skeleton, and the two sources encode different eras of the same method. Second, a broken canonical path (`agentile/rules/` for what is really `.agentile/rules/`) shipped in five places, inherited verbatim from the extraction report. Third, the federation plugin's `[[drift]]` example taught a `pin_field` value that drift-check cannot resolve — a copyable example that would have produced broken control-plane TOML.

Both HIGH findings were verified against the live workspace before editing; both held. Two findings were rejected with written reasons (the "13 rules" heading is canon-faithful over rows 0–13; template edits are upstream skeleton work, not ours). Thirty-five edits, version bump, harness 164/164.

## What I learned

Errors inherited from research are invisible to review by the researcher. I extracted the wrong rules path, then wrote it into five files, then "reviewed" those files while holding the same false belief. The independent reviewers didn't know the path either — but they *checked*, because checking cited paths was in their brief. The lesson generalizes: the reviewer's value here wasn't intelligence, it was unshared assumptions plus an instruction to verify citations.

## What I'd do differently

Put "every cited path must be read, not recalled" in the original writing pass, not just the review brief. Also: cross-check prose against vendored templates *at authoring time* — the contradiction class was mechanical and predictable.

## Open questions

- Should the harness verify cited workspace paths in the federation plugin? (Retro action item; it makes CI depend on sibling-checkout layout, which needs a skip-if-absent design like the skeleton diff.)
- The archive-vs-current rule numbering will keep biting newcomers. Is a numbering note enough, or does the canon eventually need a concordance table?

## Pointers

- Sprint: `.agentile/sprints/completed/2026-07/sprint-skills-v1/SPRINT.md`
- Predecessor journal: `2026-07-12T1200_packaging-the-method.md`
