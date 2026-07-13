---
name: red-green
description: Implementing an Agentile work package — failing tests first, then code to green, then close-with-proof. Use when starting implementation on any WP, fixing a bug, or when tempted to write code before a test exists. Also use when closing a WP to verify the close-with-proof checklist.
metadata:
  version: "0.1.0"
---

# Red → Green: executing a work package

Every WP is red-test-first: **reproduce, then fix, then green.** The failing test is written before the implementation because a test written after the code passes tends to test what the code does, not what the spec demands.

## The protocol

1. **Open the WP block** in the sprint file. Set status `[~] IN PROGRESS`. Reread the acceptance criteria — every one names a data source and a verifying test (if not, go back to `agentile:feature-spec`; do not improvise criteria mid-WP).

2. **Write the failing test(s) first.**
   - For a feature: the test that encodes the acceptance criterion, against the *named data source* — not a mock of it.
   - For a bug: the test that reproduces the defect. For a security finding: reproduce the forgery/exploit as a test.
   - Run it. **Watch it fail, and read the failure.** A test that fails for the wrong reason (compile error, missing fixture) is not red; it's broken. Red means: fails precisely because the behavior doesn't exist yet.

3. **Land the tripwire with the test** if the test plan called for one — the class-level CI gate, not just the instance-level regression test. CRITICAL/HIGH bug fixes always get one, test plan or not (see `agentile:test-plan`).

4. **Implement the smallest change that makes it green.** Constraints while writing:
   - No mocks/stubs/TODOs in production paths (Rule 1). Test doubles behind `#[cfg(test)]` or test-only flags.
   - Every "real" backend method names its data source in a comment (closes the Real-Backend loophole).
   - No `.unwrap()` in production UI code (Rule 8) — `?` or `.expect("why this cannot fail")`.
   - Don't fix unrelated things you notice; file them in the sprint's Notes and keep the diff surgical. A commit that fixes one line should not drag foreign changes along.

5. **Green, then verify behavior — not shape.** *Compiles* is a claim about syntax. *Tests pass* is a claim about the code's shape under your fixtures. If the WP touches a live system (chain, service, real DB), exercise the live path before claiming complete. The gap between "tested" and "live works" is where demo-day bugs live.

6. **Run the full suite, compare to baseline.** Count must be ≥ baseline (Rule 2). If a test had to be removed, that's an ADR, written now, not a footnote later; a rewritten assertion follows the assertion-edit rule in `agentile:refactor-mutate` (its own commit, stating why).

## Close-with-proof

A WP flips to `[x] COMPLETE` only when all of these hold:

- [ ] Every acceptance checkbox checked, each verifiable by its named test
- [ ] New tests listed in the WP block by name (`tests/x.rs::test_y`) with what each verifies
- [ ] Test count ≥ baseline; delta recorded
- [ ] No `TODO` / stub / mock in production paths (grep it, don't recall it)
- [ ] Tripwires from the test plan are in CI and have been seen red at least once
- [ ] Live-path verification done, or explicitly recorded as not applicable and why
- [ ] Commit hashes recorded in the WP block
- [ ] Daily-update line appended to the sprint file

Anything genuinely unfinished becomes a named follow-up in the WP block — visible, not vanished. `[x] COMPLETE (+ 2 follow-ups)` is honest; a silent 90% is not.

## Reporting language

Report at the precision of what you verified:

- "green locally, CI pending" — fine, say exactly that
- "the seeder compiles and unit tests pass; it has never run against a real deploy" — fine, and load-bearing
- "done" — only after close-with-proof

"90% done" is a category of lie told in good faith. The last 10% — the live path, the paperwork, the tripwire — is the work.

## After green

Hand off to `agentile:refactor-mutate` (harden), then `agentile:document-pass` (record). Both happen on every pass, not just at sprint close.
