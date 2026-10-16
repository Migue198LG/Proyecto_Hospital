# Project requirements from the original sources

Status: source extraction for project planning, 2026-10-16. This document retains the project requirements, rules, data, examples, and assessment criteria from the three PDFs. Institutional headings, logos, and repeated page footers are omitted. Wording and field labels are translated into English for readability; this is not a literal transcription or a proposed database schema.

These are academic source requirements. Later team decisions and unresolved interpretations are recorded separately in [context and decisions](00-context.md). Use [requirements](02-requirements.md) and [business rules](03-business-rules.md) for the existing RF/RNF/RN identifiers; this document does not replace or renumber them.

## Sources

| Key | Original document | Coverage |
| --- | --- | --- |
| S1 | [Project specifications](../contexto/ESPECIFICACIONES%20PROYECTO%20FINAL%20BASES%20DE%20DATOS%2026-2.pdf) | Project scope, functionality, data, and permissions; five physical pages |
| S2 | [First assessment rubric](../contexto/Ru%CC%81brica_Eval_Proyecto_1P.pdf) | First submission deliverables and weights; one page |
| S3 | [Second assessment rubric](../contexto/Ru%CC%81brica_Eval_Proyecto_2P.pdf) | Second submission deliverables and weights; one page |

## Objective and general requirements

Source: S1, p. 1. Related requirements: RF-01 and RNF-01.

- Develop a database management system that manages hospital appointments, pharmacy, services, prescriptions, and consultation rooms.
- Teams may have at most four students.
- The programming language is unrestricted.
- The database engine must be Microsoft SQL Server.
- The system must include a login module.
- The source requires at least three profiles: doctor, patient, and receptionist. Cashier or pharmacist profiles are optional in the source.

Minimum entities to develop (S1, p. 2): employees, doctors, patients, appointments, consultation rooms, specialties, prescriptions, pharmacy/medications, audit log, payment, and services.

## Appointment scheduling and payment

Source: S1, pp. 1–2. Related requirements: RF-05/RF-06/RF-07; rules RN-01 through RN-06 and RN-09.

- Appointments must be booked at least 48 hours and no more than three months in advance. Same-day appointments and past dates are not allowed.
- A doctor cannot be booked when already occupied at that date and time.
- A patient cannot book another appointment with the same doctor while they have a pending appointment with that doctor.
- Appointments must fall within the doctor's working schedule.
- Appointments cannot be rescheduled. They must be canceled and a new appointment requested.
- When booking, the patient is given eight hours to confirm payment.
- Cancellation for nonpayment releases the appointment slot.

The seven appointment statuses listed in the source are:

1. Scheduled, awaiting payment.
2. Paid, awaiting consultation.
3. Canceled for nonpayment (slot released).
4. Canceled by patient (cancellation policy applies).
5. Canceled by doctor (100% refund).
6. Completed.
7. No-show.

## Cancellations and refunds

Source: S1, pp. 1–3 and 5. Related requirements: RF-09/RF-10; rules RN-07/RN-08.

The patient cancellation policy is expressed in the source as follows:

| Advance notice stated in the source | Refund of the payment |
| --- | --- |
| 48 hours | 100% |
| 24 hours | 50% |
| Less than 24 hours | 0% |

Patients may cancel their appointments under this policy. Doctors require prior approval from reception to cancel an appointment, and doctor cancellations receive a 100% refund. Reception may cancel appointments on behalf of the patient or doctor.

Planning note: the source does not explicitly define complete time intervals, cancellation after the appointment starts, the refund calculation base, or how refunds are issued. The interval interpretation in RN-07 and questions P-06/P-07 remain subject to review; they are not resolved here.

## Patient functions and booking flow

Source: S1, pp. 2–3. Related requirements: RF-02/RF-05/RF-06/RF-08/RF-09; rules RN-10/RN-18/RN-19.

Patients can register themselves, view their personal data, view their appointment history, and cancel their appointments. The appointment list must show every appointment the patient has made, with all its data and current status, provide cancellation, and allow filtering by date(s) or status.

The source's example patient interface has personal data, scheduled appointments, and new appointment booking sections. Its booking sequence is:

1. Select a specialty. Consultation cost differs by specialty, and there must be at least ten specialties.
2. Select a doctor. There must be at least four doctors per specialty.
3. Select a date, showing only available dates.
4. Select a time slot, showing only available time slots.
5. On success, generate an appointment confirmation document and payment reference. On failure, display the error(s) in a message and restart the flow.

The specialties listed are cardiology, dermatology, gynecology, general medicine, nephrology, nutrition, ophthalmology, oncology, orthopedics, and pediatrics.

The appointment confirmation document includes:

- Appointment reference number.
- Patient name.
- Date and time slot.
- Consultation room.
- Specialty and doctor.
- Payment reference.
- A notice stating the eight-hour payment deadline.
- A notice stating the cancellation policy.

## Doctor functions and clinical data

Source: S1, p. 3. Related requirements: RF-03/RF-04/RF-08/RF-11/RF-12; rules RN-11/RN-12/RN-13.

The example doctor interface includes doctor data, prescriptions, patient data, appointments, and the patient's medical record.

