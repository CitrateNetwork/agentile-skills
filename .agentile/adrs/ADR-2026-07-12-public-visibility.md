---
created: 2026-07-12T23:00:00Z
branch: main
author: Saul Loveman + Claude Fable 5
status: active
---

# ADR-2026-07-12: agentile-skills goes PUBLIC

| Field | Value |
|-------|-------|
| **ADR Number** | ADR-2026-07-12-public-visibility |
| **Date** | 2026-07-12 |
| **Status** | ACCEPTED |
| **Author** | Saul Loveman (federation lead) + Claude Fable 5 |
| **Sprint** | — (config flip with its own ADR; no sprint warranted) |

## Context

Rule 13: PRIVATE → PUBLIC on a Tier-1 repo requires federation-lead sign-off and an ADR. The owner directed the flip in-session on 2026-07-12 ("I would like the marketplace publicly installable and available on citratenetwork org"). The repo's purpose is distribution — a marketplace nobody can install defeats it — and `/plugin marketplace add CitrateNetwork/agentile-skills` requires either public visibility or per-user GitHub auth.

## Decision

**We will flip `CitrateNetwork/agentile-skills` to PUBLIC**, and record `visibility = "public"` in the federation manifest.

## Rationale

- The repo contains methodology documentation and navigation guidance only. A pre-flip scan (grep for credentials, keys, internal IPs, infra hostnames) found nothing sensitive.
- The `citrate-federation` plugin does expose internal *shape*: repo names, tiers, canonical file paths, coordination conventions, and candid process notes (e.g. the bus-factor caution). The owner reviewed this content at 0.1.0 and authorized publication; none of it is secret material, and the federation's own essays already narrate the same structure.
- Known exposure accepted: the owner contact email in `marketplace.json` (`saulweiloveman@gmail.com`) becomes public, including via git history (history rewrite rejected — Rule 10 ceremony for no security gain; it is a contact address, not a credential).

### Alternatives considered

| Alternative | Pros | Cons | Why rejected |
|-------------|------|------|--------------|
| Stay private, per-user auth installs | No exposure | Every installer needs org access; kills marketplace use | Defeats the repo's purpose |
| Split: public `agentile` repo, private federation plugin | Minimal internal exposure | Two repos to version, register, and drift-check | Scan found nothing warranting it |
| **Flip whole repo public** | One install path, simplest | Internal shape visible | **Selected** |

## Consequences

**Positive:** anyone can `/plugin marketplace add CitrateNetwork/agentile-skills`; the methodology is citable outside the org.
**Negative (mitigated):** federation internals are readable — mitigated by the scan and by the standing rule that nothing secret lands in this repo (CI harness + review gates); future commits must assume a public audience.
**Neutral:** the `citrate-federation` plugin remains useless outside the federation workspace; its README says so.

## Compliance check

- [x] Federation-lead sign-off (owner, in-session, 2026-07-12)
- [x] Does not violate CORE_RULES (Rule 13 satisfied by this ADR)
- [x] Manifest updated: `visibility = "public"` for `[repos.agentile-skills]`
- [x] Rule-12 frontmatter present

## Revision history

| Date | Author | Change |
|------|--------|--------|
| 2026-07-12 | Saul Loveman + Claude Fable 5 | Proposed and accepted |
