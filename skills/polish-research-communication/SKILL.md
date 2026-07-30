---
name: polish-research-communication
description: Refine research communication while preserving the author's intended meaning, evidence, scope, and voice. Use for scientific manuscript prose, mathematical formulation and notation, slide narratives, research proposals, abstracts, CV entries, professional research emails, interview scripts, or concise translations between Chinese and English. Trigger when the user asks to polish, rephrase, shorten, reorganize, formalize, make text more natural, align with a journal or presentation style, or evaluate whether wording overstates a claim.
---

# Polish Research Communication

Improve the communication, not the underlying result. Never fill an evidentiary gap with fluent prose.

## Lock the requested scope

Identify:

- genre and audience;
- intended claim;
- terms, numbers, citations, and notation that must remain unchanged;
- requested length and tone;
- whether the user wants evaluation, alternatives, or a final replacement.

When the request is local, edit locally. Do not rewrite surrounding sections, expand content, or introduce a new argument unless asked.

Read [mode-guide.md](references/mode-guide.md) for genre-specific choices.

## Resolve logic before wording

1. Reconstruct the claim as premise, mechanism, result, and implication.
2. Identify repetition, reversed causality, unsupported transitions, or terms used inconsistently.
3. State material conceptual problems before polishing them away.
4. Preserve uncertainty: distinguish observation, interpretation, hypothesis, and future work.
5. Keep user-provided quantitative results exact unless a verified correction is required.

## Edit minimally

- Prefer direct verbs and concrete subjects.
- Remove repeated claims rather than replacing them with synonyms.
- Reduce stacked clauses, excessive colons, semicolons, dashes, and repeated “we”.
- Do not make prose more ornate merely to sound academic.
- Keep technical terminology consistent across equations, prose, figures, and captions.
- Offer multiple versions only when they represent meaningful tone or precision choices.

## Handle mathematical writing

- Define index sets, domains, operators, orientation, and wrapping conventions before use.
- Distinguish equality, definition (`:=`), congruence modulo \(2\pi\), and approximation.
- Use placeholders only after stating what they can instantiate.
- Separate node-, edge-, time-, and interferometric-pair indices visually.
- Verify index bounds and cardinalities.
- Explain whether a quantity is a random variable, realization, observation, or estimator.
- Prefer a clean operator definition over overloaded subscripts when the same transformation applies to several supports.

## Check the final text

Confirm that:

- the meaning did not change;
- no unsupported fact, result, citation, or causal claim was added;
- the output obeys the requested length and section boundary;
- terminology and notation are internally consistent;
- the strongest wording does not exceed the evidence;
- a slide title advances the narrative rather than merely naming the object;
- an email request is explicit without performative over-politeness.

