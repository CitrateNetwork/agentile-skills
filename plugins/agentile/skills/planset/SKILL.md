---
name: planset
description: Writing an Agentile planset. Use when planning a program of work bigger than one sprint — a new product, subsystem, migration, or audit — when locking architectural decisions, writing ADRs, defining gates and exit criteria, or when someone says "write a planset", "plan this build", or "break this into sprints".
metadata:
  version: "0.1.0"
---

# Plansets

A planset is the program-level plan: the numbered document set that turns a vision into locked decisions, sprints, and machine-checkable gates. A sprint answers "what are we doing this week"; a planset answers "what are we building, what did we decide, and how will we know it's done."

Write a planset when the work spans multiple sprints, crosses repos, or locks decisions others will build on. Don't write one for a week of work — that's a sprint file.

## Canonical structure

Plansets live at `.agentile/planset/` (or a top-level `PLANSET/` directory) as numbered docs:

```
planset/
├── 00_OVERVIEW.md              # vision, locked decisions, core invariant, reuse map
├── 01_SCOPE_OF_WORK.md         # phases, deliverables, in/out of scope, risk register
├── 02_ARCHITECTURE.md          # components, data model, authz, external surfaces
├── 03_TLA_SPECS.md             # formal spec plan (if state machines are involved)
├── 04_FEATURES_BDD.md          # Gherkin scenarios for every v1 capability
├── 05_SPRINTS_AND_WPS.md       # sprint plan + work packages
├── 06..NN_*.md                 # topic docs and ADRs as needed
└── gates.yaml                  # machine-readable exit criteria + evidence
```

ADRs live in `planset/adr/` or `.agentile/adrs/` — template in this skill's directory (`ADR_TEMPLATE.md`).

## Frontmatter

Every planset doc opens with Rule-12 frontmatter plus planset fields:

```yaml
---
created: 2026-07-12T00:00:00Z
branch: main
author: <human> + <agent model>
status: planset (Stage-1 draft | Stage-2, red-teamed)
planset: <program-name>
code: <SPRINT-CODE-PREFIX>      # e.g. MOBILE-S0
repo: <repo(s) affected>
red_teamed: <date, once done>
companions: <sibling docs>
---
```

## The load-bearing sections of 00_OVERVIEW

1. **Why this exists** — the motivation, in prose a stranger can follow.
2. **Locked decisions.** A numbered table (`D-1`, `D-2`, …) with the choice and the date it was locked. Locked means: reversing it requires a superseding ADR, not a change of mood. Example shape:

   | # | Decision | Choice |
   |---|---|---|
   | D-1 | Storage substrate | Standalone Rust + RocksDB merkle-DAG |
   | D-2 | Authorization | Reuse `CapabilityGrant` + SIWE/OIDC |

3. **Core invariant** — the single sentence everything hangs off. If you can't write it, the architecture isn't settled.
4. **Architecture at a glance** — one diagram (Mermaid or ASCII).
5. **Surfaces we consume** — the reuse map. Everything reused from existing systems, named, so nothing gets rebuilt out of ignorance.
6. **Scope** — In (v1) / Out (follow-ons).
7. **Safety & compliance gates** — refuse-unless-ALL conditions, where applicable.

## The red-team pass

A planset is Stage-1 until it has been adversarially reviewed — by a second model, a second person, or a deliberately skeptical session whose brief is to break the plan, not polish it. Findings land in a **Red-team findings** section that *supersedes* the naive plan text above it (don't silently rewrite; show the correction). Then mark frontmatter `status: planset (Stage-2, red-teamed)` with the date. Building from a Stage-1 planset is allowed only for reversible groundwork.

## gates.yaml

Exit criteria live in machine-readable form so "done" is checkable by tooling, not vibes:

```yaml
version: 1
program: <planset code>
gates:
  - id: gate1
    name: Theory locked
    status: pending | partial | met
    exit_criteria:
      - id: g1-planset
        desc: Planset docs 00-05 complete and red-teamed
        met: false
        evidence: planset/
      - id: g1-formal
        desc: TLA+ modules TLC-green
        met: false
        note: >-
          Cite the TLC run: module names, state counts, date, script.
        evidence: formal/ ; scripts/run-tlc.sh
    reviewers: [Name (role)]
```

Rules: a criterion flips to `met: true` only with an `evidence` path that exists, and a `note` citing the proof (test run, TLC log, commit). Gates are append-hostile — once `met`, the evidence stays.

## Sprint breakdown (05_SPRINTS_AND_WPS)

- Every sprint gets a stable ID (`<CODE>-S0`, `<CODE>-S1`, …), a one-line goal, and its WPs with effort (S/M/L/XL).
- Each WP names its acceptance criteria *with data sources* (see `agentile:feature-spec`).
- Dependencies between sprints are a table, not prose.
- A sprint big enough to need its own planning spawns its own planset; link, don't inline (Rule 9).

## Planset quality gate

- [ ] Locked-decisions table with dates; each decision has an ADR or an inline rationale
- [ ] Core invariant stated in one sentence
- [ ] Reuse map present (what we consume, not rebuild)
- [ ] Every v1 capability has a BDD scenario in 04
- [ ] gates.yaml exists with evidence paths
- [ ] Red-team pass done and recorded, or status honestly says Stage-1
- [ ] Sprint IDs stable and referenced nowhere else with different names
- [ ] Rule-12 frontmatter on every doc
