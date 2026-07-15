---
name: revise-reviewer-comments
description: Revise a scientific manuscript and its response letter from journal reviewer or editor comments. Use when addressing peer-review feedback, preparing point-by-point responses, editing or redlining a manuscript, reconciling reviewer requests with the evidence, or producing revised DOCX deliverables while preserving formatting and traceability.
---

# Revise Reviewer Comments

Revise the manuscript and response letter as one evidence-linked package. Resolve each comment explicitly, preserve the authors’ meaning, and never invent analyses, results, citations, approvals, or data.

## Required inputs

Locate the reviewer/editor comments, the latest manuscript, and any existing response letter or supporting files. Identify the target journal, requested file formats, deadline, and whether the authors want tracked changes, clean copy, or both. If a missing input would materially change the revision, ask for it; otherwise proceed and record the assumption.

## Workflow

1. Preserve every source file. Work on copies and do not overwrite the latest author-provided document.
2. Extract all comments into a numbered response matrix. Keep reviewer numbering and wording; split compound comments into addressable subpoints without changing their intent.
3. Classify each subpoint as substantive, editorial, clarification, new analysis/experiment, citation, or out of scope. Mark dependencies and unresolved author decisions.
4. Verify each proposed response against the manuscript, supplied data, and cited sources. Search externally only when authorized or necessary, and cite primary sources. Do not claim that an analysis or experiment was performed unless its result is present and verifiable.
5. Revise the manuscript first. Make the smallest sufficient change, preserve document styles and references, and place changes where readers will find them naturally. Use tracked changes when requested.
6. Draft the response letter second. For each point, include:
   - the reviewer comment, quoted or faithfully paraphrased;
   - a direct, courteous response;
   - the exact manuscript change or a concise quotation from it;
   - the revised location using stable section, heading, table, or figure references, plus page/line numbers only after pagination is final.
7. When disagreeing, acknowledge the concern, explain the scientific reason with evidence, and state any clarifying revision made. Do not use dismissive language.
8. Cross-check that every promised change exists, every manuscript change has a rationale, numbering is complete, citations resolve, and the response letter matches the final manuscript.
9. Render and inspect every final DOCX. Check pagination, tables, figures, headings, references, tracked changes, comments, and accidental formatting drift.

## Substantive-revision naming rule

A revision is substantive when it changes scientific content, interpretation, methods, results, limitations, citations used as evidence, or the response to a reviewer. After such a revision, every output DOCX must have a fresh local datetime suffix:

`<source-stem>_YYYY-MM-DD_HHMMSS.docx`

For example: `manuscript_revised_2026-07-15_143022.docx`.

Do not overwrite an earlier timestamped deliverable. Apply the suffix only after the document has been revised and validated, so the timestamp identifies the completed revision artifact. For a finalized working DOCX, run:

```bash
python scripts/timestamp_docx.py path/to/revised-working.docx
```

Use `--output-dir` to place the timestamped copy elsewhere and `--timestamp` for a reproducible test or user-specified timestamp. Cosmetic-only operations such as opening, rendering, or format verification do not require a new timestamp unless they alter the delivered file.

## Quality gate

Before delivery, confirm:

- all reviewer and editor comments are accounted for exactly once;
- claims in the response match visible manuscript changes;
- no unsupported data, citations, or completed-work claims were introduced;
- requested analyses are either supplied and reported or clearly flagged for author action;
- tone is professional and non-defensive;
- clean and tracked versions, if both requested, contain equivalent scientific content;
- each substantively revised DOCX follows the timestamp naming rule and opens successfully.

Report completed files, unresolved decisions, and any actions that only the authors can perform.
