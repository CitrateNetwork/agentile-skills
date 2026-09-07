# agentile-skills

The **Agentile methodology**, packaged as Claude Code skills — plus navigation skills for the CitrateNetwork federated repositories.

Agentile is a file-based, git-native method for software built by humans and AI agents together. Its premise: agents and their directors are compounding optimists, and every artifact in the method exists to force the gap between a pleasant claim and verified reality into the open. The rules were not designed; they were extracted from a year of recurring failures. This marketplace packages that method so any agent (and any teammate) can work it fluently in any repo.

## Install

```
/plugin marketplace add CitrateNetwork/agentile-skills
/plugin install agentile@agentile-skills
/plugin install citrate-federation@agentile-skills   # Citrate federation members only
```

Or copy individual skills into `~/.claude/skills/`.

### Pinning to a known-good version

`/plugin marketplace add CitrateNetwork/agentile-skills` resolves to the
**default branch** — a mutable ref. Every installation follows `main`, so a
push to `main` reaches your agent session on the next marketplace refresh. If
you want to trust a specific reviewed artifact rather than "whatever is on
`main` today", pin the marketplace source to a **release tag** and re-point it
deliberately when you have reviewed the diff:

```
# Pin to a published release tag (recommended for anything you rely on):
/plugin marketplace add CitrateNetwork/agentile-skills@vX.Y.Z
```

Integrity of the executable skill content is enforced in CI by
`scripts/check_skill_integrity.py`, which pins every `SKILL.md` by SHA-256 in
[`skills.lock`](skills.lock); a content change that is not accompanied by a
reviewed lock update fails the harness. Review is routed by
[`.github/CODEOWNERS`](.github/CODEOWNERS). See the release notes for the
digest of each tagged version.

## The `agentile` plugin (the method, portable)

| Skill | Covers |
|---|---|
| `agentile` | Master guide: the 13 rules, artifact map, sprint lifecycle, which skill when |
| `feature-spec` | Feature & spec creation; data-source tracing; acceptance criteria that name their sources; BDD |
| `planset` | Program-level planning: numbered docs, locked decisions, red-team pass, gates.yaml, ADRs |
| `test-plan` | Planning the testing framework: baselines, harness selection (TLA+ → BDD → property → unit → integration → fuzz → live), tripwires |
| `red-green` | WP execution: failing test first, code to green, close-with-proof |
| `refactor-mutate` | Post-green hardening: refactoring rules, mutation testing, strengthening tests, re-earning pinned vectors |
| `document-pass` | The documentation pass on every WP: sprint file, ADRs, frontmatter, claim canonicalization |
| `retro` | Sprint retrospectives and the close ceremony |
| `journal` | Session journals — minimum one per sprint |
| `essay` | Long-form institutional learning — attempted every sprint, written when an idea earns it |
| `case-study` | Incident → lesson → enforcement surface — written when we break and fix something, or discover something novel |

Skills ship the canonical templates (SPRINT, DAILY, ADR, RETRO, JOURNAL, ESSAY, CASE_STUDY), vendored from the `agentile` skeleton repo.

## The `citrate-federation` plugin (Citrate-specific)

| Skill | Covers |
|---|---|
| `navigate` | Orientation sequence, truth hierarchy, tiers, repo landscape, staleness rules |
| `projects` | Running work in the federation: manifest & drift discipline, pin-bump, handoffs, parallel agent dispatch, new-repo checklist |

## The intended loop

```
feature-spec → planset (if program-sized) → test-plan
  → red-green → refactor-mutate → document-pass     (every pass)
  → retro + journal                                  (every sprint)
  → essay (attempted every sprint) · case-study (on break/fix or novelty)
```

## Adopting the loop

- **[docs/TRUSTWORTHY_LOOP.md](docs/TRUSTWORTHY_LOOP.md)** — the research-grounded adoption guide: what current evidence says about agentic verification (and its defeat), the escalation ladder, and the day-1 minimal loop.
- **[docs/tutorials/journal-loop.md](docs/tutorials/journal-loop.md)** — guarantee a journal every sprint with a CI tripwire + `/loop` + `/schedule` (this repo runs the tripwire as harness check class 7, and ships the `/loop` prompt as `.claude/loop.md`).
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — the loop your contribution must pass. Same rules for humans and agents.

## Repo status

Tier-1 repo in the CitrateNetwork federation. Canonical method source: `citrate-federation/.agentile/rules/CORE_RULES.md` and the `agentile` skeleton repo — this marketplace is the distribution surface; when they diverge, the federation rules win and this repo gets a version bump.

## License

MIT
## Open source and access

This repository is public. Citrate open sources the whole chain and application layer before mainnet, in January 2027; until then most of the core is access-by-request, as a security practice, not secrecy. Approved contributors receive privileged access to every repository except the private repos of clients and employees. Request access at [citrate.ai/contact](https://citrate.ai/contact) or email `hello@citrate.ai`. Full policy: <https://docs.citrate.ai/start/open-source>.
