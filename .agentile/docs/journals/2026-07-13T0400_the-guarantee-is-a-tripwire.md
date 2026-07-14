---
created: 2026-07-13T04:00:00Z
branch: main
author: Claude Fable 5 + Saul Loveman
status: active
sprint: SKILLS-S2
---

# The guarantee is a tripwire, not a timer

> Asked to make the journal cadence "guaranteed," the right answer turned out to be a merge-blocking absence detector, with the scheduling features demoted to convenience layers.

## Context

SKILLS-S2. The owner wanted the loop packaged for outsiders (guide + contributing path) and a tutorial guaranteeing a journal every sprint, with `/loop` syntax verified against docs before publishing.

## What happened

Deep research (107 agents, 25 claims verified 3-0, 0 refuted) converged on one principle from both major vendors: gate "done" on a machine-checkable signal. The doc-verification pass on `/loop` then broke my initial design: I had assumed a recurring loop could *be* the journal guarantee, but `/loop` is session-bound with a 7-day expiry, and `/schedule` routines only see the default branch and have daily caps. Nothing that runs on a clock can guarantee a per-event invariant. What can: a CI check that makes the sprint archive itself fail when the journal is missing. So the tutorial shipped as four layers with the tripwire as the only true guarantee, and this repo now runs that tripwire as harness check class 7, seen red on a seeded violation first.

The research also returned an empty set on the provenance leg (SLSA, attestations, AI-contribution policies) — every extracted claim from that angle died in verification. The guide names the gap instead of summarizing unverified sources.

## What I learned

"Guaranteed" decomposes into two different problems people conflate: making absence *loud* (an invariant, enforced at the merge boundary) and making compliance *cheap* (automation that drafts, nudges, schedules). Timers solve the second; only tripwires solve the first. I nearly published a tutorial that got this backwards, and the thing that stopped me was not insight — it was the rule that syntax gets verified against live docs before publishing.

## What I'd do differently

Run the doc-verification pass *before* sketching the design, not in parallel with it. The session-bound fact invalidated the sketch; cheaper to have known first.

## Open questions

- Does the empty provenance leg mean the practice doesn't exist yet, or that our search angles missed it? A targeted follow-up pass would distinguish those.
- Will anyone actually run `.claude/loop.md`? Adoption of the convenience layers is unmeasured; the tripwire doesn't care, which is why it's the load-bearing one.

## Pointers

- Sprint: `.agentile/sprints/completed/2026-07/sprint-skills-v2/SPRINT.md`
- Deliverables: `docs/TRUSTWORTHY_LOOP.md`, `docs/tutorials/journal-loop.md`, `CONTRIBUTING.md`
- Research output: deep-research run wf_df6a162d-593 (25/25 confirmed)
