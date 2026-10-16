# Hospital management system — initial documentation

Status: draft v0.1. Date: 2026-10-12.

Academic project to manage appointments, consultations, prescriptions, medications, services, and payments with Microsoft SQL Server. All five role interfaces will be web-based: patient, doctor, receptionist, cashier, and administrator. Receptionists, cashiers, and administrators will access the system through a VPN.

## Start here

1. [Context, agreements, and open questions](docs/00-context.md).
2. [Problem statement and objectives](docs/01-problem-statement.md).
3. [Functional and non-functional requirements](docs/02-requirements.md).
4. [Business rules](docs/03-business-rules.md).
5. [View map and brief for Claude Design](docs/04-view-design.md).
6. [Practical guide to specification-driven development](docs/05-spec-driven-development.md) and [first feature example](specs/001-schedule-appointment.md).

The original PDFs are preserved in `contexto/`. [Project requirements from the original sources](docs/06-source-requirements.md) collects their scope, requirements, rules, data, and assessment deliverables in English, with a [Spanish version](espanol/docs/06-source-requirements.md). It omits institutional headings and page footers; use `docs/00-context.md` alongside it for later team decisions. The documents written here provide a basis for team review; they do not automatically approve the proposals.

Markdown document filenames are in English in both language versions. Primary documentation is in English; `espanol/` contains its Spanish counterpart with matching filenames. Original PDF filenames are preserved.

## Specification-driven development workflow

Work on small features. For each one: **need → specification → mockup → revisions → technical plan → implementation → verification**. Mockups can begin now and help uncover requirements. Documentation is updated when a decision changes.

| Stage | Output | Status |
| --- | --- | --- |
| Context and scope | Recorded agreements, owners, and questions | Foundation created; review pending |
| Basic documentation | Problem statement, RF, RNF, and business rules | Drafts created |
| Interface exploration | General map of five roles and mockups | Brief prepared; mockups pending |
| First academic submission | Context diagrams 0/1/2, entity-relationship diagram, and data dictionary, along with the basic documentation | Pending |
| Functional and data design | Use cases, sequences, and normalized relational model | Pending |
| Technical design | Architecture, authentication, VPN, contracts, and SQL scripts | Pending; stack not selected |
| Implementation by workflow | Login and scheduling with validations first | Pending |
| Second academic submission | Scripts, connection, test data, four views, four functions, and scheduling from the application | Pending |

The academic deliverables were taken from the original rubrics; preparing mockups alone does not fulfill them.

## Context for agents

- `AGENTS.md`: shared project instructions and entry point for Codex.
- `CLAUDE.md`: imports the same instructions for Claude Code.
- `SKILLS.md`: shared procedures; `.agents/skills` links to `.claude/skills/` so both agents read the same project skills. Use `claude-codex-sync` to check or repair this arrangement.
- `docs/`: shared functional context; read only documents relevant to the task.
- `specs/template.md`: lightweight format for specifying a feature when work on it begins.
- `specs/001-schedule-appointment.md`: draft example for learning the cycle before implementation.

An assignment to an agent must include: objective, relevant RF/RN, files to modify, scope, relevant open questions, and how to verify the result. Both agents can implement or review; the team assigns responsibilities per task.

## First step in Claude Design

Attach the original PDF `contexto/ESPECIFICACIONES PROYECTO FINAL BASES DE DATOS 26-2.pdf` along with `docs/00-context.md`, `docs/02-requirements.md`, `docs/03-business-rules.md`, and `docs/04-view-design.md`. Copy the prompt from the last document. The PDF preserves the academic requirements; the Markdown files distinguish the team's later decisions from proposals. If a discrepancy appears, record it for review. The initial assignment is a **general map of the five roles**, not system development.

Afterward, incorporate the design export, decisions made, and open questions into the project. Link screen names to their `UI-*` identifiers before assigning their implementation.

## October 20

- Problem statement
- Functional requirements
- Non-functional requirements
- Context diagram
- Entity–relationship model
- Data dictionary

## References

- [Academic specifications](contexto/ESPECIFICACIONES%20PROYECTO%20FINAL%20BASES%20DE%20DATOS%2026-2.pdf).
- [First rubric](contexto/Ru%CC%81brica_Eval_Proyecto_1P.pdf).
- [Second rubric](contexto/Ru%CC%81brica_Eval_Proyecto_2P.pdf).
- [Codex instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
- [Claude Code context and imports](https://code.claude.com/docs/en/memory).
- [Claude Design prototypes and handoff](https://academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux).
