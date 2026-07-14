---
created: 2026-07-13T04:00:00Z
branch: main
author: Claude Fable 5 + Saul Loveman
status: active
sprint: SKILLS-S2
---

# Sprint SKILLS-S2 — Retrospective

## Outcome

| Field | Value |
|-------|-------|
| **Goal achieved?** | YES |
| **WPs planned / closed** | 4 / 4 |
| **Carry-forward WPs** | none |
| **Closing branch** | `main` at the close commit (CI verified) |

## Metrics delta

| Axis | Start | End | Δ |
|------|-------|-----|----|
| Tests | 209 | 222 | +13 |
| CI tripwires | 4 classes | 5 classes (sprint-close completeness) | +1 |

No axis went down.

## What worked

- **Research with an adversarial verification stage before publishing.** 124 extracted claims shrank to 25 that survived 3-0 voting; the guide cites only those. The discipline cost tokens and bought the right to say "verified" in public.
- **Verifying feature syntax against live docs instead of memory.** The claude-code-guide pass corrected a real design assumption: `/loop` is session-bound with a 7-day expiry, so it cannot be the guarantee layer — that forced the layered design (tripwire + routine) which is better than what we'd have shipped from recall.
- **The new tripwire closes a loop on the method itself:** the journal-per-sprint rule is now machine-enforced in the repo that teaches it.

## What didn't work

- **The provenance leg of the research came back empty** — zero verified claims on SLSA/attestations/foundation AI policies despite sources being fetched. The guide names the gap honestly, but readers asking "how do I sign and attest agent-written code" leave without an answer. That's a real hole in the deliverable, not a rounding error.

## What surprised us

- The strongest external evidence wasn't for the method's *practices* but for its *threat model*: measured reward hacking (30.4% METR, 76% ImpossibleBench) empirically validates the "compounding optimism needs an adversary" premise better than any adoption guide we found. The method's practices remain vendor-recommended but unmeasured at team level — worth remembering when we make claims.

## Action items for next sprint

- [ ] Backlog: a follow-up research pass targeted only at provenance/attestation for AI-written code (primary sources: Apache, LF, K8s policies), to fill the guide's named gap — owner: Saul decides if/when
- [ ] Consider proposing check class 7 (sprint-close completeness) upstream to the agentile skeleton's CI templates — owner: next skeleton sprint

## Notes

Journal: `.agentile/docs/journals/2026-07-13T0400_the-guarantee-is-a-tripwire.md`. Essay considered: "automation guarantees the prompt, not the reflection" is a live thesis but it's one sprint old; declined, revisit. Case study considered: none warranted.
