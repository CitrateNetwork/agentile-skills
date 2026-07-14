Maintenance loop for agentile-skills (run with a bare `/loop`):

1. Run `python3 scripts/validate.py`. If anything fails, report the failures and stop the loop pass there.
2. Check `.agentile/sprints/active/` — if any WP closed since the last pass or a sprint is being closed, and `.agentile/docs/journals/` has no entry with a matching `sprint:` frontmatter field, draft one from the `agentile:journal` template and ask the user to review it. Mark the draft honestly as automated.
3. If a sprint directory was moved to `completed/` this pass, verify the close ceremony: RETRO.md present, frontmatter `status: archived`, journal present (the harness enforces this too — check 7).
4. Nothing to do → say so in one line.
