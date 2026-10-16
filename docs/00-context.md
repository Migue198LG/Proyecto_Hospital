# Context and decisions

Status: draft v0.1, 2026-10-12. Working name: Hospital management system.

## Sources and status

| Key | Source | Use |
| --- | --- | --- |
| S1 | `contexto/ESPECIFICACIONES PROYECTO FINAL BASES DE DATOS 26-2.pdf`, five pages | Academic functions, rules, data, and permissions |
| S2 | `contexto/Rúbrica_Eval_Proyecto_1P.pdf` | Deliverables for the first assessment |
| S3 | `contexto/Rúbrica_Eval_Proyecto_2P.pdf` | Deliverables for the second assessment |
| EQUIPO | Conversation with the team on 2026-10-12 | Explicit decisions on scope and working process |

**Confirmed:** comes from an explicit team instruction. **Source:** required by a PDF. **Proposed:** a recommendation still open to revision. **Open:** information not yet decided. The entire package is a draft; extracting a requirement does not mean its final wording has been approved.

## Confirmed decisions

| ID | Decision | Origin |
| --- | --- | --- |
| D-01 | Five roles: patient, doctor, receptionist, administrator, and cashier | EQUIPO |
| D-02 | All interfaces will be web-based; the desktop application is ruled out | EQUIPO |
| D-03 | Receptionists, administrators, and cashiers work with access restricted by VPN | EQUIPO |
| D-04 | The cashier handles payment collection; reception no longer collects payments | EQUIPO |
| D-05 | Specification-driven development using Codex and Claude | EQUIPO |
| D-06 | First Claude Design assignment: general map of the five roles | EQUIPO |
| D-07 | Claude Code and Codex share project skills; updates to Claude's project skills must also be available to Codex | Explicit user instruction, 2026-10-15 |
| D-08 | Use English Markdown document filenames in both language versions; primary documentation is in English with Spanish mirrors. Document 06 extracts project-relevant source content; original PDFs retain their names | Explicit user instruction, 2026-10-16; PDF preservation follows project instructions |

Academic constraint: Microsoft SQL Server (S1, p. 1). The programming language is unrestricted. The specific VPN implementation remains open; the decision to require it is confirmed.

## Scope

Includes accounts and roles, patients, doctors and working schedules, employees, specialties, consultation rooms, appointments with prepayment, cancellations, consultations, medical records, prescriptions, pharmacy, additional services, payment collection, sales receipts, refunds, and audit logs.

Not committed for this version: a real banking payment gateway, insurance providers, inpatient care, telemedicine, tax invoicing, a native mobile application, or a desktop application. These are proposed boundaries, not academic prohibitions.

## Allocation of responsibilities

| Role | Responsibility | Restriction / status |
| --- | --- | --- |
| Patient | Self-registration; personal data and appointments; scheduling and cancellation | S1. Access to their own prescriptions is still undecided |
| Doctor | Schedule, patient care, medical records, prescriptions, and cancellation requests | S1. No self-registration or editing of sensitive data |
| Receptionist | Administrative registration, scheduling, and cancellations; approval of doctors' requests | S1 + D-04. No payment collection, prescriptions, or medical records |
| Cashier | Appointment payments, sales, sales receipts, and refunds | Payment collection confirmed by D-04; detailed permissions proposed |
| Administrator | Accounts, roles, catalogs, inventory, and viewing audit logs | Proposed allocation; S1 only explicitly states the ability to register receptionists |

S1 allows reception to register doctors and other receptionists. Adding an administrator does not automatically remove that permission. Sharing or reassigning those operations must be resolved in P-02. As an initial proposal, cashiers and administrators do not receive access to clinical content solely by holding those roles.

## Open decisions

| ID | Question | Affects |
| --- | --- | --- |
| P-01 | How does the patient pay within 8 hours: at the cashier's desk, by transfer, through a simulation, or through a gateway? Who confirms each method, and what evidence is retained? | Payment workflow; do not offer real online payment in the mockup |
| P-02 | Which registration/editing operations are shared by administration and reception? Who manages working schedules, prices, and inventory? Can a user have multiple roles? | Final permissions matrix |
| P-03 | How long does a consultation last, and how is a working schedule with breaks represented? | Availability, overlaps, and scheduling |
| P-04 | Which statuses count as a pending appointment? Does the doctor see only patients linked to their appointments? Can the patient view their prescriptions? | Permissions and scheduling |
| P-05 | Do the 8 hours begin when the appointment is created? What happens to a payment made exactly at the deadline, or received beforehand but recorded later? Does three months mean calendar months? | Time boundaries |
| P-06 | Is cancellation allowed after the appointment time? Who records Completed/No-show, and when? What happens when a doctor's request is rejected? | Status transitions |
| P-07 | How and when is a refund issued? Is it calculated from the amount paid? Can sales be voided? | Cashier operations |
| P-08 | Does a medication sale require a prescription? Are batches/expiration dates and units tracked? How is initial stock recorded? | Pharmacy; S1 does not establish these rules |
| P-09 | Name, visual identity, and required personal fields. Are minors and guardians handled? | Mockups and forms |
| P-10 | Stack, deployment, VPN topology, logout, and behavior if the VPN connection is lost during an operation | Technical design and internal access |
| P-11 | How are consultation rooms reserved, and how are overlaps prevented between doctors sharing one? | Scheduling; proposed additional rule |
| P-12 | Which clinical actions require later corrections, and how is their history preserved? Who can view each audit log? | Medical records, prescriptions, and auditing |

Mockups can represent open questions as explicit alternatives; a visual option does not resolve them by itself. Define P-01/P-02/P-03 before detailing the corresponding operational workflows.

## Next cycle

1. Review the problem statement, RF/RNF, and rules with the team.
2. Create the general map and navigation for five roles in Claude Design.
3. Record findings from the mockup; resolve open questions that affect the next workflow.
4. Specify scheduling and its payment; then create the data model and technical design.
