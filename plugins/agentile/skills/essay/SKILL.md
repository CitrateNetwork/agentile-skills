---
name: essay
description: Writing an Agentile essay — long-form institutional learning for ideas that outlive their sprint. Attempt one every sprint; write one when something genuinely meaningful happened. Use at sprint close after the journal, when a journal entry keeps growing an argument, or when a principle worth keeping has emerged from the work.
metadata:
  version: "0.1.0"
---

# Essays

An essay is a conceptual argument: an idea large enough to outlive its sprint. Journals record sessions; case studies dissect incidents; essays defend claims. They preserve the *reasoning* behind how the project works, and they survive across eras even when the architecture they describe has been replaced.

**Cadence:** attempt one every sprint — at close, after the journal, ask "did an idea emerge here that a stranger would want defended in full?" Write it when the answer is yes. **Do not manufacture one when it's no** — a forced essay is a status update in a costume, and it dilutes the corpus. "Considered, none warranted" in the retro Notes is a valid outcome.

Template: `ESSAY_TEMPLATE.md` in this skill's directory.

## Essays are NOT governance

The single most important rule. Essays are historical context, not operating rules. If a future session needs "is this still how we do things?", the answer lives in CORE_RULES.md, CONFIG.md, PRODUCT_SPEC.md, or the active sprint file — never in an essay. If your essay's implications should bind current work, say which ones, and note they take effect only through an ADR or sprint plan.

## Filing

```
.agentile/docs/essays/YYYY-MM-DDTHHMM_<slug>.md
```

Rule-12 frontmatter; filename timestamp matches `created` to the minute.

## Structure that works

1. **Title** — declarative and short. The title takes a position ("The Mess Became a Method", "CI/CD Before Code").
2. **Epigraph** — one sentence: the claim the essay defends.
3. **Anchor first, never abstract.** Open with a specific artifact — a commit, a defect, a benchmark number, a line from a retro. The principle is *extracted* from the anchor, not decorated with it afterward.
4. **Named sections carry the argument.** Section titles do load-bearing work ("Drift is cheap to introduce, expensive to undo"), not numbering.
5. **Problem → principle → reification.** Show the failure, extract the rule, show the rule generalizing beyond the incident.
6. **"The honest reading" section.** Name the limits: what's aspirational vs. enforced, what the argument does not prove, which bets are still open. This section is what separates an essay from marketing. Never skip it.
7. **What this implies / does NOT imply.** Concrete consequences, flagged speculative vs. actionable — and the most likely misreadings, named so future readers can't mis-cite you.
8. **References** — the journal it grew out of, the sprint, the incident, prior essays.

## Voice

- First person, reflective without arrogance, candid about complicity — including your own failure modes as the author.
- Embed the actual bytes: code snippets, commit messages, dates, numbers. Concrete example over abstraction, always ("a ZK pipeline marked COMPLETE whose proofs don't verify," not "proxies leak").
- Metaphor sparingly but memorably — one good coinage ("scar tissue," "the honesty machine") beats five weak ones.
- Rhythm: short percussive sentences against longer architectural ones.
- Define technical terms on first use; no gatekeeping.

## Triggers worth an essay ("something meaningful happened")

- A rule earned its existence (a failure recurred until a mechanism was cast around it)
- A proxy was caught diverging from the real goal (green tests, wrong behavior)
- A structural bet was made whose payoff won't be known for months — record the reasoning *now*, while it's honest
- Two incidents rhymed across different repos or eras
- Something the method predicted actually happened (or conspicuously didn't)

## Quality gate

- [ ] Epigraph states a defendable claim (not a topic)
- [ ] Opens on a concrete anchor with dates/hashes/numbers
- [ ] "The honest reading" (or equivalent limits section) present
- [ ] "What this does NOT imply" considered
- [ ] Nothing in the essay pretends to be a rule — governance pointers go to CORE_RULES/ADRs
- [ ] References the journal/sprint it grew from
- [ ] Rule-12 frontmatter; canonical path and timestamp
