# SPEC-001 — Agendar cita y generar comprobante

Estado: **ejemplo de especificación en borrador**. Responsable: equipo, por asignar. Fecha: 2026-10-12. No es una instrucción para implementar aún.

## Necesidad y alcance

Un paciente debe poder encontrar un espacio válido con un doctor y solicitar una cita. El resultado observable es una cita **Agendada pendiente de pago**, con folio, comprobante y línea de pago. Recepción también puede agendar en nombre de un paciente, respetando las mismas reglas de disponibilidad.

Esta spec cubre creación y comprobante. El prepago de consultas en línea mediante línea de captura y la gestión en línea de cancelaciones/reembolsos están confirmados por D-04; el cajero maneja únicamente pagos de medicamentos y servicios adicionales. La integración del proveedor, verificación del pago, vencimiento automático y detalles de cancelación se especificarán por separado; sus estados y datos deben considerarse al modelar citas.

## Referencias

- Fuente: `contexto/ESPECIFICACIONES PROYECTO FINAL BASES DE DATOS 26-2.pdf`, pp. 1-3.
- Requerimientos: RF-01, RF-04, RF-05, RF-06; RNF-02, RNF-04 y RNF-05.
- Reglas: RN-01, RN-02, RN-03, RN-04, RN-05, RN-06, RN-13, RN-18, RN-19.
- Pantallas: UI-P03 y UI-P04; UI-R02 para la operación de recepción.
- Decisiones: D-01, D-02, D-03 para acceso interno y D-04 para pagos de consultas en línea y alcance del cajero.
- Pendientes que afectan implementación: P-01, P-03, P-04, P-05 y P-11.
- Propuestas a revisar: PRN-01, PRN-02 y PRN-05.

## Actores, datos y permisos

- **Paciente autenticado:** agenda únicamente para sí mismo.
- **Recepcionista autenticada y dentro de VPN:** puede crear una cita para un paciente registrado. Su acceso a la agenda no concede acceso al historial médico ni a recetas.
- **Doctor:** aparece como opción de búsqueda si pertenece a la especialidad elegida y su jornada permite el horario. No crea esta cita desde su perfil en este flujo.
- **Entradas visibles:** especialidad y costo, doctor, fecha, horario y paciente. El paciente proviene de la sesión o de la selección autorizada de recepción.
- **Salidas:** folio, estado inicial, fecha y horario, paciente, doctor, especialidad, consultorio, línea de pago, leyenda de ocho horas y política de cancelación.

Los campos del comprobante proceden de la fuente. El formato del folio, la línea de pago, la duración de consulta y la forma de asignar consultorio requieren definición antes de programar.

## Recorrido principal esperado

1. La persona entra a Agendar cita, elige especialidad y ve su costo.
2. Elige un doctor de esa especialidad.
3. Ve fechas y horarios disponibles dentro del intervalo permitido y de la jornada del doctor.
4. Revisa los datos de la cita.
5. Al confirmar, el servidor revalida las reglas y crea una sola cita pendiente de pago.
6. El sistema presenta el comprobante y la línea de pago. Se informa que el pago debe confirmarse dentro de ocho horas.

La revalidación al confirmar y la atomicidad de la reserva son propuestas de implementación para evitar ocupación simultánea; documentarlas explícitamente al preparar el plan técnico.

## Casos alternativos y errores

- Fecha fuera del intervalo de RN-01 o en el pasado: mostrar una razón comprensible y no crear cita.
- Horario ya ocupado por ese doctor o fuera de su jornada: mostrar disponibilidad actualizada; no crear cita.
- Paciente con cita pendiente con el mismo doctor: explicar el conflicto y no crear otra.
- Horario tomado entre visualización y confirmación: informar el conflicto y permitir volver a elegir; la fuente pide mostrar errores y reiniciar la solicitud, por lo que debe acordarse cómo preservar datos ya capturados.
- Especialidad sin doctores u horario sin disponibilidad: mostrar estado vacío con siguiente acción clara.
- Solicitud sin sesión válida o sin permiso: rechazarla en servidor.

## Criterios de aceptación del borrador

| ID | Dado / cuando / entonces | Reglas |
| --- | --- | --- |
| CA-01 | Dado un paciente autenticado, un doctor y un espacio válidos, cuando confirma la solicitud, entonces se crea una única cita pendiente de pago y se muestra un comprobante con todos los campos exigidos | RN-01/02/03/04/06; RF-05/06 |
| CA-02 | Dada una fecha anterior a 48 horas o posterior a tres meses, cuando intenta confirmar, entonces el servidor rechaza la solicitud y no crea una cita | RN-01; límite exacto P-05 |
| CA-03 | Dado un doctor ocupado o un horario fuera de su jornada, cuando se intenta confirmar, entonces no se crea cita y se informa por qué | RN-02/04; duración P-03 |
| CA-04 | Dado un paciente con otra cita pendiente para el mismo doctor, cuando intenta confirmar, entonces se rechaza la nueva cita | RN-03; definición de pendiente P-04 |
| CA-05 | Dadas dos solicitudes simultáneas para el mismo espacio del doctor, cuando ambas intentan confirmar, entonces como máximo una obtiene una cita | RN-02; PRN-02 |
| CA-06 | Dado un usuario ajeno o una recepcionista fuera de VPN, cuando solicita crear la cita por otra persona, entonces el servidor rechaza la operación | RF-01; RNF-03/04 |
| CA-07 | Dada una cita creada, cuando se abre su comprobante, entonces aparecen folio, paciente, fecha, horario, consultorio, especialidad, doctor, línea de pago, plazo de ocho horas y política de cancelación | RF-06; RN-06 |
| CA-08 | Dada una validación fallida o ausencia de horarios, cuando la persona consulta el resultado, entonces ve un mensaje específico y puede retomar o reiniciar la solicitud según la decisión de interfaz registrada | S1 p. 2; UI-P03 |

**Límite de esta versión:** CA-02 a CA-05 tienen partes sin definición suficiente para declararse aceptadas o programarse. Ejemplo: el texto «tres meses» requiere acordar si son meses calendario; «ocupado» requiere duración de la cita; «pendiente» requiere estados concretos.

## Preguntas para resolver con el equipo

1. P-03: ¿Cuánto dura cada consulta? ¿Duración fija o variable por especialidad? ¿Cómo se modelan descansos?
2. P-04: ¿Qué estados cuentan para la restricción de cita pendiente con el mismo doctor?
3. P-05: ¿Cómo se cuentan tres meses, el instante de 48 horas y el inicio del plazo de pago?
4. P-11: ¿Cómo se elige consultorio y se evitan dos citas simultáneas en el mismo consultorio?
5. P-01: ¿Qué proveedor e integración emiten y verifican la línea de captura para pagar consultas en línea? ¿Qué evidencia se conserva y la demostración académica usará una conexión real o una simulación identificada?
6. PRN-05: ¿Se congela en la cita el costo visto al agendar?

## Plan técnico y tareas

Pendientes hasta que el equipo confirme las reglas anteriores y seleccione stack. Al planear: esquema SQL Server y restricciones, servicio de disponibilidad, creación transaccional, autorización, generación de comprobante, interfaz y pruebas de criterios CA-01 a CA-08. No crear tablas o endpoints definitivos a partir de un boceto.

## Verificación

Por ahora solo se puede revisar la coherencia del documento y prototipo. No hay implementación ni resultados de pruebas. Tras implementar, registrar evidencia de cada CA-*, incluidos rechazos, límites exactos, concurrencia y permisos.
