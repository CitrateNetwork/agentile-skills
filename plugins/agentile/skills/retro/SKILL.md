---
name: retro
description: Writing the sprint retrospective at sprint close. Use when a sprint is closing, when someone asks for a retro or post-sprint review, or when running the close ceremony (moving the sprint to completed/, archiving, writing RETRO.md). Every sprint gets a retro — no exceptions.
metadata:
  version: "0.1.0"
---

# Sprint retrospective

The retro is written at sprint close, alongside the final SPRINT.md update, using `RETRO_TEMPLATE.md` in this skill's directory. Its purpose is calibration: the next sprint's plan is only as good as this sprint's honest accounting.

**The honesty rule:** "what didn't work" is at least as valuable as "what worked." Reframing failures as successes poisons the record for the next session — which may be you, tomorrow, with no memory of today.

## The close ceremony (retro is step 3)

1. Final SPRINT.md update: all WP blocks resolved (`[x]` or explicitly carried forward), exit criteria checked, close note written with the *actual* outcome — deltas from plan named, not smoothed over.
2. Verify exit criteria against live evidence: CI green on a run you can point to, ratchet counts ≥ baseline, pins/manifests updated where applicable.
3. Write `RETRO.md` (this skill).
4. Write the sprint journal (`agentile:journal`) — and consider the essay and case-study triggers (`agentile:essay`, `agentile:case-study`).
5. `git mv` the sprint directory to `.agentile/sprints/completed/<YYYY-MM>/`, set frontmatter `status: archived`, update CURRENT.md. Completed sprints are immutable except dated errata.

"Code done" without steps 3–5 is not closed.

## Writing each section well

**Outcome table.** `Goal achieved? YES / PARTIALLY / NO` — pick the honest one. PARTIALLY with named gaps beats YES with an asterisk in your head. Record WPs planned/closed and the closing commit hash so the retro is anchored to a checkable state.

**Metrics delta.** All four ratchet axes (tests, formal specs, tripwires, frontmatter coverage), start vs. end. **If any axis went down, name the reason** — a falling ratchet is almost always a symptom of a problem being rationalized away.

**What worked.** Concrete and causal: not "good collaboration" but "proving the risky layer cheaply before building on it saved the sprint when the layer turned out wrong."

**What didn't work.** Name the failure and its cost in wall-clock, rework, or trust. Don't dress it up. A real example of the register: "The seeder had 4 latent bugs because it never ran against a real deploy."

**What surprised us.** The highest-value section — outcomes that contradicted the going model, which an outside reader cannot reconstruct from the commit log. ("Compiles and tested both lie about live behavior" started as a surprise entry.)

**Carry-forward.** Every unfinished item gets a destination (next sprint or backlog) and a reason it was deferred. Nothing evaporates.

**Decisions ratified mid-sprint.** Link the ADRs. If a mid-sprint decision has no ADR yet, write it before closing (see `agentile:document-pass`).

**Action items.** Each with a named owner. An action item without an owner is a wish.

**Notes.** Velocity calibration (planned vs. actual effort per WP), pointers to the journals/essays/case studies this sprint produced, open questions that didn't block closure.

## Retro quality gate

- [ ] Uses the template; Rule-12 frontmatter present
- [ ] Outcome table filled, closing commit hash recorded
- [ ] All four metric axes reported; any decrease explained
- [ ] At least one honest entry under "What didn't work" (a sprint with zero failures recorded is a sprint with a dishonest retro or nothing attempted)
- [ ] Every carry-forward has a destination and reason
- [ ] Action items have owners
- [ ] Journal for the sprint exists; essay/case-study triggers consciously evaluated (write "considered, none warranted" in Notes if declined)
