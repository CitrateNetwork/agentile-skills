---
name: refactor-mutate
description: Post-green hardening — refactoring code and mutation-testing the suite. Use after a WP goes green, when cleaning up an implementation, when proving that tests actually bite (mutation testing, surviving mutants), when strengthening weak assertions, or when a pinned expected value needs to be re-earned after the world underneath it changed.
metadata:
  version: "0.1.0"
---

# Refactor & mutate

Green is a license to improve the code, not a certificate that the tests are good. This pass has two halves: **refactor the code under a live referee**, and **mutate to prove the referee bites**.

## Refactoring rules

1. **Only refactor on green.** If the suite isn't green, you're not refactoring; you're debugging with extra steps.
2. **Behavior-preserving means test-preserving.** The suite passes before and after with zero test edits. The moment a refactor requires changing a test's *assertion* (not just its plumbing), stop — either the behavior changed (that's a WP, go to `agentile:red-green`) or the test was asserting an implementation detail (fix the test first, as its own commit).
3. **Never delete a test to make a refactor pass.** Test count is monotone (Rule 2). If a test is genuinely obsolete, that's an ADR with the reason, not a quiet deletion.
4. **Keep the ratchets in view.** After the refactor: test count ≥ baseline, zero `.unwrap()` in production UI code, no `TODO`s introduced, benchmarks run if the code is performance-critical (Rule 6) with results committed.
5. **Surgical commits.** One refactor intent per commit. A rename plus a logic tweak in one diff is how logic changes sneak past review.

## Mutation testing: prove the tests bite

A test that never fails is indistinguishable from no test. Mutation testing answers: *if this code were wrong, would anything go red?*

**Procedure:**

1. Run a mutation tool over the WP's touched code — `cargo-mutants` (Rust), Stryker (JS/TS), `mutmut` (Python), or the project's configured tool. No tool available? Do it manually: flip a comparison, off-by-one a boundary, invert a branch, return a constant — and run the suite.
2. **Every surviving mutant is a verdict:** either dead code (delete it — as its own commit) or a coverage gap (write the killing test — red-first, watch it fail against the mutant).
3. Prioritize mutants in: money paths, authz checks, state transitions, parsers, arithmetic. A surviving mutant in an error-message string is noise; a surviving mutant in a balance check is a finding.
4. Record the campaign in the sprint file's Notes: mutants generated / killed / surviving-and-why. Surviving mutants you chose not to kill get a written reason.

## Mutating the tests themselves

Strengthen the suite while you're here:

- **Tighten weak assertions.** `assert!(result.is_ok())` becomes an assertion on the value. `assert_eq!(len, 3)` becomes an assertion on the contents.
- **Add adversarial variants.** For each happy-path test, ask what the malicious/degenerate input is (empty, max, duplicate, replayed, unauthorized) and add it.
- **Check the test tests the source.** An integration test that passes with the backing service turned off is a mock in disguise — unplug the source once and watch it fail.

## Pinned vectors: re-earning expected values

Tests that pin expected values captured from a real system (addresses, hashes, golden outputs) are strong — until the world beneath them legitimately changes (a chain re-rolls, a schema migrates). Then:

- **Re-earn the value from the real source.** Re-derive it by running against the live system, and record in the test comment where and when it was earned.
- **Never** update the pin to whatever the code currently produces — that converts a referee into a mirror. The tempting fix ("just update the expected value to match") is the anti-repair; it makes the test self-referential and worthless.

## Exit checklist

- [ ] Suite green, zero test-assertion edits during refactor (or ADR'd)
- [ ] Test count ≥ baseline
- [ ] Mutation campaign run on touched code; surviving mutants killed or justified in writing
- [ ] Weak assertions tightened; adversarial variants added where the mutation run exposed gaps
- [ ] Pinned vectors re-earned from source, never regenerated from the code under test
- [ ] Benchmarks run and committed if performance-critical code was touched

Then proceed to `agentile:document-pass`.