- Doctors cannot register themselves; reception registers them.
- Doctors cannot edit their employee number, professional license number, CURP, name, or specialty.
- Doctors may cancel an appointment only with prior approval from a receptionist.
- A doctor may practice only one specialty at a time.
- Each doctor has a working schedule; appointments cannot be booked outside it.

| Document | Fields listed in the source |
| --- | --- |
| Prescription | Prescription reference number, date, doctor name, professional license number, patient name, age, diagnosis, medication(s), treatment(s), observations |
| Patient medical record | Medical record identifier, patient identifier, patient name, allergies, blood type, previous conditions, weight, height |

## Reception, pharmacy, services, and sales

Source: S1, pp. 3–5. Related requirements: RF-03/RF-04/RF-09/RF-13/RF-14; rules RN-14/RN-15/RN-16/RN-18.

The source's example reception interface contains receptionists, doctors, specialties, consultation rooms, patients, appointments, additional services, pharmacy/medication inventory, payment collection/sales receipts, and the two audit logs described below.

- A receptionist can be registered by another receptionist or by an administrator.
- Reception can register and view receptionists, doctors, and patients.
- Reception cannot view medical prescriptions or a patient's medical record.
- Reception can cancel appointments on behalf of the patient or doctor.
- The source allows a receptionist to collect payments for medications and services, or a separate profile to be created for that activity. The team's later reassignment is noted below.
- Additional services must be different from consultations and medications. At least three are required. Examples: injection, vaccination, wound care, and blood test.
- The pharmacy section covers medication inventory.
- The payment collection/sales receipt section adds the service and medication amounts, as applicable.
- A customer does not need to be registered as a hospital patient to buy a service or medication.

## Audit logs and permissions

Source: S1, pp. 4–5. Related requirement: RF-15; rule RN-17.

| Audit log | Fields listed in the source |
| --- | --- |
| Appointment status | Appointment reference number, activity date, appointment status, appointment date, specialty identifier, cost, cancellation policy, refunded amount |
| Doctor–patient appointment history | History identifier, user performing the action (patient/doctor/receptionist), machine/IP (optional), appointment reference number, appointment date, appointment time, patient identifier, prescription reference number, doctor identifier, consultation status (completed/no-show), specialty, consultation room |

Audit logs allow reading and insertion only. Updating and deleting entries are prohibited for all users. Listing a prescription reference in an audit log does not override reception's prohibition on viewing prescriptions.

## First assessment deliverables

Source: S2, p. 1.

| Deliverable | Source instructions | Weight |
| --- | --- | --- |
| Problem statement | Describe the problem to solve | 5% |
| Business rules | Define the rules applicable to the project; only some were supplied | 5% |
| Functional requirements | No additional observation in the rubric | 8% |
| Non-functional requirements | No additional observation in the rubric | 7% |
| Three context diagrams | Levels 0, 1, and 2 | 30% |
| Entity–relationship diagram | Indicate PK, FK, cardinality, multivalued and composite attributes, etc. | 30% |
| Data dictionary in Excel tables | Include key, field, data type, size, and whether nulls are accepted | 15% |
| Total | | 100% |

## Second assessment deliverables

Source: S3, p. 1.

| Deliverable | Source instructions | Weight |
| --- | --- | --- |
| Use case diagram | Documentation | 10% |
| Sequence diagrams | Documentation | 10% |
| Normalized relational model | Documentation | 10% |
| Database structure script | Attach a `.sql` script | 10% |
| Database connection | Demonstrate during the in-class review | 10% |
| At least ten records per table, where applicable | Insert before the review | 5% |
| Four views | Document and implement in SQL | 7.5% |
| Four functions | Document and implement in SQL | 7.5% |
| Insert an appointment from the application, with its validations | From an application or web page | 30% |
| Total | | 100% |

## Validation and delivery expectations

Source: S1, p. 5.

As topics are covered in class, students must develop the deliverables identified in the welcome presentation. Each submission's rubric, weights, and date will be announced. Students must analyze, design, and implement all validations needed for the system to work correctly. The source does not enumerate every validation or decide every business detail.

## Later team decisions and open questions

This section is planning context, not text from the PDFs. See [00-context.md](00-context.md) for the authoritative decision and question register.

- D-01 confirms five roles: patient, doctor, receptionist, cashier, and administrator. The source's optional cashier wording does not undo this decision.
- D-02 confirms a fully web-based application. D-03 requires VPN access for receptionists, cashiers, and administrators; these requirements are later team decisions, not requirements stated in S1.
- D-04 assigns payment collection to the cashier. Reception's source-level option to collect payments must not be used as the current team permission.
- Payment method and confirmation (P-01), administrative permissions (P-02), consultation duration and schedules (P-03), the meaning of a pending appointment and clinical access (P-04), and exact time boundaries (P-05) still need decisions. Cancellation/refund details, pharmacy rules, personal data, infrastructure, consultation room conflicts, and clinical corrections/audit access remain in P-06 through P-12.

Preserve these distinctions when writing feature specifications. Mockups and this extraction do not demonstrate that authentication, permissions, VPN access, or business rules have been implemented.
