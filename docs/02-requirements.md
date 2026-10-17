# Initial requirements

Status: draft v0.1. References S1, D-*, and P-* are in `00-context.md`; RN-* and PRN-* are in `03-business-rules.md`. The criteria are verification proposals and must be detailed when each workflow is specified.

## Functional requirements

| ID | Requirement | Initial acceptance criterion | Source / rules |
| --- | --- | --- | --- |
| RF-01 | Authenticate users and show navigation by role | Each of the five profiles accesses its navigation; an operation outside its permissions is rejected by the server | S1 p. 1; D-01; detailed permissions P-02 |
| RF-02 | Register patients and view their data | A person creates a patient account and views their data; reception can register them | RN-10/RN-15; fields in P-09 |
| RF-03 | Manage registration and viewing of employees, accounts, and roles | Reception registers doctors; reception or an administrator registers receptionists; cashier registration and other permissions follow P-02 | RN-11/RN-15; proposed extension D-01 |
| RF-04 | Manage specialties, costs, consultation rooms, and working schedules | Catalogs and schedules used for booking can be viewed; each doctor has only one active specialty | RN-04/RN-13/RN-18/RN-19; owners P-02 |
| RF-05 | Schedule appointments with valid availability | Specialty, doctor, date, and time slot are selected; dates, time slots, and duplicates that violate RN-01/02/03/04 are rejected | S1 pp. 1/2; boundaries P-03/P-04/P-05 |
| RF-06 | Generate an appointment confirmation document and payment reference | When the appointment is created, show its reference number, patient, date, time slot, consultation room, specialty, doctor, payment reference, payment deadline, and cancellation policy | S1 p. 3; RN-06/RN-07 |
| RF-07 | Verify online consultation prepayments and handle expired deadlines | The system verifies payment against the appointment’s línea de captura and marks it paid; an unpaid expired appointment is canceled and releases the slot. The cashier cannot confirm consultation payments; late notifications follow the reconciliation policy to be defined | D-04; RN-06/RN-22; integration and boundaries P-01/P-05 |
| RF-08 | View appointments and history with filters | Patients see their appointments by date/status; doctors view their schedules; reception views the general schedule | S1 pp. 2/3/4; RN-09/RN-10 |
| RF-09 | Manage cancellations online | Patients or reception cancel through the web application according to policy; doctors request cancellation and reception approves online before cancellation; no cashier step or rescheduling is available | D-04; RN-05/RN-07/RN-08; P-06 |
| RF-10 | Manage consultation refunds online | Distinguish refund entitlement, processing, and verified execution; the patient views the result online. The cashier neither issues nor confirms consultation refunds | D-04; RN-07/RN-08; execution and reconciliation P-07 |
| RF-11 | Record patient care and view medical records | Doctors access permitted clinical data and record the consultation outcome only through the hospital-network VPN; reception does not receive clinical content | S1 p. 3; RN-14/RN-21; D-09; RNF-03; P-04/P-06/P-12 |
| RF-12 | Issue and view prescriptions | A prescription includes reference number, date, doctor, professional license number, patient, age, diagnosis, medications, treatments, and observations; doctors require hospital-network VPN access to issue or view it | S1 p. 3; RN-14/RN-21; D-09; RNF-03; corrections P-12 |
| RF-13 | Manage medications and inventory | Medications, prices, and stock can be viewed; the proposed sales workflow updates quantities | S1 p. 4; PRN-03; owners and details P-02/P-08 |
| RF-14 | Manage services and sales | The cashier can sell services and medications to a customer without a patient account; the total is calculated and a sales receipt is generated | S1 pp. 4/5; RN-16/RN-18/RN-22 |
| RF-15 | Record and view audit logs | Record the actor and appointment/consultation activity; no interface or permission allows entries to be modified or deleted | S1 pp. 4/5; RN-17; viewing P-12 |

## Non-functional requirements

| ID | Requirement | Proposed verification | Status |
| --- | --- | --- | --- |
| RNF-01 | Use Microsoft SQL Server | Demonstrate a connection and executable scripts on the selected database engine | Source S1/S3 |
| RNF-02 | Provide the five interfaces through a browser | Open each web interface; patient interface usable on mobile and internal operations on a computer | Web confirmed D-02; responsive adaptation proposed |
| RNF-03 | Restrict reception, administrator, cashier, and doctor consultation functions to the hospital's private network through a VPN | With valid credentials but no authorized hospital-network VPN access, reject protected pages and direct API requests, including the doctor's clinical reads/writes and prescriptions; with VPN access, still reject unauthenticated or unauthorized requests | Confirmed D-03/D-09; technical design and remote VPN policy P-10 |
| RNF-04 | Enforce authentication and authorization on the server | Reject unauthorized direct access, even when the resource URL or identifier is known | Proposed; implements S1 permissions |
| RNF-05 | Maintain integrity under concurrent operations | Two simultaneous reservations for the same slot do not cause double booking; sales/payment operations do not leave partial changes | Proposed PRN-02/PRN-03/PRN-04 |
| RNF-06 | Protect credentials and user data | Protected transport, no plaintext password storage, and responses consistent with permissions | Proposed; technical decisions pending |
| RNF-07 | Support usability and comprehension | Forms with labels, keyboard navigation, statuses expressed with text as well as color, and specific messages | Proposed; accessibility target to be defined |
| RNF-08 | Preserve traceability | Each relevant change includes actor, reference, and timestamp; audit logs protected against updates/deletion | Source RN-17; implementation proposed |
| RNF-09 | Define recovery and backups | Document and demonstrate restoration using test data | Proposed; frequency, RPO, and RTO to be defined |
| RNF-10 | Establish measurable performance targets | Measure scheduling and appointment confirmation with agreed data volume and concurrency | Open; no invented response times or capacity |

## Minimum document data

- **Appointment confirmation document:** the fields listed in RF-06.
- **Medical record:** medical record/patient identifier, name, allergies, blood type, previous conditions, weight, and height (S1 p. 3).
- **Prescription:** the fields listed in RF-12.
- **Appointment audit log:** reference number, activity date, status, appointment date, specialty, cost, cancellation policy, and refunded amount (S1 p. 4).
- **Consultation operations audit log:** medical record, user, appointment, date/time, patient, prescription reference number, doctor, consultation outcome, specialty, and consultation room; machine/IP optional (S1 p. 4). A reference to a prescription does not grant access to its content.

Personal forms, required fields, types, lengths, and validations will be defined in the data dictionary. Do not infer them from a mockup.

## Priority checks for future specs

1. Valid scheduling and rejection for each applicable RN, including time boundaries once resolved.
2. Simultaneous requests for the same time slot and the same patient/doctor.
3. Online payment by línea de captura, verified confirmation, duplicate/late notifications, expired deadline, and payment at the agreed boundary; cashier access to consultation payments/refunds is rejected.
4. Cancellation at 48 hours, at 24 hours, and below 24 hours; approved cancellation requested by a doctor.
5. Reception without payment collection or clinical content permissions; reception/administrator/cashier functions and doctor clinical reads/writes with and without hospital-network VPN access, including direct API requests. VPN access must not bypass authentication or role permissions.
6. Sale to an unregistered customer; correct stock and total.
7. Activity logging and rejection of audit log modification/deletion.
