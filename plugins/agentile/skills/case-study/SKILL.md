---
name: case-study
description: Writing an Agentile case study — turning a real incident into a durable lesson with an enforcement surface. Use when something broke and was fixed, when a near-miss or surprising outcome revealed a recurring pattern, when a novel concept or implementation emerged that others will want to reuse, or when a costly remediation is closing.
metadata:
  version: "0.1.0"
---

# Case studies

A case study is anchored to a specific incident and turns it into a durable lesson. It sits between an essay (idea-first) and an audit finding (defect-first): it takes a thing that actually happened, names what it teaches, and proposes the **enforcement surface** that would catch its recurrence.

**Write one when:**
- Something broke and the break-plus-fix reveals a pattern that could recur in other forms
- A near-miss or surprising outcome contradicted the going model
- A particularly costly or instructive remediation is closing
- Something **novel** emerged — a concept or implementation worth reusing — and the "incident" is the discovery itself
- An external industry incident maps cleanly onto a class of risk this project carries

**Don't write one for routine bugs.** The point is the generalizable lesson, not the diary entry. If there's no lesson that transfers beyond the instance, it's a journal entry.

Template: `CASE_STUDY_TEMPLATE.md` in this skill's directory.

## Filing

```
.agentile/docs/case_studies/YYYY-MM-DDTHHMM_<slug>.md
```

Rule-12 frontmatter (`created`, `branch`, `author`, `status`). Slug names the incident and hints the lesson (`live-pinned-vectors-and-the-masked-main`).

## Structure

1. **Dek** — one sentence naming the lesson. The reader knows within five seconds what they're getting.
2. **TL;DR** — 3–5 sentences: what happened, what it cost, what to do about it. Written for the reader who reads nothing else.
3. **Anchor incident** — dates, commits, components, observed behavior, `file:line` citations. Plus the table: when / where / **cost** (wall-clock, dollars, lost trust — be specific) / detected by.
4. **Expected vs. got** — the design's implication against the code's behavior, side by side.
5. **Why it happened** — the mechanism. Don't stop at proximate cause; keep asking "and why did THAT happen?" until the answer is a property of how the team, tool, or process works. "A typo" is never the bottom.
6. **The repair — and the anti-repair.** Document the correct fix *and* the tempting-but-wrong fix, and why the wrong one is wrong. (Example of the register: when a pinned test vector breaks after the world changes, the anti-repair is updating the pin to whatever the code now produces — it converts a referee into a mirror. The repair is re-earning the value from the real source.)
7. **Indicators** — the early-warning signs that, in retrospect, should have flagged it. These become tripwire candidates.
8. **Enforcement surface** — the durable mechanism that prevents recurrence: CI tripwire, TLA+ invariant, lint rule, review gate. Specific, with where it lives. **A case study without an enforcement surface is just a war story.**
9. **What this does NOT cover** — adjacent failure modes the enforcement doesn't prevent. Naming these honestly is the difference between a useful case study and a smug one.
10. **References** — sprint, audit findings, related essays/case studies, external sources.

## Voice

Clinical, forensic, rule-extracting. Setup → break → repair, like a postmortem. Real commands and diffs, not paraphrase. No blame theater and no heroics — the system that allowed the defect is the subject, not the person or agent who typed it.

## The follow-through

A case study isn't closed until its enforcement surface is *filed as work*: a WP in an active sprint or a named backlog item, linked from the case study. Verify the tripwire has been seen red at least once (see `agentile:test-plan`). For novel-concept case studies, the equivalent follow-through is the reuse pointer: where the pattern now lives so the next project consumes it instead of reinventing it.

## Quality gate

- [ ] Dek names a transferable lesson
- [ ] Anchor incident cited with dates, commits, `file:line`
- [ ] Cost quantified honestly
- [ ] Five-whys depth: root cause is a process/tool property, not a typo
- [ ] Anti-repair documented alongside the repair
- [ ] Enforcement surface named, specific, and filed as real work
- [ ] "What this does NOT cover" present
- [ ] Rule-12 frontmatter; canonical path
