# General map and brief for Claude Design

Status: draft v0.1, 2026-10-12. Confirmed objective D-06: explore the general map of the five roles. Mockups are pending; this document is the design assignment.

## What to deliver first

1. Navigation map for the five profiles and the points where their tasks connect.
2. Low-fidelity mockups of login and one main screen per role: six initial views.
3. Minimal navigable prototype connecting the initial views, with fictional data.
4. Inventory of secondary screens and a list of decisions/questions discovered.

If a role selector is used to present the prototype, it must indicate **demonstration mode**. In production, access depends on the authenticated account; the selector does not grant permissions.

After reviewing the map, detail one workflow at a time. Do not design every screen with final polish in the first iteration.

## Agreements the mockup must preserve

- Everything is web-based. Patient: mobile and computer. Doctor: computer/tablet. Reception, cashier, and administration: web interfaces focused on computer use.
- Reception, cashier, and administrator functions require VPN access to the hospital's private network. The same restriction applies to the doctor's consultation, medical record, and prescription views (UI-D02/UI-D03/UI-D04; D-09). Without VPN access, show the access-denied state without patient or clinical content. The prototype only represents the behavior; policy for other doctor views remains in P-10.
- Reception manages scheduling and online cancellation approvals. Consultation prepayment by línea de captura, cancellations, and refunds are managed online without cashier intervention (D-04). The cashier collects only medication and additional-service payments. Cancellation does not mean a refund has already been executed.
- Reception has no prescriptions, medical records, or payment collection actions.
- Doctors cannot register themselves or edit their name, CURP, professional license number, employee number, or specialty. They request cancellation for reception's approval.
- There is no Reschedule button. Canceling and requesting a new appointment are separate operations.
- Scheduling: specialty/cost → doctor → date → time slot → review → appointment confirmation document with a línea de captura for online prepayment and an 8-hour deadline.
- Dates from 48 hours to three months in advance; available time slots within the working schedule; no other pending appointment with the same doctor.
- The online consultation channel is confirmed; the provider, verification mechanism, and real-versus-simulated integration remain open (P-01/P-05/P-07), as do detailed administrator permissions and inventory rules. Do not turn a visual control into a business decision.

## Proposed navigation

| Profile | Main menu | Landing view |
| --- | --- | --- |
| Patient | Home, Schedule, My appointments, My data | Next appointment and payment deadline, if applicable |
| Doctor | Schedule, Consultations, Prescriptions, Requests, My profile | Today's schedule |
| Receptionist | Home, Schedule, Patients, Staff, Cancellations | Appointments and pending requests |
| Cashier | Home, Sales, Receipts, Stock | Medication and additional-service sales |
| Administrator | Home, Users, Catalogs, Pharmacy, Services, Audit logs | Proposed administrative summary |

The placement of functions in menus is proposed. Permissions for shared administrative registration operations must be resolved in P-02.

## View inventory and traceability

IDs are preserved even if names change. A view can be implemented as a page, tab, or dialog; that decision is validated through the mockup.

