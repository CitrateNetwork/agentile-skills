---
created: 2026-07-13T02:00:00Z
branch: main
author: Saul Loveman + Claude Fable 5
status: active
---

# Tutorial: guarantee a journal every sprint

The `agentile:journal` cadence rule is *minimum one journal per sprint*. A cadence rule without enforcement is a hope. This tutorial builds the guarantee in four layers — a deterministic tripwire plus three grades of automation — using Claude Code's `/loop`, `/schedule`, and hooks. All syntax below is verified against the official docs ([scheduled-tasks](https://code.claude.com/docs/en/scheduled-tasks), [routines](https://code.claude.com/docs/en/routines), [hooks](https://code.claude.com/docs/en/hooks)) as of 2026-07-13.

The design principle, straight from the method: **automation guarantees that a missing journal is loud and that a draft exists; only the author makes it true.** An auto-drafted journal is a prompt to reflect, not the reflection.

## Layer 1 — the tripwire (deterministic, always on)

The non-negotiable layer: CI goes red if a sprint closes without its journal. Every completed sprint directory must contain `RETRO.md`, and a journal must exist whose frontmatter `sprint:` matches the sprint's ID.

```python
# sprint-close completeness (drop into your validation script)
import re
from pathlib import Path

def frontmatter_field(path, field):
    m = re.search(rf"^{field}:\s*(.+)$", path.read_text(), re.M)
    return m.group(1).strip() if m else None

journal_sprints = {frontmatter_field(j, "sprint")
                   for j in Path(".agentile/docs/journals").glob("*.md")}

for sprint_dir in Path(".agentile/sprints/completed").glob("*/*/"):
    sprint_md = sprint_dir / "SPRINT.md"
    sprint_id = frontmatter_field(sprint_md, "sprint")
    assert (sprint_dir / "RETRO.md").is_file(), f"{sprint_dir}: no RETRO.md"
    assert sprint_id in journal_sprints, f"{sprint_dir}: no journal with sprint: {sprint_id}"
```

This repo runs exactly this as check class 7 of `scripts/validate.py` — a sprint archived without its journal cannot merge green. The tripwire is the guarantee; everything below just makes meeting it convenient.

## Layer 2 — in-session `/loop` (while you're working)

`/loop` re-runs a prompt on an interval inside your current session. Syntax: `/loop [INTERVAL] [PROMPT]`, units `s/m/h/d`, minimum 1 minute.

```
/loop 45m check .agentile/sprints/active/ — if any WP closed since the last
check or a sprint is being closed, and .agentile/docs/journals/ has no entry
for it yet, draft one from the agentile:journal template and ask me to review
```

Or let Claude self-pace (it picks 1 minute to 1 hour adaptively) by omitting the interval:

```
/loop watch the active sprint and prompt me to journal at every boundary
```

Best option for a repo: commit the loop prompt as `.claude/loop.md`, and a bare `/loop` runs it. That makes the journal-watch loop part of the repo itself — any contributor types `/loop` and gets the same behavior.

**Limits you must know:** loops are session-bound. They stop when you start a new conversation (they do survive `claude --resume` / `--continue` if unexpired), expire after 7 days, and cap at 50 per session. Press `Esc` to stop one. So `/loop` is the convenience layer, not the guarantee — a closed laptop means no loop.

## Layer 3 — `/schedule` cloud routine (survives your sessions)

For the actual "guaranteed even if nobody opens a terminal" layer, use a scheduled cloud routine. Routines run on Anthropic's infrastructure against a fresh clone of your default branch, and push to `claude/`-prefixed branches:

```
/schedule every weekday at 5pm: compare .agentile/sprints/completed/ against
.agentile/docs/journals/ — for any sprint missing a journal, draft one from
the JOURNAL_TEMPLATE (frontmatter sprint: set correctly, honest about being
an automated draft) on a claude/ branch and open a PR for the author to
rewrite. If an active sprint has daily updates but no journal yet, note it
in the PR description instead of drafting.
```

Manage with `/schedule list`, `/schedule update <name>`, `/schedule run <name>`, or the web UI at claude.ai/code/routines (which also supports GitHub-event and API triggers — e.g. fire the routine when a PR whose branch matches `sprint-close/*` merges).

**Limits:** recurring custom crons have a 1-hour minimum; runs count against a daily cap on your account; the routine sees only what's on the default branch, so it cannot see an unclosed local sprint — which is fine, because the journal debt it enforces is defined by what's merged.

## Layer 4 (optional) — a Stop hook as a hard gate

Anthropic's published escalation ladder ends with deterministic gates: a `Stop` hook runs a script when Claude finishes responding and can block the turn from ending until the check passes (Claude Code overrides after 8 consecutive blocks). Wire the Layer-1 script in `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 scripts/check_sprint_close.py"
          }
        ]
      }
    ]
  }
}
```

If the script exits non-zero with a message like "sprint SKILLS-S2 archived without a journal," the agent cannot end its turn on a close that skipped the ceremony — it has to fix it or say why. Note the documented constraint: hooks can run scripts, block, and inject context, but cannot invoke slash commands.

## Which layers do you need?

| Layer | Guarantees | Fails when |
|---|---|---|
| 1. CI tripwire | absence is loud, merge-blocking | never (that's the point) |
| 2. `/loop` | you get nudged while working | session ends, 7-day expiry |
| 3. `/schedule` routine | a draft PR exists even if nobody's at a terminal | daily cap hit; work never merged |
| 4. Stop hook | the closing session can't end without the journal | agent overrides after 8 blocks |

Minimum honest setup: **Layer 1 + Layer 3.** The tripwire makes the debt visible; the routine pays the mechanical part of it. Layers 2 and 4 are quality-of-life for people actually in the loop.

One last honesty note, per `agentile:journal`: if the auto-draft ships unedited, you've automated a status update wearing a journal's clothes. The dek test still applies — a human or the working agent rewrites the draft with what was actually learned, or the entry is noise with valid frontmatter.
