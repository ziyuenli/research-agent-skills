# Evidence Rubric

## Accept

Accept a candidate when one or more of these conditions holds:

- The workflow recurs in independent tasks.
- An explicit user correction reveals a stable preference or failure mode.
- A successful result depends on non-obvious procedure.
- A project artifact and a conversation independently support the same invariant.
- A deterministic test verifies the proposed rule or utility.

Assign confidence:

- **High:** repeated explicit corrections, reproducible tests, or authoritative artifacts.
- **Medium:** repeated consistent behavior without direct testing.
- **Low:** one plausible instance; defer rather than deploy.

## Reject

Reject:

- raw transcripts or identifiable quotations;
- credentials, tokens, personal records, private paths, and session identifiers;
- facts inferred only from titles or summaries;
- project-specific code or temporary filesystem state;
- generic knowledge Codex already has;
- a stylistic preference contradicted by a later explicit instruction;
- scientific claims without verifiable evidence.

## Candidate record

Record:

| Field | Meaning |
|---|---|
| Source | Stable identifier, not raw content |
| Evidence summary | Minimal paraphrase of the observed pattern |
| Recurrence | Independent occurrence count or artifact support |
| Confidence | High, medium, or low |
| Target | Existing skill, new skill, reference, script, or reject |
| Proposed change | Specific reusable behavior |
| Validation | Structural, deterministic, or forward test |

## Coverage

“Complete” requires a finite enumerated source set and a successful read or explicit status for every item. If an interface caps results without pagination, label the result “complete for the exposed set” and record the unresolved history as inaccessible.

