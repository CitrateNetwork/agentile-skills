---
name: journal
description: Writing an Agentile journal entry — the short-form session reflection. Use at sprint boundaries (kickoff, pivot, close — minimum one per sprint), after any session that produced a non-obvious learning, or when someone says "journal this". Not for status updates; those go in the sprint file.
metadata:
  version: "0.1.0"
---

# Journals

A journal is a short-form session reflection: what was learned during a work session that won't survive in commit messages. The chronology of journals across a project **is** its development history — treat them as the primary source future readers (including future you, memory wiped) will reconstruct the project from.

**Cadence:** minimum one per sprint, plus any session with a non-obvious learning. Kickoff, mid-sprint pivots, and close are the natural boundaries.

Template: `JOURNAL_TEMPLATE.md` in this skill's directory.

## Filing

```
.agentile/docs/journals/YYYY-MM-DDTHHMM_<slug>.md
```

Filename timestamp matches the frontmatter `created` to the minute. Rule-12 frontmatter, plus `sprint:` when the entry belongs to one.

## The dek test

Every journal opens with a one-line dek: the single sentence that captures why the entry exists. **If you can't write the dek, you're not ready to write the journal** — you have events but no learning yet. Work the material until the sentence appears, or file the events as a daily-update line instead.

## What goes in each section

- **Context** (2–3 sentences): sprint, branch, the immediate problem. Future readers won't have your context — give them just enough.
- **What happened**: linear narrative, 3–6 paragraphs. Show the work, not just the conclusion — the dead ends are often the payload.
- **What I learned**: the durable takeaway that should change how the next session approaches similar work. If there's no learning, this isn't a journal — it's a status update, and status belongs in the sprint file.
- **What I'd do differently**: the counterfactual. "Nothing — exactly this, again" is a legitimate answer, but say it honestly, not lazily.
- **Open questions**: surfaced but unresolved. These seed the next sprint's risk table.
- **Pointers**: sprint path, commit hashes, related journal/essay.

## Voice

Terse, in-session, outcome-focused. First person. Numbers up front when there are numbers ("108 findings — 4 CRITICAL, 26 HIGH..."). No victory laps: **losses, caught mistakes, and unproven claims are recorded with the same care as wins.** Where the record is thin or the claim unverified, the entry says so — an honest "this has never run against a real deploy" is worth more than a page of accomplishments.

Journal ≠ essay ≠ case study:

| Form | Anchor | Size | Write when |
|---|---|---|---|
| Journal | a session | 30–60 lines | every sprint, minimum |
| Essay (`agentile:essay`) | an idea | 100+ lines | the idea outgrows its sprint |
| Case study (`agentile:case-study`) | an incident | 100–150 lines | something broke and taught, or something novel emerged |

A journal that keeps growing an argument wants to be an essay; a journal that keeps circling one incident wants to be a case study. Split it, and leave a pointer.

## Quality gate

- [ ] Filed at the canonical path with matching timestamp
- [ ] Rule-12 frontmatter (+ `sprint:` if applicable)
- [ ] Dek passes the test — one sentence, real learning
- [ ] "What I learned" would actually change a future session's behavior
- [ ] Unverified claims labeled as such
- [ ] Pointers to sprint and commits present
