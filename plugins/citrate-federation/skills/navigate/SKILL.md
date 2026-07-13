---
name: navigate
description: Orientation in the CitrateNetwork federated repositories. Use when landing in citrate-labs or any citrate-* repo for the first time in a session, when unsure which repo owns a concern, when sources disagree about the state of the federation, or when someone asks "where does X live?" or "what's the current state of Y?"
metadata:
  version: "0.1.0"
---

# Navigating the Citrate federation

The federation is ~40 repos, dozens of handoffs and plansets, and one human. Without a map, an agent burns its context reading everything and still acts on stale facts. This skill is the map: where truth lives, what to ignore, and the order to read things in.

## The mental model

- **`citrate-labs/`** is the meta-repo: umbrella docs, `onboarding/`, `handoffs/`, `docs/essays/`, `docs/case_studies/`, and `citrate-journals/` (no remote). It vendors no source code. The code repos live inside it as **independent git repos** (untracked by labs).
- **`citrate-federation/`** is the control plane: `manifest.toml` (cross-repo SHA pins — the federation's heartbeat), `agentile/` (rules, CURRENT.md), `scripts/` (pin-bump, drift-check).
- Every repo runs **Agentile** (see the `agentile` plugin): `.agentile/AGENT_ENTRY.md` + `CLAUDE.md` per repo, sprint files as the source of status.

## The orientation sequence (do this, in this order)

1. `citrate-labs/START_HERE.md` — pick your door (agents → `onboarding/AGENTS.md`)
2. `citrate-labs/onboarding/AGENTS.md` — mental model + truth hierarchy
3. `citrate-labs/onboarding/FEDERATION_MAP.md` — full repo inventory with tiers
4. `citrate-federation/agentile/CURRENT.md` — what's active *right now*
5. `citrate-federation/manifest.toml` — which SHA of each repo is known-good together
6. `<target repo>/CLAUDE.md` — that repo's hard rules
7. `<target repo>/.agentile/AGENT_ENTRY.md` — entry point + tier
8. `<target repo>/.agentile/sprints/active/` — what's in flight there

Read only as deep as the task needs — the sequence exists so you can stop early with confidence, not so you read everything.

## The truth hierarchy (when sources disagree)

1. **The code and its tests** — a passing test beats prose, always
2. **`<repo>/CLAUDE.md`** — repo hard rules (no mocks, name your data sources)
3. **`<repo>/.agentile/AGENT_ENTRY.md`** — read-first + tier
4. **`citrate-federation/manifest.toml` + `citrate-federation/agentile/CURRENT.md`** — cross-repo pins and live status
5. **Active sprint files** — in-flight work with daily updates
6. **Plansets** — the plan and acceptance criteria
7. **`handoffs/*.md`** — session-to-session context. Useful but **DATED** — verify before relying

Staleness is the characteristic failure of this archive: a document doesn't lie, it answers a stale question in a fresh-sounding voice. Check the `created:` frontmatter date on everything, and treat anything dated **before 2026-06-07** with suspicion — the May-2026 genesis re-roll invalidated earlier chain heights, addresses, and deployment facts (chain ID 40204 itself is permanent).

## Tiers

Tier comes from each repo's `AGENT_ENTRY.md` frontmatter (and the manifest). **T1** = highest-stakes surface — consensus, contracts, money, keys, identity, or anything customer-facing under a partner's eye; changes get the most review, and PRIVATE→PUBLIC flips need sign-off (Rule 13). T2/T3 = marketing/docs/tooling weight. `—` = not yet tier-tagged.

## Where things live (lookup table)

| You need… | Canonical source |
|---|---|
| Current SHA pins across repos | `citrate-federation/manifest.toml` |
| What sprint is active now | `citrate-federation/agentile/CURRENT.md` |
| The 13 rules, in full | `citrate-federation/.agentile/rules/CORE_RULES.md` (reading copy: `citrate-labs/docs/AGENTILE_RULES.md`) |
| Repo inventory + tiers | `citrate-labs/onboarding/FEDERATION_MAP.md` |
| A repo's hard rules | `<repo>/CLAUDE.md` |
| A repo's tier + read-order | `<repo>/.agentile/AGENT_ENTRY.md` |
| In-flight work in a repo | `<repo>/.agentile/sprints/active/` |
| Cross-repo wiring diagram | `citrate-federation/routing/topology.md` |
| Whether pins are in sync | `citrate-federation/scripts/drift-check.sh` (nightly CI) |
| Pre-split (May 2026) history | `citrate-agentile-archive/` — read-only |
| Narrative history / voice reference | `citrate-journals/` (chapters, tracks, indexes), `docs/essays/agentile-history/` |
| Session-to-session context | `citrate-labs/handoffs/` — check dates |

## The repo landscape (orient by concern)

- **Chain & node:** `citrate-chain` (T1 — the L1: GhostDAG, LVM/REVM, contracts, Halo2), `citrate-node-agent`, `citrate-bundler`, `citrate-simulation`
- **Identity & wallets:** `citrate-identity` (auth.citrate.ai OIDC), `citrate-native` (T1 desktop), `citrate-wallet-extension` (T1), `citrate-core` (T1 full-node desktop client + app launcher)
- **Compute & agents:** `citrate-inference-gateway`, `citrate-compute-pool`, `citrate-agent-runtime`, `nist-agent`, `citrate-studio` (all T1)
- **Memory & comms:** `citrate-memories` ("git for agents" DAG, MCP-served), `citrate-comms` (T1 E2E workspace)
- **Apps & surfaces:** `citrate-explorer` (CitrateScan), `citrate-dashboard` (T1), `citrate-buyer-webapp` (T1), `citrate-alf-web` (T1 ALF portal), `citrate-boeing-shell` (T1), `citrate-learning-center` (T1), `citrate-landing` (T2), `citrate-dataroom` (T1)
- **SDKs:** `citrate-sdk-js`, `citrate-sdk-python`, `citrate-sdk-marketplace` (all T1)
- **Security & audit:** `citrate-security` (audit control plane, Agentile-Audit standard), `hermes-audit-2026-07`
- **Docs & business:** `citrate-docs` (T3, Atlas), `citrate-commercial`, `citrate-compliance` (T3)

When unsure which repo owns a concern, check FEDERATION_MAP.md before grepping the world — the map is maintained as a first-class artifact and it is usually right.

## Hard safety facts

- Never `git pull` a pinned consumer to "update" it — fetch the exact object and detach onto it; the pin is the truth (fail closed).
- Remotes are hard-pinned fully-qualified GitHub URLs (`git@github.com:CitrateNetwork/<repo>.git` or `https://github.com/CitrateNetwork/<repo>.git`) — never SSH aliases; an unpinned alias is an indirection an attacker can repoint. (Individual machines may use HTTPS rewrites; the manifest pins are what matter.)
- Force-push, branch deletion on main, and secret rotation require explicit human approval first (Rule 10).
- `citrate-journals` has **no remote** — never assume it is backed up remotely; never push it anywhere.

For starting or coordinating work (sprints, cross-repo deps, handoffs, dispatch), continue to `citrate-federation:projects`.
