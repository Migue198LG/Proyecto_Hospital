# Practical guide: developing this project with specifications

Status: initial working guide, 2026-10-12. Read after `README.md` and `docs/00-context.md`.

## Core idea

Describe **what must happen and how to verify it** before deciding **how to program it**. Each functional change must be traceable from its source to verified behavior. The specification remains a living document: when the team learns something during mockup design or implementation, it updates the corresponding document and then adjusts design, code, and tests.

The process resembles the *Specify → Plan → Tasks → Implement → Converge* workflow from [GitHub Spec Kit](https://github.com/github/spec-kit/blob/main/docs/index.md). This project uses a lightweight Markdown version; it does not depend on installing Spec Kit or choosing a framework now.

## Two levels of specification

1. **Project level:** `docs/00-context.md` records decisions and open questions; `01-problem-statement.md` explains the problem; `02-requirements.md` collects RF/RNF; `03-business-rules.md` contains RN; `04-view-design.md` identifies screens. The PDF in `contexto/` is the original academic source.
2. **Feature level:** a file in `specs/` details a journey a person can complete or a system operation. Example: `specs/001-schedule-appointment.md`. It is created from `specs/template.md`, with references to global IDs, acceptance criteria, edge cases, and open questions.

The project document changes when a shared rule or decision changes. A feature spec changes when that feature's behavior changes. A mockup replaces neither.

## Cycle for each feature

| Step | Question it must answer | Evidence retained |
| --- | --- | --- |
| 1. Define scope | Who needs to do what, and what is out of scope? | Need, actors, and scope in the spec |
| 2. Specify | Which rules, inputs, outputs, states, and permissions apply? | RF/RN references and observable workflow |
| 3. Clarify | Which decision is missing for two people to implement the same behavior? | P-* resolved in `00-context.md` or identified as blocking that part |
| 4. Mock up | How will each role see and complete the journey? | Prototype with UI-* IDs, states, and errors |
| 5. Plan | Which data, contracts, transactions, and components are needed? | Technical plan for that feature; stack only once agreed |
| 6. Break down | Which small tasks can be built and verified? | Task list with owners and dependencies |
| 7. Implement | Does the application meet each criterion, including a rejection case? | Code, schema, and necessary tests |
| 8. Converge | Do the PDF, decisions, spec, mockup, code, and tests agree? | Traceability review and closed open questions |

A prototype can be created before all open questions are resolved: it helps uncover questions. Only behaviors to be implemented need precise definitions. Avoid accidentally turning a visual option into a business rule.

## Traceability example

```text
Specifications PDF, p. 1: at least 48 hours in advance
  → RN-01: boundary for requesting an appointment
  → RF-05: scheduling with valid availability
  → UI-P03: date and time slot selection
  → SPEC-001 / CA-02: a date earlier than the minimum is rejected
  → test: the server rejects the request and does not create the appointment
```

The screen helps prevent an error; the rule must also be enforced when the request reaches the server directly. When adding a change, review connected references before declaring the task complete.

## Exercise with the current project

1. Read [the sample scheduling specification](../specs/001-schedule-appointment.md). Separate what is confirmed from P-03/P-04/P-05/P-11.
2. Compare its criteria with the UI-P03/UI-P04 mockup from Claude Design. Note missing fields or states.
3. Resolve with the team the questions that affect the appointment before the technical plan: duration, what a pending appointment means, time boundaries, and consultation room allocation.
4. Create the first implementable spec for the agreed workflow. Then decide on architecture and schema for that workflow, rather than the entire hospital at once.
5. Ask Codex or Claude Code for a task plan citing CA-* criteria, and check the tasks before implementation.

**Review prompt for an agent, before programming:**

```text
Read the context PDF, docs/00-context.md, docs/02-requirements.md,
docs/03-business-rules.md, and specs/001-schedule-appointment.md.
Review the spec against the source: identify contradictions, rules without
acceptance criteria, criteria without a source, and P-* decisions still needed.
Propose concrete corrections to the document. Do not choose a stack or write code.
```

**Planning prompt, after resolving the open questions that affect the workflow:**

```text
Read the agreed spec and the UI-P03/UI-P04 design approved by the team.
Propose a plan and small tasks to implement each CA-* with SQL Server.
Identify the data model, server operations, validations,
authorization, concurrency, and relevant tests. Use only the stack
recorded as a project decision; flag any gaps.
```

## How to divide work without losing context

Claude Design explores the interface and records visual decisions. Codex and Claude Code can review a spec, plan, implement, or verify; each task must name the same files and criteria. When two people or agents work at the same time, assign owners by file or module and agree on the contract between their tasks before making dependent changes.

At the end of a task, the result must state which RF/RN/CA it covers, what was verified, and what remains open. The team incorporates any new decision into `docs/00-context.md`, then updates the affected spec, mockup, and code. Keeping these documents under version control will make it possible to review who changed a rule and why.

## Recommended order now

1. Review the draft problem statement, RF/RNF, and RN as a team. Identify what comes from the PDF and what is proposed.
2. Obtain the general map of five roles and six initial views in Claude Design, using `docs/04-view-design.md`.
3. Prepare the context diagrams, entity-relationship diagram, and data dictionary from the first rubric; resolve business questions that affect those models.
4. Refine `SPEC-001` and choose the stack when planning its implementation.
5. Implement and verify a small journey first: registration/login, scheduling, appointment confirmation document, and payment confirmation according to the agreed method.
6. Continue with cancellations, consultation/prescription, sales/inventory, administration, and audit logs, each with its own spec and criteria.

Steps 2 and 3 can progress at the same time with cross-review: the mockup can reveal data missing from the model, and the model can reveal interface questions. The second rubric requires scheduling an appointment from an application or website with validations; this is why the journey deserves early attention.

## Shared scripts and checks

Agent configuration files (`AGENTS.md`, `CLAUDE.md`, `SKILLS.md`, `.claude/`, `.agents/`) are local and not versioned, so the procedures teammates need live here and in `scripts/`. The scripts need only Python 3 and Bash; run them from the repository root.

| Command | Purpose | What it does not prove |
| --- | --- | --- |
| `python3 scripts/trace_check.py` | Checks that every cited RF/RNF/RN/PRN/UI/D/P/SPEC/CA identifier is defined in its owner document, that local links resolve, that every English `.md` has its `espanol/` mirror with the same heading structure and identifiers, and lists identifiers that exist only in `plans/` as proposals | Correct translation, permission consistency, diagram balancing, or complete requirement coverage; those need a manual review |
| `scripts/new_spec.sh <slug> ["Name"] ["Nombre"]` | Creates `specs/NNN-<slug>.md` and `espanol/specs/NNN-<slug>.md` from both templates with the next free number and status draft | That the references are right; take them from the owner documents and review them |

Definition of done for a documentation task: the owner document defines any new identifier, the affected documents cite it, the Spanish mirror is updated, `trace_check.py` reports no errors, and the delivery states what remains open. For implementation tasks, add the acceptance criteria executed and their evidence; a passing structural check is not a functional test.

Paths without a Spanish mirror are listed in `scripts/mirror-exclusions.txt`, the single list used by the check and by the Claude Code hook.
