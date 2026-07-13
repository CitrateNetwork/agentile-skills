---
created: 2026-07-12T00:00:00Z
branch: main
author: Saul Loveman + Claude Fable 5
status: active
repo: agentile-skills
tier: T1
---

# AGENT_ENTRY — agentile-skills

## What this repo is

The Agentile methodology packaged as a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`), plus federation-navigation skills. Tier-1 because it is the training surface for every agent and employee working in the federation: an error here propagates into every repo that installs it.

## Read, in order

1. `CLAUDE.md` — this repo's hard rules (vendored templates, version bumps, no method drift)
2. `plugins/agentile/skills/agentile/SKILL.md` — the method itself, mastered by reading it
3. `.agentile/sprints/active/` — what's in flight
4. Canonical upstream: `../citrate-federation/.agentile/rules/CORE_RULES.md`, `../agentile/.agentile/templates/`

## What lives here

- `.claude-plugin/marketplace.json` — marketplace manifest (2 plugins)
- `plugins/agentile/` — 11 methodology skills + vendored templates
- `plugins/citrate-federation/` — 2 federation skills (navigate, projects)
- `.agentile/` — this repo's own sprints, journals, retros (we dogfood)

## Cross-repo references

- Registered in `citrate-federation/manifest.toml` as `[repos.agentile-skills]`
- Listed in `citrate-labs/onboarding/FEDERATION_MAP.md`
- Method canon: `citrate-federation/agentile/` — this repo distributes; it does not define
