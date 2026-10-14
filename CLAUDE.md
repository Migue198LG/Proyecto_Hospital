# Context for Claude Code
# Shared project instructions

## Context

Current stage: basic documentation and exploration of views. Read `README.md` and `docs/00-contexto.md` when starting a task; after that, read only the necessary specifications.

Team agreements: five roles (patient, doctor, receptionist, cashier, and administrator), a fully web-based application, VPN access for receptionist/cashier/administrator, and payment collection handled by the cashier. Microsoft SQL Server is an academic requirement. The stack, VPN provider, and payment method have not yet been decided.

## Specification-driven work

- The documents distinguish source requirements, confirmed decisions, proposals, and open questions. Do not turn proposals or design assumptions into team decisions.
- Consult RF/RNF in `docs/02-requerimientos.md` and RN in `docs/03-reglas-negocio.md`. Keep identifiers stable and link changes to those IDs.
- For a new feature, use `specs/plantilla.md` with scope, actors, rules, acceptance criteria, and relevant questions. A specification can be short.
- If the user has already authorized a decision, incorporate it into `docs/00-contexto.md` and update the affected documents. If it changes an academic rule, record the difference and the point to validate with the instructor.
- When a missing business decision would change the outcome, identify the open question and continue with independent work. Do not silently fill in that rule.
- Mockups use fictional data. Document visual decisions, empty states, errors, and permissions for each screen. The prototype does not demonstrate that permissions, the VPN, or the rules are implemented.
- Before writing production code, define the task's behavior and acceptance criteria. Verify relevant rules and boundaries, not just the happy path.
- Keep the PDFs in `contexto/` as original sources. Update the derived documentation without modifying those PDFs.
- Do not choose tools, frameworks, or infrastructure as part of a mockup task unless the user asks for it.
- When several tasks run in parallel, agree on an owner for each file and communicate dependencies. Do not overwrite another collaborator's changes.

## Permissions that must be preserved

- Reception does not collect payments or process monetary refunds; the cashier performs those operations.
- Reception cannot view prescriptions or medical records.
- Doctors cannot register themselves or modify their sensitive data; their cancellation requests require reception's approval.
- Audit logs: read and insert only; no one may update or delete entries. Inserting events through system operations is proposed.
- The VPN complements authentication and role-based authorization; these must be enforced on the server.

## Deliverables

Briefly communicate what changed, what remains open, and what was verified. Do not claim that something is approved, tested, connected, or implemented when it is only documented or mocked up.
