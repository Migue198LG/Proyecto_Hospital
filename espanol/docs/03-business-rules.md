# Reglas de negocio

Estado: borrador v0.1. Referencias S1/EQUIPO y decisiones D-* en `00-context.md`. Los pendientes P-* deben conservarse hasta que el equipo los resuelva.

## Reglas extraídas y decisiones confirmadas

| ID | Regla | Origen / precisión pendiente |
| --- | --- | --- |
| RN-01 | Las citas se solicitan con al menos 48 horas y como máximo tres meses de anticipación; no se permiten fechas pasadas | S1 p. 1; límites exactos y meses en P-05 |
| RN-02 | Un doctor no puede tener citas que ocupen el mismo horario | S1 p. 1; duración y traslapes en P-03 |
| RN-03 | Un paciente no puede solicitar otra cita pendiente con el mismo doctor | S1 p. 1; definición de pendiente en P-04 |
| RN-04 | Toda cita debe quedar dentro de la jornada del doctor | S1 pp. 1/3; descansos y duración en P-03 |
| RN-05 | Una cita no se reagenda: se cancela y se solicita una nueva | S1 p. 1 |
| RN-06 | Al agendar se concede un plazo de 8 horas para confirmar el pago; al incumplir se cancela por falta de pago y se libera la fecha | S1 p. 1; vencimiento exacto y evidencia de pago en P-01/P-05 |
| RN-07 | La cancelación del paciente aplica la política de devolución según anticipación | S1 p. 2; interpretación de intervalos debajo |
| RN-08 | El doctor solicita cancelación y necesita aprobación previa de recepción; una cancelación por doctor devuelve el 100% | S1 pp. 1/3/5; operación monetaria en P-07 |
| RN-09 | Los estados de cita son los siete especificados debajo | S1 p. 1; transiciones y responsables en P-06 |
| RN-10 | El paciente puede registrarse, consultar sus datos y citas, y cancelar sus citas | S1 p. 2 |
| RN-11 | El doctor no se registra a sí mismo; recepción realiza su alta | S1 p. 3; cualquier permiso adicional de administrador se resuelve en P-02 |
| RN-12 | El doctor no edita su número de empleado, cédula profesional, CURP, nombre ni especialidad | S1 p. 3 |
| RN-13 | Un doctor ejerce una especialidad a la vez y tiene jornada de trabajo | S1 p. 3 |
| RN-14 | Recepción no puede visualizar recetas ni historial médico | S1 p. 5 |
| RN-15 | Recepción puede dar de alta y consultar recepcionistas, doctores y pacientes; administrador también puede dar de alta recepcionistas | S1 p. 5; asignación definitiva en P-02 |
| RN-16 | Se pueden vender medicamentos y servicios a personas sin registro de paciente | S1 p. 5; requisitos de receta en P-08 |
| RN-17 | Las bitácoras permiten consulta e inserción; actualizar y borrar está restringido para todos los usuarios | S1 p. 5; se propone inserción a través de operaciones del sistema |
| RN-18 | Debe haber al menos diez especialidades, cuatro doctores por especialidad y tres servicios extras distintos de consulta y medicamentos | S1 pp. 2/4 |
| RN-19 | El costo de consulta depende de la especialidad | S1 p. 2 |
| RN-20 | Hay cinco roles y todas sus interfaces son web | D-01/D-02 |
| RN-21 | Las operaciones de recepción, administrador y cajero, y las funciones de consultorio del doctor (datos del paciente/clínicos, historial médico, diagnósticos, tratamientos y recetas), requieren acceso por VPN a la red privada del hospital, además de autenticación y permisos por rol de la aplicación | D-03/D-09; implementación, política de VPN remota, otras funciones del doctor y pérdida de conexión en P-10 |
| RN-22 | El cajero cobra únicamente medicamentos y servicios adicionales. Las consultas se pagan por anticipado en línea mediante línea de captura; sus pagos, cancelaciones y reembolsos se gestionan en línea sin intervención del cajero. Recepción no cobra | D-04; proveedor y conciliación P-01/P-05/P-07; aprobación del doctor sigue en RN-08 |

## Política de cancelación del paciente

Interpretación propuesta del texto de S1, p. 2, para convertirlo en intervalos sin huecos:

| Anticipación respecto al inicio de cita | Porcentaje de devolución |
| --- | --- |
| Al menos 48 horas | 100% |
| Al menos 24 y menos de 48 horas | 50% |
| Menos de 24 horas, antes de la cita | 0% |

Confirmar esta interpretación y qué pasa después del inicio de la cita (P-06). Los reembolsos de consultas se gestionan en línea sin intervención del cajero (D-04); base de cálculo, mecanismo de ejecución y plazos siguen en P-07. Cancelar y verificar una devolución efectivamente ejecutada son operaciones distintas.

## Estados de cita de la fuente

1. Agendada pendiente de pago.
2. Pagada pendiente por atender.
3. Cancelada Falta de pago.
4. Cancelada Paciente.
5. Cancelada Doctor.
6. Atendida.
7. No acudió.

No añadir estados clínicos o financieros a esta lista sin una decisión explícita. La solicitud de cancelación del doctor puede modelarse como un trámite asociado, con pendiente/aprobada/rechazada; es una propuesta, no un octavo estado de cita aprobado.

## Propuestas adicionales por validar

| ID | Propuesta | Motivo / pendiente |
| --- | --- | --- |
| PRN-01 | Impedir traslapes de consultorio aunque sean doctores diferentes | Consistencia de agenda; P-11 |
| PRN-02 | Revalidar disponibilidad al confirmar y asegurar reserva atómica | Evitar que dos solicitudes simultáneas ocupen el mismo espacio |
| PRN-03 | Impedir ventas con existencias insuficientes y actualizar inventario con la venta | Consistencia de farmacia; P-08 |
| PRN-04 | Impedir confirmar dos veces un mismo pago o ejecutar dos veces la misma devolución | Consistencia de pagos/reembolsos de consultas en línea y ventas separadas de medicamentos/servicios; P-01/P-07 |
| PRN-05 | Conservar el costo y la política aplicados a una cita aunque cambien los catálogos | Historial consistente; por validar |
| PRN-06 | Administrador y cajero sin contenido clínico por defecto; doctor con acceso a pacientes relacionados con su atención | Matriz de permisos pendiente P-02/P-04/P-12 |

Estas propuestas pueden considerarse en los bocetos, con etiquetas de pendiente. No están aprobadas como reglas de negocio del equipo.
