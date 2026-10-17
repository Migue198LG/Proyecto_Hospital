# Hospital management system — revised project plan

Status: proposed revision for review, 2026-10-16; updated with the user’s confirmed clarification of D-04: the cashier handles only medications/additional services, while consultation payments by línea de captura and consultation cancellations/refunds are online. The remaining D-10–D-23 proposals are not approved by this clarification. Record the actual approval date and scope when approved; do not label all documents approved automatically.

## Basis and priorities

Preserve D-01–D-09 and all existing RF/RNF/RN/UI/SPEC/CA identifiers. The original PDFs remain the academic authority; [source extraction](../docs/06-source-requirements.md) is the working reference, and [context](../docs/00-context.md) records later team decisions. Record any departure from a source requirement and the instructor validation needed. A plan review is not evidence that the system works.

The first submission is planned for **2026-10-20**, as supplied by the user. Prioritize the rubric: problem statement, business rules, RF/RNF, three context/data-flow diagrams, ER diagram, and Excel data dictionary. SQL Server, consultations, prescriptions, inventory, services, sales, and audits remain project scope even where the second rubric specifically demonstrates appointment insertion. They are not optional stretch work.

Existing working-tree edits must be preserved. Agent files and skills are currently ignored by Git; `.agents/skills` resolves to `../.claude/skills`. Keep that arrangement. Shared engineering procedures needed by teammates must also appear in tracked documentation and scripts.

## Revised proposals D-10–D-23

### D-10 — Stack and a supported database environment

