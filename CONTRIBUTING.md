# Contributing

This repo packages the Agentile methodology, and contributions to it run under the loop it ships. Same rules for humans and agents — an agent-authored PR is welcome and is held to exactly the standard below, nothing extra and nothing less.

## The loop your contribution must pass

1. **Read first (Rule 0).** `CLAUDE.md`, then the skill you're touching, then `docs/TRUSTWORTHY_LOOP.md` if you're new to the method.
2. **Done is machine-checkable.** `python3 scripts/validate.py` must pass at ≥ the count on `main`. The count is a ratchet: it never goes down. If you add a check, seed a violation and watch it fail before you trust its green (the repo's own harness was built this way; see the sprint records in `.agentile/sprints/completed/`).
3. **Skill edits bump versions.** Any change to a `SKILL.md` bumps the owning `plugin.json` and its `marketplace.json` entry (the harness cross-checks them).
4. **Templates are vendored, read-only.** `*_TEMPLATE.md` files are copies from the `agentile` skeleton repo. Never edit them in place — propose the change upstream, then re-vendor and regenerate `templates.lock`. The harness fails on in-place edits.
5. **Method content stays pinned to canon.** Skills describe the method; they don't fork it. Wording, structure, trigger, and reference fixes are welcome. Changes to the method's substance (rules, cadences, protocols) need a decision record and belong upstream first.
6. **Claims at the precision of evidence.** A description that says "Use when X" must be true. A doc that cites a number links its source. If you can't verify it, don't ship it.

## What review looks like

Your PR gets CI (the harness) plus an independent review — a fresh-context reviewer (human or agent) that sees the diff and the criteria, not your reasoning. Findings are triaged, not auto-applied: expect some to be accepted and some rejected with written reasons, and feel free to push back the same way. Deterministic checks outrank reviewer opinion in both directions.

## What gets rejected

- Any `TODO`, stub, or mock in shipped content (Rule 1)
- Test/check removals without a written decision record (Rule 2)
- Edits to closed sprints, retros, or dated records (Rule 3 — write a dated follow-up instead)
- Direct edits to vendored templates
- Skill descriptions that aren't trigger conditions ("Use when/at/after…" — CI-enforced)
- New skills without an owning plugin entry, version, and at least the description/name checks passing
- Unverifiable claims presented as fact, including in docs

## Attribution

Say what wrote the change. Commits from agent sessions in this repo carry a `Co-Authored-By` trailer for the agent; do the same or the equivalent for your tooling. This is a disclosure norm we hold ourselves to, not a gate — the gates are the checks above, which don't care who typed.

## Quick start

```
git clone https://github.com/CitrateNetwork/agentile-skills
cd agentile-skills
python3 scripts/validate.py   # must pass before and after your change
```

Sprint bookkeeping (`.agentile/`) is maintained by the maintainers; outside PRs don't need to touch it. If your change is big enough to want a sprint, open an issue first and we'll open one together.
