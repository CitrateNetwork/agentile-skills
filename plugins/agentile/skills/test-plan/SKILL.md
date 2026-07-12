---
name: test-plan
description: Planning the testing framework for a sprint or work package before implementation. Use at sprint kickoff, when choosing test harnesses (unit, integration, property, fuzz, E2E, formal), when snapshotting the coverage baseline, when designing tripwires for a finding class, or when someone asks "how will we test this?"
metadata:
  version: "0.1.0"
---

# Test planning

Under Agentile the test plan is written before the code, because tests are the referee: they are the mechanism that converts "the agent says it works" into "the repo proves it works." A test plan has three jobs — snapshot the baseline, choose the harness, and design the tripwires.

## 1. Snapshot the baseline (day 0, non-negotiable)

Record the four ratchet axes in `.agentile/coverage/BASELINE.md` (and quote them in the sprint file's Test Baseline table):

| Axis | What it counts | Ratchet rule |
|---|---|---|
| **Tests** | canonical test-command count | Never decreases within a sprint (Rule 2). Removing a test requires an ADR. |
| **Formal specs** | TLA+/property modules | Never decreases. |
| **CI tripwires** | grep/lint/assertion gates in CI | Never decreases. |
| **Frontmatter coverage** | docs with Rule-12 frontmatter | Never decreases. |

Record the *canonical command* for each count once (e.g. `cargo test --workspace 2>&1 | tail -1`), so every future session counts the same way. A baseline captured with a different command is not a baseline; it's an argument waiting to happen.

## 2. Choose the harness per WP

Method order for each WP — skip a step only with a written reason in the WP block:

1. **TLA+ / formal spec** — if the WP touches a state machine, consensus path, concurrency seam, or cross-actor invariant. Model first; TLC-green before implementation. Formal specs have caught spec bugs that all downstream tests inherited.
2. **BDD / Gherkin** — behavior with branches, taken from the feature spec (`agentile:feature-spec`).
3. **Property-based tests** — anything with serialization, parsing, validation, arithmetic, or roundtrip invariants. One property test outranks twenty examples.
4. **Unit tests** — pure logic, edge cases.
5. **Integration tests** — the ones that fail if a real data source is disconnected. Every "real backend" claim needs at least one (this is what closes the Real-Backend loophole).
6. **Fuzz harnesses** — parsers, decoders, anything consuming untrusted bytes.
7. **E2E / live-path tests** — a broadcast against the real system. *Compiles* and *tested* are claims about the code's shape; only exercising the live path is a claim about behavior. Plan at least one live-path check for anything user-facing.

## 3. Design the tripwires

A tripwire is a cheap, permanent CI check that catches a *class* of defect, not an instance. When the plan anticipates a risk (or a past incident maps onto this work), add the tripwire to the plan up front:

- grep gates: `TODO|FIXME|unimplemented!` in production paths; `.unwrap()` in UI crates
- naming gates: test-only types (`Stub*`, `Fake*`, `Mock*`) outside `#[cfg(test)]`
- count gates: test/spec/tripwire counts vs. baseline (the ratchet itself)
- pinned-vector gates: expected values earned from the real system, with a documented re-earning procedure for when the world legitimately changes (see `agentile:refactor-mutate`)

**Rule for critical findings:** every CRITICAL/HIGH bug fixed gets a tripwire for its class, not just a regression test for its instance.

## 4. Verify the referee is alive

A test plan that assumes CI is running is incomplete. Plan the meta-checks:

- [ ] CI actually executes on every push to main (check the last run's timestamp, not the badge)
- [ ] The sprint's exit criteria say "linked CI run green", never "tests were run locally"
- [ ] If CI will be down (billing, migration), the plan names the manual verification substitute and its cadence

The bound on how long a checkably-false claim survives is exactly the length of your verification blackout. Keep the blackout at zero.

## Test-plan output

The plan lands in the sprint file (Method + Test Baseline sections) plus, for larger programs, planset doc `03_TLA_SPECS.md` / `04_FEATURES_BDD.md`. For each WP it answers:

- Which harness levels apply, and why the skipped ones don't
- Which failing tests will be written first (names, not vibes — `tests/x.rs::test_y`)
- Which tripwires land with the WP
- What the live-path verification is
- What the baseline counts are and what they must be at close

Then hand off to `agentile:red-green` to write the failing tests.