Use Node.js 24 LTS at a maintained patch version, TypeScript, Express, EJS, minimal browser JavaScript, `mssql`, Vitest, ESLint, and Prettier. Pin the runtime major and dependency lockfile. The installed Node 22.14 is an inventory observation, not a reason to freeze an old patch; Node 22 is in maintenance while 24 is the longer-lived baseline. [Node release schedule](https://github.com/nodejs/Release).

Use SQL Server 2022 Developer for the academic development environment. Establish an x86-64 Linux host for the SQL Server container, accessible to the Mac over an authorized private connection. A supported Windows SQL Server installation is the fallback if that is the equipment available. Name the host owner before M3. Do not make Apple Silicon emulation a required development path: `platform: linux/amd64` does not make it supported. Microsoft excludes translation/emulation environments from support. [SQL Server container deployment](https://learn.microsoft.com/en-us/sql/linux/containers/deploy?view=sql-server-ver17).

Before application work, verify a real connection, rollback, persistence across restart, and the selected session-store integration on that host. This is a future readiness check, not a claim about the current machine.

### D-11 — Transactions, migrations, and retries

Keep critical operations in stored procedures with `SET XACT_ABORT ON`, explicit transaction ownership, error handling/rollback, and audit insertion in the same transaction. Use database constraints plus server authorization and parameterized calls. The runtime identity receives only necessary procedure/view permissions; it must not be `sa`, database owner, schema owner, or a schema migration identity.

Use ordered, versioned migrations with an applied-version ledger. Use `CREATE OR ALTER` for programmable objects where appropriate; do not hide schema drift behind blanket “idempotent” existence checks. Generate the rubric's complete SQL build script from a deterministic apply order. Separate runtime, migration, and fixture privileges.

Add durable operation identifiers for booking, payment, refund issuance, and sales. A retry of the same request returns the original result; reuse with a different payload fails. Define uniqueness and retention in the model. Lock resources consistently, bound deadlock retries, and report errors by violated constraint: a duplicate patient/doctor reservation is not always “slot taken.”

### D-12 — Online consultation prepayment and reliable expiration

D-04 confirms consultation prepayment online through a línea de captura, separate from cashier sales of medications/additional services. Propose one full MXN payment for the appointment’s frozen cost, without installments or overpayments. The provider/reference issuer and real-versus-simulated academic integration remain in P-01. A labeled simulator may demonstrate behavior only if selected; it is not a live payment connection. The cashier cannot confirm or reconcile consultation payments.

Propose that eight consecutive hours start at the successful booking’s database-recorded `created_at`; show the exact deadline, línea de captura, amount, and online instructions. P-05 must decide the authoritative payment timestamp and treatment of delayed notifications before production implementation. Verify payment evidence server-side, including reference, amount, currency, and unique transaction ID; a browser success redirect or an uploaded receipt alone must not mark a consultation paid. Never reactivate an expired/canceled appointment automatically when a late payment arrives: its slot may already be reassigned. Record the financial discrepancy for online reconciliation/refund, with execution and exception ownership defined in P-07.

Keep a once-per-minute expiration worker, with startup catch-up, last-success monitoring, and bounded transactional batches. Resolve expired reservations during booking and apply the same rule in availability reads. Online payment processing and expiration must share a locking protocol; once P-05 defines the authoritative timestamp, specify the exact race outcome. Persist provider events separately from appointment status, deduplicate/reconcile notifications, and retain failed or unmatched events for online follow-up. A missed worker or duplicate/late notification must not cause indefinite slot blocking, duplicate collection, or double booking.

### D-13 — Slots, rooms, and schedule changes

Use 30-minute slots on a hospital-wide `:00`/`:30` grid. Represent intervals as start-inclusive/end-exclusive; blocks and appointments cannot cross midnight in v1. Weekly blocks include weekday, start/end, room, and effective dates. Breaks use separate blocks. Unavailability uses dated intervals. Freeze appointment start, end, doctor, specialty, room, price, and policy.

Serialize booking, block edits, and unavailability changes over the same doctor/room resources; lock hints without an indexed access strategy and shared locking protocol are not a concurrency design. Reject schedule, room, specialty, or availability changes that invalidate existing future reservations; resolve affected appointments through the cancellation workflow first. Preserve referenced schedule versions.

Keep filtered unique indexes for active `(doctor_id, start_at)` and `(patient_id, doctor_id)` reservations; add active `(room_id, start_at)`. Propose preventing simultaneous appointments for one patient across different doctors, with an active `(patient_id, start_at)` index. This last restriction is a team proposal beyond RN-03. These keys prevent overlaps only because every slot follows the same fixed grid and duration; validate that precondition in the database. Indexes do not replace schedule validation.

### D-14 — Time and monetary boundaries

Store event instants in UTC as `datetime2(3)` and use database `SYSUTCDATETIME()` as the authoritative clock. Store birth dates as `date` and recurring working hours as local time. Display hospital time in `America/Mexico_City`; explicitly document and verify the SQL Server time-zone mapping. This avoids depending on container-local configuration. [SQL Server UTC clock](https://learn.microsoft.com/en-us/sql/t-sql/functions/sysutcdatetime-transact-sql?view=sql-server-ver17).

Capture one authoritative database time after acquiring the operation’s relevant locks. Booking requires at least 48 elapsed hours; the upper limit is three calendar months from that instant expressed in hospital local time, then converted to UTC. Define end-of-month clamping and test leap years. The online payment timestamp and delayed-notification policy remain P-05; do not substitute notification receipt time for payment time without that decision. Refund bands use elapsed time before the frozen start.

Use `decimal(12,2)` for MXN amounts, positive integer quantities, nonnegative price/stock checks, and an explicit rounding rule: round calculated refunds to two decimals. Never use floating point for totals. Folios are unique but may contain sequence gaps.

### D-15 — Pending appointments and clinical access

Statuses 1 and 2 count as pending under RN-03 after resolving expiration. An appointment alone must not grant perpetual access to a patient's entire record.

Propose: the assigned doctor can read the record for a paid appointment from 24 hours before its start until consultation closure; clinical writes require that paid appointment to have started. After completion, the doctor can read their own consultation and issued prescriptions. Access to the broader record requires another qualifying paid appointment. An unpaid, canceled, or no-show appointment grants no clinical access. Corrections use an explicit linked addendum workflow; appointment outcomes remain final. Enforce patient scope in every read, write, print, and download request.

No patient prescription portal in v1 is a scope proposal, not a consequence of D-09: the doctor's VPN obligation does not logically prohibit a separately authorized patient portal. Track that possible extension under proposed P-17.

### D-16 — Cancellation, outcomes, and refunds

Retain refund bands: at least 48 hours → 100%; at least 24 and less than 48 → 50%; less than 24 hours but before start → 0%. Both patient and doctor cancellation must be committed before appointment start. Doctor-request submission does not reserve the right to a later cancellation; reception approval rechecks time and current state. Reject obsolete requests without changing an appointment already expired, canceled, or completed.

Allowed transitions remain: 1→2 verified online payment system; 1→3 expiration system; 1/2→4 patient or reception online; 1/2→5 reception online by approval or direct cancellation; 2→6 assigned doctor; 2→7 reception. Resolve expiration/payment races under P-05 before applying a transition. A rejected cancellation request leaves the appointment unchanged. Reception’s direct doctor cancellation records reason and acting user. The cashier has no consultation transition permissions.

Completion requires the scheduled start to have passed and a consultation to be closed. Propose no-show only at/after the scheduled end, with no recorded consultation start; lock against concurrent consultation start/closure. No-show gives no automatic refund. Do not allow completion and no-show to race independently.

Cancellation calculates entitlement from the actual confirmed payment; doctor cancellation refunds 100%. Create a pending online refund only when the amount due is positive; preserve zero entitlement in the cancellation audit. Submit an idempotent refund request through the selected online mechanism and mark it executed only after verified evidence; pending, processing, failed, and completed are financial workflow states, not extra appointment statuses. Use a durable request/outbox and reconciliation process: a database transaction cannot make an external refund atomic. Define executor, exception owner, evidence, and timing in P-07; neither cashier nor reception executes monetary refunds. A pending refund does not keep the slot occupied. No sale voids in the academic v1; record that limitation explicitly.

### D-17 — Permissions and accounts

Keep the supplied role allocation with corrected D-04: reception registers doctors/receptionists, reads both audit logs, shares schedule management with admin, and handles authorized online cancellations/doctor approvals. Cashier monetary operations cover only medications and additional services; no consultation payments, cancellations, or refunds. Reception, cashier, and administrator have no clinical content. Reception retains read access to administrative catalog/inventory information shown in S1; catalog editing belongs to administration.

The matrix must specify create/read/update/deactivate/approve/issue/print actions, own-versus-other records, sensitive fields, and network scope. “Manage accounts” must not imply role escalation by reception. Only admin creates cashier/admin accounts; the first admin is provisioned through a documented setup operation. Audit registration and role changes. Disable accounts rather than deleting referenced people; revoke sessions on deactivation or role changes. No hard deletion of referenced catalogs.

One account has one role in v1. Keep patient records separate from login accounts: a reception-registered patient need not have an account. Employee access does not also act as patient access; any future combined-role model requires a separate decision.

### D-18 — Academic pharmacy and sales

Keep unit inventory, admin stock entries, atomic decrements, frozen line prices, and sales to registered patients or named walk-in customers. Aggregate duplicate medication lines before stock validation, lock medications in stable order, and commit sale, payment, stock movements, and receipt reference together. A sale line references exactly one medication or one service; specify this constraint and its FKs.

Medication prescription checks, batches, expiration tracking, sale voids, and tax invoicing are excluded from this fictional academic prototype. This exclusion does not establish real-world dispensing permission. Store no real patient or payment-card data in fixtures. Define stock as a cached balance reconciled against immutable movements, with every entry/decrement recorded in the same transaction. Positive and negative adjustments require explicit reasons and admin permission.

### D-19 — Identity, minors, and historical documents

Keep fictional “Hospital San Mateo,” structured names, birth date, sex, CURP, contact information, employee number/hire date, and doctor license/specialty. Specify field lengths, uniqueness, and optionality in the dictionary; distinguish account login email from patient contact email. CURP validation in the prototype is format validation, not identity verification.

Propose v1 self-service registration for adults only. Reception registers minors with required responsible-adult name, relationship, and phone; reception performs their booking/cancellation. Do not assign a child's account a shared guardian login or require a unique email for every child. Guardian portal access is a future feature. This narrows S1's general patient self-registration wording; record the difference and validate the minors exception with the instructor. Age is calculated on the relevant date; prescription age, doctor license/name, patient name, and clinical text are frozen at issuance so later profile edits cannot alter an issued prescription.

### D-20 — Network boundary and web security

Use Tailscale subject to verifying account eligibility, team/device limits, and the chosen host. Do not promise it is unconditionally free. Propose allowing authorized staff VPN connections from outside hospital facilities; that explicitly resolves the remote-origin part of P-10. All doctor routes and reception/cashier/admin routes use the private entry point.

Expose patient routes through a public entry point and mount protected routes only on the private one. Bind/firewall the private listener to the authorized tailnet path and configure grants for the intended staff and server port. `100.64.0.0/10` membership alone is not proof of an authorized tailnet identity. Document IPv4/IPv6 and any reverse proxy; accept forwarded metadata only from explicitly trusted infrastructure. Keep application sessions, role checks, and record-level authorization after the network boundary. This topology is a design recommendation based on [Tailscale grants](https://tailscale.com/docs/features/access-control/grants), not a tested deployment.

Local bypass is permitted only with an explicit development configuration, loopback binding, and fictional data. Deployment startup fails if bypass is enabled. Use HTTPS, CSRF protection for state changes, output escaping, parameterized queries, login throttling, secure/HttpOnly/SameSite cookies, session regeneration after login, and revocation. Use Argon2id with documented measured parameters rather than making bcrypt the default for new credentials. [OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).

Store server sessions in SQL Server with expiry cleanup; validate the adapter before freezing it. Do not use Express's default MemoryStore outside local development. Set 8-hour absolute lifetime and 30-minute idle timeout for staff, and 8-hour absolute/60-minute idle for patients. [Express session documentation](https://expressjs.com/en/resources/middleware/session/).

Online payment notifications use a dedicated integration endpoint with server-side authenticity checks and replay protection according to the selected provider; they must not be routed through cashier permissions or require a provider to join the staff VPN. Do not expose internal staff routes to enable callbacks.

On VPN loss, the next protected request fails. A request already accepted may still commit even if its response is lost; transactions do not equate disconnection with rollback. Reconnect and query/retry using the operation identifier before repeating any monetary action.

### D-21 — Audit and clinical corrections

Keep both source-required audit logs, procedure-generated inserts, update/delete-denying permissions, and blocking triggers as defense in depth. No application role may alter, truncate, update, or delete them. Do not claim these controls constrain a SQL Server sysadmin who can change the controls themselves. Separate that infrastructure privilege from the application's administrator role.

The scheduler uses an identifiable system actor, not a fictitious patient/doctor. Audit state changes with old/new status, actor, reason, timestamp, and source-required snapshot fields. Distinguish refund entitlement from actual issuance; issuance appends an event. Protect clinical contents while reception sees only the permitted history metadata and opaque prescription reference.

Allergies and previous conditions use child tables with effective/inactive state, author, timestamp, and correction reason. Do not physically delete rows or pretend the consultation-history log captures clinical edits made outside consultation closure. Keep detailed clinical revision records inaccessible to reception. Weight/height belong to consultations; record unknown, not measured, and no known allergies distinctly. Issued prescriptions are immutable; corrections reference the superseded prescription and preserve its original content.

### D-22 — Conventions and artifact ownership

Keep Spanish UI, English primary Markdown with Spanish mirrors, English `snake_case` database identifiers, and versioned Mermaid sources. Change procedure prefix from `sp_` to `usp_`; Microsoft reserves the former convention for system procedures. Keep `fn_`, `vw_`, and `trg_`. [SQL Server procedure naming](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-procedure-transact-sql?view=sql-server-ver17).

Keep `feat/<slug>` branches and one teammate's review for code. Propose also reviewing changes to decisions, permissions, the model, and source interpretations; minor editorial documentation can go directly to `main`. This review task performs no commit or push. Pin diagram/export tool versions rather than fetching an unspecified latest version on every export.

For M1, the dictionary tables in `docs/07-data-model.md` are canonical; generate Excel from a strict, documented table format. Include PK/FK target, type/length, precision/scale, nullability, defaults, uniqueness/checks, and description. Fail on malformed or missing tables instead of silently exporting partial data. Once SQL exists, check schema/dictionary agreement against SQL Server metadata.

### D-23 — Fixtures and rubric coverage

Keep at least 10 specialties, 40 doctors with four per specialty, 10 rooms, 10 services, 20 medications, and 30 patients. “Ten rows where applicable” is not permission to invent ten statuses or arbitrary child records; document exemptions such as the seven fixed appointment statuses and technical metadata tables.

Use deterministic fictional fixtures with a relative-date anchor. Future appointments use business procedures. Historical scenarios may use a privileged fixture loader only on a disposable development database; mark provenance and validate all relationships, statuses, totals, and audits. The ability to insert audit rows does not authorize normal runtime bypass of business rules. Run fixtures twice without duplicating data, and never disable constraints or protective triggers as the routine loading strategy.

## Documentation and model changes

Keep the proposed file inventory, with these adjustments:

| Artifact | Revised requirement |
| --- | --- |
| `docs/00-context.md` | Record approved decisions only after approval. Resolve individual P-10 subquestions explicitly. Preserve resolved P entries and PRN-to-RN history instead of erasing the decision trail. |
| `docs/01-problem-statement.md` | Identify the hospital and operational problems as fictional case assumptions, not observed findings. Tie objectives to RF IDs. |
| `docs/02-requirements.md` | Keep RF/RNF IDs. Refine existing RF-04/RF-07/RF-11 before adding overlapping RF-16/RF-17/RF-18; add new IDs only for genuinely separate requirements. Distinguish consultation measurements from reception's no-show action. |
| `docs/03-business-rules.md` | Full action/data/network matrix; transition guards as well as arrows; refund and expiration boundaries; preserve PRN-01–PRN-06 as superseded aliases if promoted to RN-23–RN-28. |
| `docs/04-view-design.md` | Include empty/error/loading/conflict/permission states. Retire UI-K02/UI-K05 from navigation while retaining historical IDs; UI-P07/UI-P08 cover online consultation payment/refund tracking. Preserve doctor cancellation approval in reception. |
| `docs/05-spec-driven-development.md` | Keep shared commands and definition of done here because ignored agent files will not reach teammates. Distinguish documentation validation from implemented acceptance tests. |
| `docs/06-source-requirements.md` | Preserve source extraction. Change only the explicitly labeled later-team-decisions section, with accurate approval state. |
| `docs/07-data-model.md` | Start with the proposed 26 tables, not a fixed count. Separate consultation financial records from cashier sales; model payment references, verified provider events, refund requests/outbox, and reconciliation. Add effective schedules, optional patient accounts, clinical revisions, deduplication, sessions, and migration metadata as needed; define cardinalities/deletion behavior. |
| `docs/08-architecture.md` | Supported DB host, public/private route separation, trust boundaries, sessions, lock protocol, retries, migrations, least privileges, backup/restore, four views and four functions. Document each view's audience and function inputs/outputs; no nondeterministic clock hidden in rule functions. |
| `docs/09-roadmap.md` | Map every S2/S3 rubric item and S1 scope item to a deliverable, owner, dependency, and verification evidence. Preserve clinical/pharmacy/sales work as required project scope. |
| `docs/diagrams/context-dfd.md` | Level 0: one system process and external entities, including the online payment service (or explicitly labeled simulator). Level 1: processes/stores, separating consultation payments from cashier sales. Level 2: numbered scheduling/online-payment decomposition balanced with its parent. Label data flows. |
| `specs/001-schedule-appointment.md` | Exact time/grid/room/cost rules, expiration on booking, authorization, concurrent booking and schedule edits, durable retries, and confirmation contents. Preserve CA IDs. |
| `specs/template.md` | Decisions applied, scoped CA IDs, error/permission boundaries, and verification status. No automatically “agreed” generated spec. |
| `README.md` | Link deliverables and roadmap; accurately explain local agent files, readiness, and completed versus planned work. |

For the ER rubric, supply both the logical Mermaid ER model (PK/FK/cardinality/optionality) and a conceptual diagram explicitly depicting composite names and multivalued allergies/conditions. A prose table alone may not satisfy “indicate attributes” in the diagram. Keep a notation legend and mapping to child tables. Ask the instructor to confirm level-numbering/notation expectations without delaying the proposed diagrams.

Explain functional dependencies and 1NF/2NF/3NF per relevant entity; distinguish legitimate historical snapshots from uncontrolled duplication. Include blood type, diagnosis, treatment, observations, medication instructions, receipt details, payment/refund uniqueness, and the audit fields required by S1. For prescriptions, decide which fields are free-text clinical snapshots versus optional medication catalog references; a catalog edit must not alter an issued document.

Keep four views and four functions, but replace the proposed cashier consultation-payment view `vw_cashier_pending_payments` with `vw_appointment_payment_status`, available only to authorized online workflows; do not grant it to the cashier. Views alone do not enforce per-patient authorization. `fn_patient_age` accepts an as-of date; `fn_refund_percentage` accepts explicit instants; `fn_doctor_slots` accepts a bounded interval and reference time; `fn_sale_total` calculates from frozen sale lines. Preserve historical age rather than recalculating it at print time.

## Agent setup and automation

After the M1 content is stable, simplify `AGENTS.md`, use the `@AGENTS.md` import in `CLAUDE.md`, and update `SKILLS.md` through `claude-codex-sync`. Preserve `comment-xd` and the exact `/commit-push` trigger. Remove the installer command from project instructions; tool updates are unrelated to routine project work. Do not silently change the existing commit skill through duplicated Claude notes.

Keep `.claude/skills` canonical and `.agents/skills` linked. Codex documents repository skill discovery and symlink support, but loading a file does not prove that the current UI has refreshed. Do not promise that Claude slash-command syntax or hooks run identically in Codex; document the direct script command as the portable fallback. [Official Codex skills documentation](https://learn.chatgpt.com/docs/build-skills).

For `trace-check`, scope definitions to owner documents, resolve aliases/ranges, and namespace acceptance criteria as `SPEC-001/CA-01`. Repeated CA-01 in a different spec is valid. Ignore template placeholders, distinguish references from definitions, and track draft plan IDs separately from approved decision definitions. Check local links, missing mirrors, heading levels/counts, and ID sets. These are structural checks, not proof of correct translation, permission consistency, DFD balancing, or full RF coverage. Add a manual traceability table: source → RF/RN → spec/CA → artifact/test evidence.

For `new-spec`, allocate the next free number without overwriting, validate slugs, keep status draft, and treat keyword references as suggestions needing review. Generate a real Spanish mirror before declaring success; a stub is an incomplete task. Do not make teammates depend on a local-only skill to create a spec.

For `sql-conventions`, incorporate the revised D-11/D-13/D-14/D-21/D-22 rules, including `usp_`, UTC, fixed-grid assumptions, actor scope, and schema/dictionary agreement. `db-apply.sh` and Docker configuration are M3 outputs; do not document them as available before they exist.

Add the three proposed scripts: `trace_check.py`, `data_dictionary_xlsx.py`, and `export-diagrams.sh`. Define the Markdown parser contract and explicit input/output paths. Excel needs an index, styled tables, filters, frozen headers, readable widths, and a deterministic sheet-name mapping within Excel's limits. Reopen the generated workbook and compare every field/row with the source. Export every intended Mermaid block with stable unique filenames; inspect legibility, clipping, and labels. Generation without errors is not sufficient visual verification.

Use one exclusion list for agent-file mirror exclusions in the skill, hook, and checker. Before deleting the three ignored Spanish agent mirrors, inspect them for unique content and preserve any differences. No deletion is performed during this review. Parallel translation, if used during execution, assigns one owner per file and starts only after English sources are stable.

## Milestones and execution order

| Milestone | Target | Deliverable and exit condition |
| --- | --- | --- |
| M1a | October 16–17 | Review decisions, model skeleton, problem/RF/RNF/RN drafts, and rubric coverage; unresolved instructor questions logged. |
| M1b | October 18 | Complete DFD 0/1/2, conceptual/logical ER, dictionary, and generated workbook; reconcile entities, flows, and fields. |
| M1c | October 19 | Spanish mirrors, visual review, structural checks, reproducible artifact export, and team review; reserve time for corrections. |
| M1 | October 20 | First submission package with every S2 item and readable final exports; submission owner records delivery evidence. |
| M2 | By November 1, provisional | Mockups, use cases, sequences, and specs for auth/network, booking, payments/expiration, cancellation/refunds; concrete DB-host readiness check. |
| M3 | After M2; date follows P-14 | Schema/migrations, fixtures, constraints/procs, four views/functions, backup/restore, integration checks, and complete SQL script. |
| M4 | Before second submission | Working login, role/network boundaries, appointment insertion with validations, payment/expiration/cancellation; evidence against acceptance criteria. |
| M5 | P-14, instructor date unknown | S3 rehearsal and submission: use cases, sequences, normalized model, scripts, connection, fixtures, four views/functions, validated insertion. |
| M6 | Required project completion; date to confirm | Consultation/prescription, pharmacy/services/sales, administration and audit interfaces; integrate earlier if required by the instructor's final deadline. |

Execute by dependency: decision review → RF/RN and permission matrix → model/dictionary → DFD/ER → first-submission narrative/spec alignment → Excel/diagram export → mirrors/review. Architecture elaboration and agent automation must not delay M1. File ownership must be assigned before parallel work; until names are provided, use accountable roles rather than pretending “TBD” is assigned.

## Open items and proposed operational targets

- **P-14 (proposed new register entry):** instructor's second-submission date and whether all S1 application workflows are due then. Do not invent late November as a commitment.
- **P-15 (proposed):** actual team names, file/module owners, reviewer, and submission owner. The source caps the team at four; one person may own several areas.
- **P-16 (proposed):** adopt daily full backup, seven-day retention, a separate protected copy, RPO ≤24 hours, and RTO ≤2 hours for the academic environment. Measure a restore before marking RNF-09 verified. This becomes resolved only if the proposal is approved.
- **P-17 (proposed):** optional future patient prescription portal and guardian portal; outside v1 scope, not a blocker for M1.
- **Dependencies to validate:** online payment-reference provider, real-versus-simulated integration (P-01), delayed-event timing/reconciliation (P-05), online refund execution and exception ownership (P-07), supported database host/owner, Tailscale eligibility/limits, and instructor diagram conventions. These are readiness conditions, not silently resolved P-10 details. Do not invent or renumber P-13 to fill a sequence gap.

For RNF-10, propose booking endpoint p95 ≤2 seconds with 10,000 appointments and 20 concurrent users, measured over a documented five-minute workload on a named environment; record error/conflict rates and exclude external payment-terminal time. It is a target, not a benchmark result. For RNF-07, specify keyboard operation, visible focus, labels/error association, contrast and non-color status cues; assess against WCAG 2.2 AA without claiming full conformance from a short checklist. [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/).

## Verification and reporting

For this review, verify only consistency against the repository's source extraction, existing decisions/rules, current identifiers, local Git/skill arrangement, and cited technical documentation. No application, VPN, SQL, export script, or new skill has been implemented or tested by this plan.

During execution, M1 checks cover every rubric item, DFD balancing, ER attributes/cardinality, dictionary/ER agreement, workbook contents/layout, diagram readability, traceability, local links, and Spanish semantic equivalence. `trace-check` success is supporting evidence only.

Before marking implementation verified, test exact time boundaries; month ends; duplicate/retried requests; booking versus booking/schedule edits; payment versus expiry/cancellation; duplicate, reordered, unmatched, and late provider notifications; online refund retry/failure/reconciliation; cashier denied consultation operations; completion versus no-show; concurrent stock consumption; duplicate refunds; direct-route and cross-patient access; public versus private ingress including proxy/IPv6 cases; audit tampering with the runtime identity; worker downtime/catch-up; commit followed by lost response; and restore from backup. Document fixture exceptions and failures honestly.

Report changed artifacts, approval state, open dependencies, and checks actually executed. Do not commit/push without `/commit-push`, and do not describe planned controls as implemented.
