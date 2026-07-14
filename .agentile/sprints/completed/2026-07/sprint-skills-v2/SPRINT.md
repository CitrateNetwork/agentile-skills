---
created: 2026-07-13T02:00:00Z
branch: main
author: Saul Loveman + Claude Fable 5
status: archived
sprint: SKILLS-S2
---

# Sprint SKILLS-S2: The trustworthy loop, packaged for outsiders

## Sprint Metadata

| Field | Value |
|-------|-------|
| **Sprint ID** | SKILLS-S2 |
| **Sprint Name** | The trustworthy loop, packaged for outsiders |
| **Goal** | A reader with no federation context can adopt a verified minimal loop, contribute to this repo safely, and guarantee a journal every sprint with documented tooling. |
| **Branch** | `main` |
| **Start Date** | 2026-07-13 |
| **Status** | `COMPLETE` |
| **Predecessors** | SKILLS-S0, SKILLS-S1 (closed 2026-07-12/13) |

## Test Baseline (start of sprint)

| Metric | Count | Captured | Canonical command |
|--------|-------|----------|-------------------|
| **Tests** | 209 | 2026-07-13 | `python3 scripts/validate.py` |
| **CI tripwires** | 4 classes | 2026-07-13 | validate.yml |

## Work Packages

### WP-1: docs/TRUSTWORTHY_LOOP.md — research-grounded adoption guide

| Field | Value |
|-------|-------|
| **Status** | `[x] COMPLETE` |
| **Estimated effort** | M |

**Acceptance Criteria**

- [x] Every external claim cites a source URL from the verified deep-research pass (25/25 confirmed, 0 refuted, 107 agents) — no claims from the unverified provenance leg presented as verified
- [x] Maps external practice to Agentile skills explicitly (minimal loop → escalation → full method)
- [x] Contains an honest-reading section naming the evidence gaps

### WP-2: docs/tutorials/journal-loop.md — guaranteed journal-per-sprint tutorial

| Field | Value |
|-------|-------|
| **Status** | `[x] COMPLETE` |
| **Estimated effort** | M |

**Acceptance Criteria**

- [x] All `/loop` and `/schedule` syntax verified against code.claude.com/docs (scheduled-tasks.md, routines.md, hooks.md) — no recalled syntax
- [x] Layered design: CI tripwire (deterministic) + in-session /loop + persistent /schedule routine + optional Stop hook, with the limits of each named (session-bound, 7-day expiry, cloud caps)
- [x] The tripwire layer is real in this repo (see WP-4), not hypothetical

### WP-3: CONTRIBUTING.md — trustworthy contributor path

| Field | Value |
|-------|-------|
| **Status** | `[x] COMPLETE` |
| **Estimated effort** | S |

**Acceptance Criteria**

- [x] States the loop a contribution must pass (harness, red-first for harness changes, version bump, independent review)
- [x] Same rules for human and agent authors, stated explicitly
- [x] Names what gets rejected and why

### WP-4: Harness check class 7 — sprint-close completeness

| Field | Value |
|-------|-------|
| **Status** | `[x] COMPLETE` |
| **Estimated effort** | S |

**Acceptance Criteria**

- [x] Every dir under `.agentile/sprints/completed/` must contain RETRO.md and have a journal in `.agentile/docs/journals/` whose frontmatter `sprint:` matches the sprint's ID — data source: both file sets
- [x] Seen red on a seeded violation before trusted green

## Daily updates

- 2026-07-13 — kickoff. Deep-research verified (25 claims, 0 refuted); /loop + /schedule syntax verified against official docs via claude-code-guide agent.

- 2026-07-13 (later) — all 4 WPs closed. Guide cites only 3-0-verified claims; tutorial syntax doc-verified; check 7 seen red on a seeded missing-journal violation then green (222/222); .claude/loop.md ships the Layer-2 loop. Closing.

## Close note (2026-07-13)

Goal met. Deliverables: docs/TRUSTWORTHY_LOOP.md, docs/tutorials/journal-loop.md, CONTRIBUTING.md, harness check class 7, .claude/loop.md, README section. Delta from plan: none material. The provenance research leg produced zero verified claims and the guide says so explicitly instead of papering over it.
