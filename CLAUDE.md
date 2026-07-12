# agentile-skills — repo rules

This repo packages the Agentile methodology as Claude Code skills. It is a Tier-1 federation repo and it dogfoods the method it ships.

Hard rules:

- **The skills document the method; the method governs the skills.** Canonical sources are `citrate-federation/agentile/rules/CORE_RULES.md` and the `agentile` skeleton repo's templates. When editing a SKILL.md, verify against the canonical source — do not drift the method by paraphrase. Divergence found → fix here, note the vendored-template version in the commit.
- **Templates are vendored, not authored here.** `*_TEMPLATE.md` files inside skill directories are copies from `agentile/.agentile/templates/`. Update them by re-copying from the skeleton, never by editing in place.
- **Every skill edit is a version bump** in the owning `plugin.json` (and `marketplace.json` for structural changes).
- **Descriptions are trigger conditions**, not summaries: they must say *when* to use the skill ("Use when…").
- **Rule-12 frontmatter** on all `.agentile/` docs in this repo.
- Sprint status lives in `.agentile/sprints/` — see the method you are standing in.
