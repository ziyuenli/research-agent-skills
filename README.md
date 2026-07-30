# Research Agent Skills

This repository contains portable Codex skills for research engineering and one explicit personal collaboration profile. Skills keep reusable instructions concise and place detailed guidance or deterministic utilities in their own resource directories.

## Skills

| Skill | Purpose | Invocation |
|---|---|---|
| Dr. Li Profile | Apply Dr. Li's approval and communication preferences | `$dr-li-profile` |
| Scale Scientific Python | Diagnose and optimize large array, multiprocessing, I/O, graph, and solver workloads | `$scale-scientific-python` |
| InSAR Workflows | Build and validate tool-neutral, GAMMA-aware SAR/InSAR pipelines | `$insar-workflows` |
| Revise Reviewer Comments | Revise manuscripts and response letters with traceable DOCX deliverables | `$revise-reviewer-comments` |

Each skill is stored under `skills/<skill-name>/` with a required `SKILL.md` and UI metadata in `agents/openai.yaml`. Optional `references/` and `scripts/` contain supporting material used only when needed.

## Repository guidance

- `identity.md` defines the research-agent role.
- `principles.md` records the collection's general scientific principles.
- Raw conversations, session identifiers, credentials, private paths, and project-specific source code are not stored here.
- Add a new skill only when a recurring workflow needs specialized instructions or deterministic resources.
