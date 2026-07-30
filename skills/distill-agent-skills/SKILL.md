---
name: distill-agent-skills
description: Distill reusable Codex skills from conversation histories, project artifacts, corrections, failures, and successful workflows. Use when auditing chats or projects for recurring procedures, updating an existing skill from usage evidence, creating a new skill only when a specialized workflow recurs, validating skill packages, or synchronizing a canonical skill repository with the active Codex skill directory.
---

# Distill Agent Skills

Turn observed work into portable instructions without turning raw history into permanent context.

## Plan before reading sources

1. Define the source boundary, canonical skill repository, staging location, deployment directory, and privacy exclusions.
2. Record the plan before modifying a skill.
3. State interface limits. Never describe a recent or exposed subset as all history.
4. Inventory existing skills before proposing new ones.

Read [evidence-rubric.md](references/evidence-rubric.md) before accepting or rejecting candidates. Use `scripts/inventory_codex_sessions.py` to reconcile local Codex session metadata without copying transcripts.

## Build a source ledger

- Give every conversation or project a stable source identifier.
- Record coverage as complete, partial, inaccessible, irrelevant, or duplicate.
- Read actual turns or artifacts before treating a title as evidence.
- Keep source summaries outside deployed skills.
- Exclude credentials, session tokens, identifiable personal records, private paths, and project source code from reusable content.

## Extract candidates

Look for:

- repeated procedures and tool-routing decisions;
- user corrections that expose stable scope, tone, or approval preferences;
- successful recovery patterns and verified failure causes;
- domain invariants, acceptance tests, and deterministic utilities;
- repeated work that consumes substantial reasoning or is easy to perform incorrectly.

Retain negative evidence. Record what failed, the observed reason, and the guardrail that prevents recurrence. Do not preserve accidental implementation details as general rules.

## Decide the destination

For every candidate, choose one:

1. Update an existing skill when its trigger and conceptual boundary already fit.
2. Add a one-level-deep reference for detailed or conditional guidance.
3. Add a tested script for repeated deterministic mechanics.
4. Create a new skill only when a recurring specialized workflow has a distinct trigger.
5. Reject generic knowledge, unverified claims, temporary state, and one-off preferences.

Resolve contradictions using stronger evidence: explicit correction over inference, verified artifact over recollection, repeated behavior over a single event, and current instruction over stale preference.

## Implement conservatively

- Stage changes in a writable clean copy when the canonical repository has unrelated edits.
- Keep `SKILL.md` imperative, concise, and below 500 lines.
- Put all trigger conditions in the frontmatter description.
- Avoid duplicate guidance across `SKILL.md` and references.
- Update `agents/openai.yaml` when the skill purpose changes.
- Preserve the canonical repository's unrelated changes.

## Validate

For every changed skill:

1. Run `quick_validate.py`.
2. Test every added script on representative and malformed input.
3. Check links, referenced paths, frontmatter, naming, trigger overlap, privacy, portability, and stale UI metadata.
4. Forward-test substantial skills on realistic prompts without leaking intended answers.
5. Fix failures and rerun validation.

## Deploy

Treat the source repository as canonical and the Codex skill directory as a deployed copy.

1. Compare staged changes with the canonical repository.
2. Apply only reviewed skill files.
3. Synchronize the same validated package to `$CODEX_HOME/skills/<skill-name>`, falling back to `~/.codex/skills`.
4. Compare recursive diffs or hashes between source and deployed copies.
5. Report which skills were created, updated, rejected, validated, and installed, plus any coverage gaps.

