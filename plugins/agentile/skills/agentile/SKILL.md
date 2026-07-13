---
name: agentile
description: Master guide to the Agentile methodology. Use when working in any repo with a .agentile/ directory, when kicking off, running, or closing a sprint, when unsure which Agentile artifact (spec, planset, WP, ADR, retro, journal, essay, case study) a situation calls for, or when someone asks "how does Agentile work?"
metadata:
  version: "0.1.0"
---

# Agentile — the method

Agentile is a file-based, git-native methodology for software built by humans and AI agents together. Its premise: **agents and their human directors are compounding optimists** — both biased toward over-claiming in good faith. Every rule and artifact below exists to force the gap between a pleasant-sounding claim and verified reality into the open.

Three properties define it:

1. **Everything important is external, checkable, and dated.** The smartest contributor in the room forgets everything every morning. State lives in files with frontmatter, not in chat, memory, or vibes.
2. **Rules are scar tissue, not design.** Each rule was extracted from a failure that recurred at least three times. Don't add speculative rules; don't drop enforced ones.
3. **Verification must be alive.** Absence-of-red and presence-of-green look identical when the verifier is dead. A sprint closes when linked CI is green, not when tasks are marked done.

## The 13 core rules

These are non-negotiable. Humans and agents follow identical rules.

| # | Rule | In practice |
|---|------|-------------|
| 0 | **Read before writing** | Read `.agentile/AGENT_ENTRY.md` and the repo's `CLAUDE.md` before touching code. |
| 1 | **No mocks, stubs, or TODOs in production paths** | Test doubles live behind `#[cfg(test)]` / test-only flags. CI greps for violations. |
| 2 | **Test count only goes up** | Snapshot at sprint kickoff; the end-of-sprint diff is non-negative. Removing a test requires an ADR. |
| 3 | **Audits are immutable** | Dated, never edited. Corrections go in a dated errata file. |
| 4 | **The sprint file is the truth** | Status lives in `.agentile/sprints/active/<slug>/SPRINT.md` — not Slack, not chat, not memory. |
| 5 | **Rule-12 frontmatter on every doc** | Every `.agentile/` doc opens with YAML: `created`, `branch`, `author`, `status`. |
| 6 | **Daily benchmark on performance-critical crates** | Sessions touching core code end with the benchmark suite; results committed. |
| 7 | **Data-source tracing before implementation** | Every endpoint names its data source (contract address, RPC method, file path) BEFORE code is written. |
| 8 | **Zero unwraps in production UI code** | `grep -rn '\.unwrap()' src/` returns 0 in GUI crates. Use `?` or `.expect("why")`. |
| 9 | **One source of truth per topic** | Link, don't copy. Canonical config wins over per-repo divergence. |
| 10 | **Authorization before destruction** | Force-push, branch deletion on main, secret rotation: explicit human approval first. |
| 11 | **The manifest is canonical** | Cross-repo state lives in the federation manifest; per-repo divergence loses. |
| 12 | **Cross-repo deps follow the drift map** | Declare the `[[drift]]` entry first, then add the dependency. |
| 13 | **Visibility flips need sign-off** | PRIVATE → PUBLIC on a Tier-1 repo requires lead approval and an ADR. |

(Rules 6, 8, 11–13 are federation-flavored; in a standalone repo, keep their spirit: benchmark what's hot, never unwrap in shipped UI, keep one canonical pin registry. Numbering note: in the pre-split archive, rule 5 was numbered "Rule 12" and rule 7 was "Rule 11" — the corpus and the vendored templates still use those names. "Rule-12 frontmatter" means rule 5 here; SPRINT_TEMPLATE.md's "Rule 11" means data-source tracing, not the manifest rule.)

## The artifact map

