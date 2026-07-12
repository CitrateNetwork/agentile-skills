---
name: document-pass
description: The documentation pass that ends every WP and every session. Use after a WP closes, at the end of a work session, when a decision surfaced that needs an ADR, when public claims need canonicalization against reality, or when someone asks "update the docs" in an Agentile repo.
metadata:
  version: "0.1.0"
---

# The documentation pass

Documentation is not an afterthought in Agentile; it is the medium the project thinks in. Every contributor forgets everything every morning — what survives is what got written down, dated, and filed in the right home. The documentation pass runs at the end of **every** WP and every session, not just at sprint close.

## The pass, in order

### 1. Sprint file (Rule 4: it is the truth)

- Update the WP block: status marker, checked criteria, test names, commit hashes, follow-ups.
- Append the daily-update line: `- YYYY-MM-DD — <what closed>. <status>. <blockers>.` Append-only; never rewrite history.
- Update the Notes section with anything mid-sprint that the retro will need.

### 2. Decisions → ADRs (same day they're made)

Any decision that surfaced during the work — a library choice, a schema shape, a rejected approach — becomes an ADR *now*, while the alternatives are still in your head. Use the template shipped with `agentile:planset`. Link it from the sprint file's decisions section. An undocumented decision will be re-litigated by the next session at full cost.

Once ACCEPTED, an ADR is append-only. Reversing it means a new ADR that supersedes it, with the old one's frontmatter updated to `status: superseded`.

### 3. Rule-12 frontmatter sweep

Every doc created or touched this pass carries:

```yaml
---
created: YYYY-MM-DDTHH:MM:SSZ
branch: <git branch>
author: <name or role>
status: active | superseded | archived
---
```

Frontmatter coverage is a ratchet axis — it never goes down.

### 4. One-source-of-truth check (Rule 9)

For each topic you documented, ask: does this already have a home? If yes, update the home and link to it — don't write a second copy that will drift. If you found two homes for one topic, merge them now and leave a pointer. Copies rot; links don't.

### 5. Code-level docs

- Module/crate READMEs updated if the public surface changed.
- Every "real" backend method still names its data source in a comment.
- Comments state constraints the code can't show — not narration of what the next line does.

### 6. Claim canonicalization

Anywhere the work touched a public or cross-team claim (README, landing copy, spec, pitch material), grade the claim against what is now verified:

| Verdict | Meaning | Action |
|---|---|---|
| **SUBSTANTIATED** | Evidence exists and is linked | Keep; link the evidence |
| **STALE** | Was true, world changed | Update or date-stamp it |
| **UNSUPPORTED** | Nothing verifies it | Remove or downgrade wording |
| **OVERSTATED** | True-ish, but stronger than the evidence | Rewrite at the precision of the evidence |

Caveats ship *alongside* numbers, not after. "1,200 TPS (3-node LAN testnet, unverified on WAN)" outlives "1,200 TPS" every time someone checks.

### 7. Status surfaces

- Update the project's `CURRENT.md` (or equivalent live-status table) if sprint status changed.
- If the work unblocks or blocks someone else, write it where they will look — a handoff doc, not a chat message.

## Pass checklist

- [ ] Sprint file current (WP blocks + daily line)
- [ ] Every new decision has an ADR, linked from the sprint file
- [ ] All touched docs have Rule-12 frontmatter
- [ ] No topic gained a second home; merges done where found
- [ ] READMEs / data-source comments current
- [ ] Public claims graded; STALE/UNSUPPORTED/OVERSTATED ones fixed
- [ ] CURRENT.md / status surface updated

At sprint close, this pass hands off to `agentile:retro` and `agentile:journal`.
