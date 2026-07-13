---
name: feature-spec
description: Feature and spec creation under Agentile. Use when defining a new feature, writing or updating PRODUCT_SPEC.md, turning a request into acceptance criteria, writing BDD/Gherkin scenarios, or when a task arrives as a vague ask ("add a dashboard") that needs to become a testable specification before any code is written.
metadata:
  version: "0.1.0"
---

# Feature & spec creation

A spec's job is to make "done" checkable before work starts. Under Agentile, specs come before code because an unspecified feature invites the two failure modes the method exists to prevent: the agent optimizing a proxy ("it compiles, it must work") and the human accepting a pleasant claim ("dashboard shows earnings" — from where?).

## Where specs live

- **`.agentile/PRODUCT_SPEC.md`** — what the finished product does. Authoritative for product behavior (canonical constants still live in CONFIG.md): when a feature idea conflicts with it, either the spec is amended (ADR) or the feature bends.
- **Feature specs** — either a section added to PRODUCT_SPEC.md, a planset doc (`04_FEATURES_BDD.md`), or a WP scope block in the sprint file, depending on size. One home per feature (Rule 9); link from everywhere else.

Every spec doc carries Rule-12 frontmatter (`created`, `branch`, `author`, `status`).

## The spec-writing sequence

1. **Name the user and the outcome.** One sentence: who does what, and what changes in the world when it works.
2. **Trace every data source before writing behavior** (Rule 7). For each thing the feature displays, stores, or computes, name where the value comes from: contract address + method, RPC call, API endpoint, file path, table. If you cannot name the source, the feature is not specifiable yet — go find the source first. "We'll mock it for now" is how mocks end up in production.
3. **Write acceptance criteria that name their data sources.**
   - BAD: "Dashboard shows earnings."
   - GOOD: "Dashboard shows earnings from `ContributionAccounting.sol` via `eth_call`, verified by integration test `tests/integration_earnings.rs::test_earnings_from_contract`."
   Every criterion is a checkbox a skeptical reviewer can verify without asking you anything.
4. **Write BDD scenarios for behavior with branches.** Gherkin (`Given / When / Then`) for every capability with more than one outcome. These become the skeleton of the test plan (`agentile:test-plan`) and the failing tests (`agentile:red-green`).
5. **Declare scope edges.** An explicit **Out of scope (v1)** list. Follow-ons get named, not implied.
6. **Declare the simulation boundary, if any.** If part of the feature will ship as scaffolding (fixtures, canned data, demo gates), the spec says so explicitly, names the seam where real replaces fake, and the UI/docs must admit it. A prototype that admits it is scaffolding is safe to ship for review; a fake-live one is not, because it can be mistaken for done.

## Loopholes the spec must close

Specs are where two documented evasion patterns get blocked:

- **The Wittgenstein loophole.** A test-only type (`StubFooBackend`) gets wired as the default because nothing said it couldn't be. Spec fix: name the production backend and require test doubles behind `#[cfg(test)]` or a test-only feature flag.
- **The "Real Backend" loophole.** A type named `RealXxxBackend` returns hardcoded data and queries nothing. Spec fix: require every "real" method to name its data source in a code comment, and require at least one integration test that would fail if the source were disconnected.

## Spec quality gate

Before a spec is accepted into a sprint:

- [ ] One-sentence outcome exists and a non-author can restate it
- [ ] Every displayed/stored/computed value has a named data source
- [ ] Every acceptance criterion names its data source and its verifying test
- [ ] Branching behavior has Gherkin scenarios
- [ ] Out-of-scope list exists
- [ ] Simulation boundaries (if any) are explicit and visible to users
- [ ] Rule-12 frontmatter present
- [ ] No criterion is satisfiable by a mock, stub, or hardcoded value

## Claim honesty

Write spec language at the precision of what will actually be verified. "Sub-second finality" is a claim someone will have to substantiate in a doc-canonicalization pass (`agentile:document-pass`); "finality observed under 1s in the 3-node local testnet, unmeasured on mainnet" is a claim that survives audit. Precise now is cheaper than retracted later.

## Handoff

A finished spec feeds directly into:
- `agentile:planset` if the feature is program-sized (multiple sprints)
- `agentile:test-plan` to design the harness before implementation
- `agentile:red-green` once the sprint kicks off
