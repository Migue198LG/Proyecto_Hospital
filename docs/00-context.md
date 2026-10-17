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
| D-03 | Receptionist, administrator, and cashier functions are restricted to the hospital's private network through a VPN | EQUIPO; network scope clarified by the user, 2026-10-16 |
| D-04 | The cashier collects only medication and additional hospital-service payments. Consultations are prepaid online using a payment reference (línea de captura); appointment payments, cancellations, and associated refunds are managed online, outside the cashier workflow. Reception does not collect payments | EQUIPO; explicit user clarification, 2026-10-16 |
| D-05 | Specification-driven development using Codex and Claude | EQUIPO |
| D-06 | First Claude Design assignment: general map of the five roles | EQUIPO |
| D-07 | Claude Code and Codex share project skills; updates to Claude's project skills must also be available to Codex | Explicit user instruction, 2026-10-15 |
| D-08 | Use English Markdown document filenames in both language versions; primary documentation is in English with Spanish mirrors. Document 06 extracts project-relevant source content; original PDFs retain their names | Explicit user instruction, 2026-10-16; PDF preservation follows project instructions |
| D-09 | Doctors must use the same hospital-network VPN access for consultation functions: patient care, patient/clinical data, medical records, diagnoses, treatments, and prescriptions | Explicit user instruction, 2026-10-16 |

Academic constraint: Microsoft SQL Server (S1, p. 1). The programming language is unrestricted. The specific VPN implementation remains open; the decision to require it is confirmed.

## Hospital network and VPN access

D-03 and D-09 restrict reception, administration, cashier operations, and the doctor's consultation functions to the hospital's private network through an authorized VPN connection. These protected functions must not be directly accessible from the public Internet, even with valid application credentials.

For doctors, the restriction covers reading patient and clinical data during care, viewing medical records, recording the consultation, diagnoses and treatments, and issuing or viewing prescriptions (RF-11/RF-12; UI-D02/UI-D03/UI-D04). This decision does not automatically extend the same restriction to every doctor function: the network policy for the schedule, profile, and cancellation requests remains to be defined in P-10.

VPN access complements application authentication and role authorization; the server must enforce both. A VPN connection alone does not grant clinical permissions or remove reception's prohibition on viewing prescriptions and medical records. This is a documented requirement, not an implemented control.

P-10 must distinguish access to the hospital network from physical presence at the hospital: it is still undecided whether the VPN may accept connections originating outside the facilities. Provider, topology, and behavior on connection loss also remain open. D-03/D-09 are team decisions in addition to the academic source, which does not specify a VPN.

## Scope

Includes accounts and roles, patients, doctors and working schedules, employees, specialties, consultation rooms, appointments with prepayment, cancellations, consultations, medical records, prescriptions, pharmacy, additional services, payment collection, sales receipts, refunds, and audit logs.

Online consultation prepayment through a payment reference (línea de captura) and online cancellation/refund management are confirmed by D-04. The provider, verification/reconciliation mechanism, and whether the academic demonstration uses a real integration or an explicitly labeled simulation remain open in P-01/P-05/P-07. These flows do not involve the cashier. Doctor cancellation still requires reception’s approval through the web application (RN-08).

Not committed for this version: insurance providers, inpatient care, telemedicine, tax invoicing, a native mobile application, or a desktop application. These are proposed boundaries, not academic prohibitions.

## Allocation of responsibilities

| Role | Responsibility | Restriction / status |
| --- | --- | --- |
| Patient | Self-registration; personal data and appointments; scheduling and cancellation | S1. Access to their own prescriptions is still undecided |
| Doctor | Schedule, patient care, medical records, prescriptions, and cancellation requests | S1. No self-registration or editing of sensitive data; consultation functions require hospital-network VPN access (D-09) |
| Receptionist | Administrative registration, scheduling, and cancellations; approval of doctors' requests | S1 + D-04. No payment collection, prescriptions, or medical records |
| Cashier | Medication and additional-service sales, payment collection, and sales receipts | D-04; no consultation payments, consultation cancellations, or associated refunds |
| Administrator | Accounts, roles, catalogs, inventory, and viewing audit logs | Proposed allocation; S1 only explicitly states the ability to register receptionists |

S1 allows reception to register doctors and other receptionists. Adding an administrator does not automatically remove that permission. Sharing or reassigning those operations must be resolved in P-02. As an initial proposal, cashiers and administrators do not receive access to clinical content solely by holding those roles.

## Open decisions

| ID | Question | Affects |
| --- | --- | --- |
| P-01 | Online consultation prepayment through a línea de captura is confirmed (D-04). Which provider issues/verifies the reference, what evidence is retained, and is the academic integration real or simulated? | Online payment integration; mockups must not claim a live connection |
| P-02 | Which registration/editing operations are shared by administration and reception? Who manages working schedules, prices, and inventory? Can a user have multiple roles? | Final permissions matrix |
| P-03 | How long does a consultation last, and how is a working schedule with breaks represented? | Availability, overlaps, and scheduling |
| P-04 | Which statuses count as a pending appointment? Does the doctor see only patients linked to their appointments? Can the patient view their prescriptions? | Permissions and scheduling |
| P-05 | Do the 8 hours begin when the appointment is created? Which verified timestamp determines timely online payment, and how are late notifications or money received after expiration reconciled without double booking? Does three months mean calendar months? | Time boundaries and online reconciliation |
| P-06 | Is cancellation allowed after the appointment time? Who records Completed/No-show, and when? What happens when a doctor's request is rejected? | Status transitions |
| P-07 | Consultation refunds are managed online, outside the cashier workflow (D-04). What provider/process executes them, with what timing, evidence, calculation base, and exception owner? Separately, can medication/service sales be voided? | Online consultation refunds; separate sales policy |
| P-08 | Does a medication sale require a prescription? Are batches/expiration dates and units tracked? How is initial stock recorded? | Pharmacy; S1 does not establish these rules |
| P-09 | Name, visual identity, and required personal fields. Are minors and guardians handled? | Mockups and forms |
| P-10 | Stack, deployment, VPN provider/topology, whether VPN connections may originate outside hospital facilities, network policy for the doctor's non-clinical functions, logout, and behavior if the VPN connection is lost during an operation | Technical design and hospital-network access; D-03/D-09 define the protected functions |
| P-11 | How are consultation rooms reserved, and how are overlaps prevented between doctors sharing one? | Scheduling; proposed additional rule |
| P-12 | Which clinical actions require later corrections, and how is their history preserved? Who can view each audit log? | Medical records, prescriptions, and auditing |

Mockups can represent open questions as explicit alternatives; a visual option does not resolve them by itself. Define P-01/P-02/P-03 before detailing the corresponding operational workflows.

## Next cycle

1. Review the problem statement, RF/RNF, and rules with the team.
2. Create the general map and navigation for five roles in Claude Design.
3. Record findings from the mockup; resolve open questions that affect the next workflow.
4. Specify scheduling and its payment; then create the data model and technical design.