| ID | View | Content and main action | References |
| --- | --- | --- | --- |
| UI-C01 | Login | Credentials, account-based access, patient registration link | RF-01 |
| UI-C02 | Patient registration | Personal and access data; fields pending | RF-02; P-09 |
| UI-C03 | Internal access unavailable | Explain the VPN restriction and allow retrying; also represent an expired session | RNF-03; P-10 |
| UI-P01 | Patient home | Next appointment, status, payment deadline, and access to scheduling | RF-06/08 |
| UI-P02 | My data | View personal details; editing only if agreed | RF-02; P-09 |
| UI-P03 | Schedule appointment | Steps for specialty, doctor, date, time slot, and review | RF-05; RN-01/02/03/04 |
| UI-P04 | Appointment confirmation | Reference number, appointment data, línea de captura, deadline, and online prepayment instructions; no cashier step | RF-06; D-04; P-01 |
| UI-P05 | My appointments and details | Date/status filters, confirmation document, cancellation, and history | RF-08/09 |
| UI-P06 | Confirm cancellation | Applicable policy and estimated refund before accepting online; link to refund tracking | RF-09/10; RN-07; D-04 |
| UI-P07 | Online consultation payment | Línea de captura, amount, deadline, payment instructions, and verified status; integration not yet selected | RF-07; D-04; P-01/P-05 |
| UI-P08 | Online consultation refund tracking | Entitlement, processing, verified execution or failure; no cashier visit | RF-10; D-04; P-07 |
| UI-D01 | Doctor schedule | Day/week, patients, time slots, and consultation rooms | RF-08 |
| UI-D02 | Consultation | Appointment/patient data, clinical information, and care outcome; requires hospital-network VPN access | RF-11; RNF-03; D-09; P-06 |
| UI-D03 | Medical record | Allergies, blood type, medical history, weight, height, and consultations; requires hospital-network VPN access | RF-11; RNF-03; D-09; P-04/P-12 |
| UI-D04 | Prescriptions | List, issuance, and printable view; requires hospital-network VPN access | RF-12; RNF-03; D-09 |
| UI-D05 | My profile | Sensitive data for viewing and working schedule | RN-12/13 |
| UI-D06 | Cancellation requests | Submit a request and track reception's response | RF-09; RN-08 |
| UI-R01 | Reception home | Today's schedule and cancellation requests | RF-08/09 |
| UI-R02 | General schedule | Filters by doctor, specialty, consultation room, and date; appointment creation and details | RF-05/08/09 |
| UI-R03 | Patients | Search, registration, administrative record, and appointments | RF-02/08; RN-14 |
| UI-R04 | Staff | Register/view doctors and receptionists; working schedules according to agreed permissions | RF-03/04; RN-11/15; P-02 |
| UI-R05 | Cancellations | Doctors' requests, approval, and patient cancellations | RF-09; RN-07/08 |
| UI-K01 | Cashier home | Medication/additional-service sales and proposed daily summary; no consultation payments | RF-14; D-04 |
| UI-K02 | Retired: appointment payments at cashier | Historical identifier retained; excluded from navigation and permissions; online replacement UI-P07 | D-04; RF-07 |
| UI-K03 | Sale | Medications/services, quantities, total, and payment collection; customer without an account | RF-14; RN-16/22 |
| UI-K04 | Sales receipts | View and retrieve receipts again | RF-14; reprinting proposed |
| UI-K05 | Retired: consultation refunds at cashier | Historical identifier retained; excluded from navigation and permissions; online tracking UI-P08 | D-04; RF-10 |
| UI-K06 | Stock | View available medications, without clinical content | RF-13; proposed permissions P-02 |
| UI-A01 | Administrator home | Administrative summary; metrics to validate | Proposal; RF-08/13/15 |
| UI-A02 | Users and employees | Accounts, profiles, and access; permissions to resolve | RF-03; P-02 |
| UI-A03 | Catalogs | Specialties/costs, consultation rooms, and working schedules according to P-02 | RF-04 |
| UI-A04 | Pharmacy | Medications, prices, inventory, and proposed stock entries | RF-13; P-02/P-08 |
| UI-A05 | Services | Catalog and prices for additional services | RF-14; RN-18; P-02 |
| UI-A06 | Audit logs | Filters and activity viewing; no editing/deleting or opening clinical content by default | RF-15; RN-17; P-12 |

Do not give administrators all access by default: their detailed matrix must be agreed. Their expanded functions in this inventory are proposals.

## Relationships between profiles

- **Appointment:** patient or reception schedules → confirmation document/línea de captura/deadline → patient pays online → system verifies payment → doctor views the schedule and provides care.
- **Expiration:** appointment without confirmation within the deadline → cancellation for nonpayment → slot becomes available. The actual automatic process is designed later.
- **Doctor cancellation:** doctor requests online → reception decides online → if approved, appointment canceled with 100% refund entitlement → online refund processing and verified result; no cashier intervention.
- **Patient cancellation:** patient or reception cancels online → calculation according to policy → online refund processing and verified result, when applicable.
- **Sale:** cashier selects medication/service → records payment and sales receipt → inventory is updated according to rules to be validated.
- **Administration:** maintains the catalogs and accounts used by other profiles, according to permissions still to be agreed.

The online prepayment channel is confirmed (D-04). Do not require a cashier visit for consultation payment/cancellation/refund, or claim a live payment integration while P-01 remains open. Doctor approvals by reception remain in the online workflow.

## States to explore

