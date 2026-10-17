# SPEC-001 — Schedule an appointment and generate a confirmation document

Status: **draft specification example**. Owner: team, to be assigned. Date: 2026-10-12. This is not yet an instruction to implement.

## Need and scope

A patient must be able to find a valid slot with a doctor and request an appointment. The observable result is an appointment **Scheduled, awaiting payment**, with an appointment reference number, confirmation document, and payment reference. Reception can also schedule on behalf of a patient, following the same availability rules.

This spec covers creation and the confirmation document. Online consultation prepayment by línea de captura and online cancellation/refund management are confirmed by D-04; the cashier handles only medication and additional-service payments. Provider integration, payment verification, automatic expiration, and cancellation details will be specified separately; their statuses and data must be considered when modeling appointments.

## References

- Source: `contexto/ESPECIFICACIONES PROYECTO FINAL BASES DE DATOS 26-2.pdf`, pp. 1-3.
- Requirements: RF-01, RF-04, RF-05, RF-06; RNF-02, RNF-04, and RNF-05.
- Rules: RN-01, RN-02, RN-03, RN-04, RN-05, RN-06, RN-13, RN-18, RN-19.
- Screens: UI-P03 and UI-P04; UI-R02 for reception's operation.
- Decisions: D-01, D-02, D-03 for internal access, and D-04 for online consultation payments and cashier scope.
- Open questions affecting implementation: P-01, P-03, P-04, P-05, and P-11.
- Proposals to review: PRN-01, PRN-02, and PRN-05.

## Actors, data, and permissions

- **Authenticated patient:** schedules only for themselves.
- **Authenticated receptionist connected to the VPN:** can create an appointment for a registered patient. Access to the schedule does not grant access to medical records or prescriptions.
- **Doctor:** appears as a search option if they belong to the selected specialty and their working schedule permits the time slot. They do not create this appointment from their profile in this workflow.
- **Visible inputs:** specialty and cost, doctor, date, time slot, and patient. The patient comes from the session or reception's authorized selection.
- **Outputs:** reference number, initial status, date and time slot, patient, doctor, specialty, consultation room, payment reference, eight-hour deadline notice, and cancellation policy.

The confirmation document fields come from the source. The format of the appointment reference number and payment reference, consultation duration, and consultation room allocation method require definition before programming.

## Expected main journey

1. The person opens Schedule appointment, selects a specialty, and sees its cost.
2. They select a doctor in that specialty.
3. They see available dates and time slots within the permitted interval and the doctor's working schedule.
4. They review the appointment data.
5. Upon confirmation, the server revalidates the rules and creates a single appointment awaiting payment.
6. The system presents the confirmation document and payment reference. It states that payment must be confirmed within eight hours.

Revalidation at confirmation and atomic reservation are implementation proposals to prevent simultaneous booking; document them explicitly when preparing the technical plan.

## Alternative cases and errors

- Date outside the RN-01 interval or in the past: show an understandable reason and do not create an appointment.
- Time slot already occupied by that doctor or outside their working schedule: show updated availability; do not create an appointment.
- Patient with a pending appointment with the same doctor: explain the conflict and do not create another.
- Time slot taken between viewing and confirmation: report the conflict and allow another selection; the source requires showing errors and restarting the request, so how to preserve already-entered data must be agreed.
- Specialty without doctors or time slot without availability: show an empty state with a clear next action.
- Request without a valid session or permission: reject it on the server.

## Draft acceptance criteria

| ID | Given / when / then | Rules |
| --- | --- | --- |
| CA-01 | Given an authenticated patient and a valid doctor and slot, when the patient confirms the request, then a single appointment awaiting payment is created and a confirmation document with all required fields is shown | RN-01/02/03/04/06; RF-05/06 |
| CA-02 | Given a date less than 48 hours or more than three months in advance, when confirmation is attempted, then the server rejects the request and does not create an appointment | RN-01; exact boundary P-05 |
| CA-03 | Given an occupied doctor or a time slot outside their working schedule, when confirmation is attempted, then no appointment is created and the reason is stated | RN-02/04; duration P-03 |
| CA-04 | Given a patient with another pending appointment with the same doctor, when confirmation is attempted, then the new appointment is rejected | RN-03; definition of pending P-04 |
| CA-05 | Given two simultaneous requests for the same doctor's slot, when both attempt confirmation, then at most one obtains an appointment | RN-02; PRN-02 |
| CA-06 | Given an unrelated user or a receptionist outside the VPN, when they request creation of an appointment for another person, then the server rejects the operation | RF-01; RNF-03/04 |
| CA-07 | Given a created appointment, when its confirmation document is opened, then the reference number, patient, date, time slot, consultation room, specialty, doctor, payment reference, eight-hour deadline, and cancellation policy appear | RF-06; RN-06 |
| CA-08 | Given failed validation or no available time slots, when the person views the result, then they see a specific message and can resume or restart the request according to the recorded interface decision | S1 p. 2; UI-P03 |

**Limit of this version:** CA-02 through CA-05 contain parts that are not sufficiently defined to be declared accepted or implemented. For example, “three months” requires agreement on whether they are calendar months; “occupied” requires appointment duration; “pending” requires specific statuses.

## Questions to resolve with the team

1. P-03: How long does each consultation last? Is duration fixed or variable by specialty? How are breaks modeled?
2. P-04: Which statuses count toward the restriction on a pending appointment with the same doctor?
3. P-05: How are three months, the 48-hour boundary, and the start of the payment deadline calculated?
4. P-11: How is a consultation room selected, and how are two simultaneous appointments in the same room prevented?
5. P-01: Which provider and integration issue and verify the línea de captura for online consultation payment? What evidence is retained, and will the academic demonstration use a real connection or a labeled simulation?
6. PRN-05: Is the cost shown at booking frozen in the appointment?

## Technical plan and tasks

Pending until the team confirms the rules above and selects a stack. When planning: SQL Server schema and constraints, availability service, transactional creation, authorization, confirmation document generation, interface, and tests for criteria CA-01 through CA-08. Do not create final tables or endpoints from a mockup.

## Verification

For now, only the consistency of the document and prototype can be reviewed. There is no implementation or test results. After implementation, record evidence for each CA-*, including rejections, exact boundaries, concurrency, and permissions.