```
.agentile/
├── AGENT_ENTRY.md          # read-first orientation + tier
├── CONFIG.md               # canonical constants (highest doc authority)
├── PRODUCT_SPEC.md         # what the finished product does
├── rules/CORE_RULES.md     # the rules above
├── planset/                # program-level plans (00–NN numbered docs, gates.yaml)
├── sprints/
│   ├── active/<slug>/      # SPRINT.md, DAILY.md, RETRO.md (at close)
│   ├── backlog/
│   └── completed/<YYYY-MM>/  # immutable after close
├── adrs/                   # cross-cutting: ADR-<YYYY-MM-DD>-<slug>.md (planset-scoped: ADR-<NNN>-<slug>.md in planset/adr/, per the vendored template)
├── coverage/BASELINE.md    # ratchet baselines (tests, specs, tripwires, frontmatter)
├── formal/                 # TLA+ specs + TLC results, where applicable
└── docs/
    ├── journals/           # <YYYY-MM-DDTHHMM>_<slug>.md — session reflections
    ├── essays/             # ideas that outlive their sprint (NOT governance)
    └── case_studies/       # incident → lesson → enforcement surface
```

## The sprint lifecycle

1. **Kickoff.** Copy `SPRINT_TEMPLATE.md` (in this skill's directory) to `.agentile/sprints/active/YYYY-MM-DD-sprint-<track>-<id>-<slug>/SPRINT.md` (naming per the template header; repos with an established shorter `sprint-<slug>` convention keep it — match the repo). Fill goal, deliverables, WPs. Snapshot the test baseline (all four ratchet axes). Register the sprint in the project's CURRENT.md if one exists.
2. **Method order per WP:** TLA+ (if state-machine touching) → BDD/Gherkin → **failing test + tripwire** → code → refactor → adversarial check → journal entry. If a step doesn't apply, write down why in the WP block.
3. **Daily updates.** Append one dated line (or a DAILY.md block) per work day. Append-only.
4. **Decisions become ADRs** the moment they surface; link them from the sprint file.
5. **Close ceremony.** All exit criteria checked, CI green, `git mv` the sprint directory to `completed/<YYYY-MM>/`, set frontmatter `status: archived`, write RETRO.md, write the sprint journal. "Code done" without the paperwork is not closed.

**WP status markers:** `[ ] NOT STARTED` · `[~] IN PROGRESS` · `[x] COMPLETE` · `[!] BLOCKED`
**Effort scale:** S (<1 day) · M (1–3 days) · L (3–5 days) · XL (>1 week)

## Which skill, when

| Situation | Skill |
|---|---|
| Defining what to build; writing acceptance criteria | `agentile:feature-spec` |
| Planning a program of work, architecture, locked decisions | `agentile:planset` |
| Deciding how a sprint will be tested before code exists | `agentile:test-plan` |
| Implementing a WP (failing test → code → green → close) | `agentile:red-green` |
| Hardening after green: refactor, mutate, prove tests bite | `agentile:refactor-mutate` |
| End-of-pass documentation, ADRs, claim canonicalization | `agentile:document-pass` |
| Closing a sprint honestly | `agentile:retro` |
| Recording what a session taught (every sprint, minimum) | `agentile:journal` |
| An idea outgrew its sprint (attempt every sprint) | `agentile:essay` |
| Something broke and was fixed, or something novel emerged | `agentile:case-study` |

## Anti-patterns

- **"Status in Slack."** Rule 4 violation. Move it to the sprint file.
- **"90% done."** Not a measure of progress; a category of lie told in good faith. The last 10% is the work. Report what is verified, what is scaffolding, and what is unproven.
- **Editing a closed sprint or audit.** Write a dated follow-up instead.
- **`TODO:` in production.** Ship behind a flag or don't ship.
- **Two homes for the same work.** Pick one; link from everywhere else.
- **Trusting green CI you haven't seen run.** A dead verifier produces exactly the same silence as a passing one. Check that the referee is on the field.

## Templates in this skill

- `SPRINT_TEMPLATE.md` — copy to start any sprint.
- `DAILY_TEMPLATE.md` — append-only daily log.

Other templates ship with their owning skills (`retro`, `journal`, `essay`, `case-study`, `planset`).
