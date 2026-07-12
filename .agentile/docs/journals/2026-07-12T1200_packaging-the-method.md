---
created: 2026-07-12T12:00:00Z
branch: main
author: Claude Fable 5 + Saul Loveman
status: active
sprint: SKILLS-S0
---

# Packaging the method without flattering it

> Turning a lived methodology into thirteen installable skills forced a distinction we hadn't needed before: which parts of Agentile are the method, and which parts are just how one federation happens to apply it.

## Context

SKILLS-S0 kickoff session. The ask: package the whole Agentile workflow — spec, planset, test plan, red-green, refactor/mutate, document, retro, journal/essay/case-study — as a marketplace, plus a federation-navigation skill, so employees and fresh agent sessions arrive fluent instead of re-deriving the method at full cost.

## What happened

Four parallel explorations extracted the method as practiced: the 13 rules and sprint/WP protocol, the planset and gates conventions, the journal/essay/case-study corpus and its voice, and the existing marketplace formats to match. The extraction surfaced a clean seam: eleven skills are portable (the method), two are Citrate-specific (the map). That seam became the two-plugin split.

The templates question resolved against instinct. Rule 9 says link, don't copy — but a marketplace install lands outside the federation, where links dangle. The templates are vendored copies with a CLAUDE.md rule and a planned CI tripwire (WP-3) to keep them honest against the skeleton source. Rule 9 bends for distribution surfaces; the mitigation is a drift detector, which is the same answer the federation gave to cross-repo pins.

The repo ships in violation of its own method, and says so: zero tests, zero tripwires at initial commit. The sprint file records it as WP-3 rather than rounding "packaged" up to "done."

## What I learned

Writing the skills was mostly *deletion*. The corpus says everything three times in three registers (rules doc, workflow doc, essays); a skill has to say it once, at the altitude an agent can act on mid-task. The test that worked: every section had to answer "what would an agent do differently in the next ten minutes for having read this?" — anything that didn't was history, and history belongs in the essays, which the skills point to but don't quote at length.

## What I'd do differently

Write WP-3 (the validation harness) *first*, red-test-style. The name/directory consistency check that should be a CI lint was instead a one-off shell loop run by hand at the end (it passed, 13/13 — but a pass that lives in scrollback is not a ratchet). The method predicted this; I deferred it anyway because "it's just docs." It is never just docs.

## Open questions

- Should skill descriptions be A/B'd against real trigger behavior — do the "Use when" phrases actually fire in practice?
- Does the `essay` skill's "attempt every sprint" cadence survive contact with sprints that are pure grind? (The rule says yes, with "considered, none warranted" as a valid outcome — watch whether that escape valve gets overused.)

## Pointers

- Sprint: `.agentile/sprints/active/sprint-skills-v0/SPRINT.md`
- Canon extracted from: `citrate-federation/agentile/rules/CORE_RULES.md`, `docs/AGENTILE_WORKFLOW.md`, `agentile/.agentile/templates/`, `docs/essays/agentile-history/`