| Area | States and variants |
| --- | --- |
| Common | Loading, empty, error, expired session, access denied by role/VPN |
| Schedule | With appointments, no appointments, no time slots, slot taken during confirmation, invalid date |
| Patient | No upcoming appointment, awaiting payment, paid, expired, canceled, completed, no-show |
| Cancellation | Refund of 100/50/0%; doctor's request pending/approved/rejected, as a proposal |
| Cashier | Sale/receipt not found, sale already collected, sale without items, insufficient stock; no consultation-payment/refund actions |
| Online consultation payment/refund | Invalid or expired línea de captura, awaiting verification, duplicate/late notification, payment failure, refund pending/processing/completed/failed; detailed reconciliation in P-01/P-05/P-07 |
| Doctor | Patient with no medical history, recorded allergy, new prescription, and existing prescription |

The error states shown are design scenarios; they must be linked to acceptance criteria before implementation. Do not create new appointment statuses without updating their specification.

## Provisional visual direction

Interface in Spanish, readable and restrained; operational content first. Consistent components across profiles: search controls, forms, tables, appointment cards, status labels, and confirmations. Labels include text, not just color.

Brand, palette, and typography will be chosen later. Use a working name and fictional data. Do not add photographs or decoration that compete with schedules and forms. Currency, dates, and example fields are for demonstration until their formats are agreed.

## Initial prompt to copy into Claude Design

```text
We are designing an academic hospital management system project at an early stage. We want to explore navigation and content layout before developing the system.

Read the original PDF “ESPECIFICACIONES PROYECTO FINAL BASES DE DATOS 26-2.pdf” and the four attached derived documents: 00-context.md, 02-requirements.md, 03-business-rules.md, and 04-view-design.md. Use the PDF to check the academic requirements; the Markdown files also record the team's later decisions. Distinguish confirmed decisions from proposals and open questions. If you find a discrepancy, flag it for review. Preserve UI/RF/RN IDs so design and specifications can be linked.

The entire application is web-based and has five roles: patient, doctor, receptionist, cashier, and administrator. Reception, cashier, and administration require VPN access to the hospital's private network. Doctors require the same access for consultation, medical record, and prescription functions (UI-D02/UI-D03/UI-D04); without it, show access denied without clinical content. The network policy for other doctor functions remains open in P-10. The patient interface needs mobile adaptation; the other profiles need a comfortable computer layout, and the doctor also needs a tablet layout.

First create the general navigation map for the five roles and low-fidelity mockups of six views: login (UI-C01), patient home (UI-P01), doctor schedule (UI-D01), reception home (UI-R01), cashier home (UI-K01), and administrator home (UI-A01). Include menus for their secondary views, identifying which still need to be designed. Make this minimal presentation navigable with fictional data. If you use a profile selector to explore the prototype, label it as demonstration mode.

Critical rules: reception does not collect payments or view prescriptions or medical records; the cashier collects only medication and additional-service payments. Consultations are prepaid online using a línea de captura; consultation payments, cancellations, and refunds are managed online without cashier intervention (D-04). A doctor’s cancellation still requires reception’s online approval. There is no rescheduling. Appointments are requested between 48 hours and three months in advance, with an available doctor and time slot within their working schedule; the patient cannot have another pending appointment with that same doctor. The confirmation includes the línea de captura and an 8-hour deadline. The payment provider and verification mechanism remain open. Patient cancellation: proposed intervals of 100% at least 48 hours in advance, 50% from 24 to less than 48 hours, and 0% with less than 24 hours’ notice; cancellation by a doctor gives a 100% refund. Executing the online refund is separate from canceling. Audit logs cannot be edited or deleted.

Detailed administrator permissions and some rules remain open. Do not grant clinical access or universal permissions by default. Flag every new proposal in a separate list without presenting it as a confirmed requirement.

Include empty and populated view variants, and representations of errors/internal access without VPN. There is no need to detail every screen now. Propose a consistent visual layout in Spanish and record the decisions. The result is a mockup with simulations; do not connect a database, VPN, or real payments.

Deliver: map by role, six initial views, minimal navigable walkthrough, inventory of secondary views with their IDs, and a short list of questions. Do not choose the production stack. When a question does not block the general map, record it and continue.
```

## How to review and bring the design back into the project

- Check that all five profiles and the six requested initial views appear.
- Check the separation of reception/cashier responsibilities and the doctor's clinical access.
- Review whether navigation makes it clear who schedules, confirms, provides care, and cancels.
- Verify empty states/errors and that the prototype does not present proposals as approved functions.
- Save the export and decisions alongside a spec for the workflow to be implemented. Use UI-* IDs to name views and link them to RF/RN.
- Incorporate business changes into the shared documents before asking Codex or Claude Code to implement that behavior.

Reference on workflows, prototypes, and design handoff: [official Claude Design guide](https://academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux).
