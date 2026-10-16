# Business rules

Status: draft v0.1. References S1/EQUIPO and decisions D-* are in `00-context.md`. Open questions P-* must be retained until the team resolves them.

## Extracted rules and confirmed decisions

| ID | Rule | Origin / clarification pending |
| --- | --- | --- |
| RN-01 | Appointments are requested at least 48 hours and no more than three months in advance; past dates are not allowed | S1 p. 1; exact boundaries and months in P-05 |
| RN-02 | A doctor cannot have appointments occupying the same time slot | S1 p. 1; duration and overlaps in P-03 |
| RN-03 | A patient cannot request another pending appointment with the same doctor | S1 p. 1; definition of pending in P-04 |
| RN-04 | Every appointment must fit within the doctor's working schedule | S1 pp. 1/3; breaks and duration in P-03 |
| RN-05 | An appointment is not rescheduled: it is canceled and a new one is requested | S1 p. 1 |
| RN-06 | Scheduling grants an 8-hour deadline to confirm payment; missing it cancels the appointment for nonpayment and releases the slot | S1 p. 1; exact deadline and payment evidence in P-01/P-05 |
| RN-07 | Patient cancellation applies the refund policy according to how far in advance it occurs | S1 p. 2; interval interpretation below |
| RN-08 | Doctors request cancellation and need reception's prior approval; a cancellation requested by a doctor gives a 100% refund | S1 pp. 1/3/5; monetary operation in P-07 |
| RN-09 | Appointment statuses are the seven specified below | S1 p. 1; transitions and owners in P-06 |
| RN-10 | Patients can register, view their data and appointments, and cancel their appointments | S1 p. 2 |
| RN-11 | Doctors do not register themselves; reception registers them | S1 p. 3; any additional administrator permission is resolved in P-02 |
| RN-12 | Doctors cannot edit their employee number, professional license number, CURP, name, or specialty | S1 p. 3 |
| RN-13 | A doctor practices one specialty at a time and has a working schedule | S1 p. 3 |
| RN-14 | Reception cannot view prescriptions or medical records | S1 p. 5 |
| RN-15 | Reception can register and view receptionists, doctors, and patients; administrators can also register receptionists | S1 p. 5; final allocation in P-02 |
| RN-16 | Medications and services can be sold to people without patient registration | S1 p. 5; prescription requirements in P-08 |
| RN-17 | Audit logs allow reading and insertion; updating and deleting are prohibited for all users | S1 p. 5; insertion through system operations is proposed |
| RN-18 | There must be at least ten specialties, four doctors per specialty, and three additional services other than consultations and medications | S1 pp. 2/4 |
| RN-19 | The consultation cost depends on the specialty | S1 p. 2 |
| RN-20 | There are five roles, and all their interfaces are web-based | D-01/D-02 |
| RN-21 | Receptionists, administrators, and cashiers require a VPN to work | D-03; implementation and VPN connection loss in P-10 |
| RN-22 | Payment collection is the cashier's responsibility, and reception no longer collects payments | D-04; having the cashier also issue refunds is proposed |

## Patient cancellation policy

Proposed interpretation of the text in S1, p. 2, to turn it into intervals without gaps:

| Time before the appointment starts | Refund percentage |
| --- | --- |
| At least 48 hours | 100% |
| At least 24 and less than 48 hours | 50% |
| Less than 24 hours, before the appointment | 0% |

Confirm this interpretation and what happens after the appointment starts (P-06). The amount used for the calculation, refund method, and refund date remain in P-07. Canceling and recording an actually issued refund are separate operations.

## Appointment statuses from the source

1. Scheduled, awaiting payment.
2. Paid, awaiting consultation.
3. Canceled for nonpayment.
4. Canceled by patient.
5. Canceled by doctor.
6. Completed.
7. No-show.

Do not add clinical or financial statuses to this list without an explicit decision. A doctor's cancellation request can be modeled as an associated process with pending/approved/rejected statuses; this is a proposal, not an approved eighth appointment status.

## Additional proposals to validate

| ID | Proposal | Reason / open question |
| --- | --- | --- |
| PRN-01 | Prevent consultation room overlaps even when doctors differ | Scheduling consistency; P-11 |
| PRN-02 | Revalidate availability at confirmation and ensure an atomic reservation | Prevent two simultaneous requests from occupying the same slot |
| PRN-03 | Prevent sales with insufficient stock and update inventory with the sale | Pharmacy consistency; P-08 |
| PRN-04 | Prevent confirming the same payment twice or issuing the same refund twice | Cashier consistency; P-01/P-07 |
| PRN-05 | Preserve the cost and policy applied to an appointment even if catalogs change | Consistent history; to be validated |
| PRN-06 | Administrators and cashiers have no clinical content access by default; doctors have access to patients related to their care | Permissions matrix pending P-02/P-04/P-12 |

These proposals can be considered in mockups with labels indicating that they are pending. They are not approved as the team's business rules.
