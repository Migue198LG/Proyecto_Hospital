# Problem statement and objectives

Status: draft for team review. Scope source: S1; submission structure: S2, defined in `00-context.md`.

## Problem statement

Hospital operations require coordinating patients, doctor availability, consultation rooms, appointments, payments, and medical care. When this information is managed in separate records, scheduling conflicts, inconsistencies between an appointment's status and its payment, and difficulties reviewing the history of operations can arise.

Management also needs to apply advance-booking, online consultation prepayment by línea de captura, online cancellation, and online refund policies consistently (D-04). The cashier collects only medication and additional-service payments; those sales and stock are separate from consultation payments. Clinical data must be accessed according to each user’s responsibilities.

The project proposes a centralized web system to support these operations, with five roles and a Microsoft SQL Server database. It separates reception and cashier tasks, preserves traceability, and restricts reception, administration, cashier operations, and the doctor's consultation functions to the hospital's private network through a VPN.

**Evidence note:** the risks above describe the problem the project seeks to solve. No actual hospital has been studied, and it has not been demonstrated that one uses separate records or experiences these problems. If the team has a reference institution, replace this general formulation with evidence from that institution's operations.

## General objective

Develop a web system that manages a hospital's appointments and associated operations, applying business rules, role-based permissions, and activity logging using Microsoft SQL Server.

## Specific objectives

- Facilitate patient registration and appointment requests with valid availability.
- Keep appointment statuses, payments, cancellations, and refunds synchronized.
- Support doctors in reviewing medical history and issuing prescriptions.
- Facilitate medication and service sales with sales receipts and stock control.
- Separate patient, doctor, reception, cashier, and administration responsibilities.
- Record appointment and consultation activity in audit logs that cannot be edited or deleted.

## Proposed evidence of success

Detailed criteria are in `02-requirements.md`. The demonstration must allow a valid appointment to be scheduled, reject one that violates the rules, confirm a payment, cancel according to the policy, conduct a consultation with a prescription, and generate a receipt for a sale.

It will also verify that reception cannot collect payments or view clinical content, and that reception, administration, cashier operations, and the doctor's consultation functions reject access without the hospital-network VPN. Authentication and role permissions must still apply inside the VPN. These are project criteria, not results already achieved.
