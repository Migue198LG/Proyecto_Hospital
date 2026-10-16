# Requisitos del proyecto extraídos de las fuentes originales

Estado: extracción de fuentes para planear el proyecto, 2026-10-16. Este documento conserva los requisitos, reglas, datos, ejemplos y criterios de evaluación del proyecto contenidos en los tres PDFs. Se omiten encabezados institucionales, logotipos y pies de página repetidos. La redacción y las etiquetas de campos se presentan de forma legible; no es una transcripción literal ni una propuesta de esquema de base de datos.

Estos son requisitos de las fuentes académicas. Las decisiones posteriores del equipo y las interpretaciones pendientes se registran por separado en [contexto y decisiones](00-context.md). Consultar [requerimientos](02-requirements.md) y [reglas de negocio](03-business-rules.md) para los identificadores RF/RNF/RN existentes; este documento no los sustituye ni renumera.

## Fuentes

| Clave | Documento original | Cobertura |
| --- | --- | --- |
| S1 | [Especificaciones del proyecto](../../contexto/ESPECIFICACIONES%20PROYECTO%20FINAL%20BASES%20DE%20DATOS%2026-2.pdf) | Alcance, funciones, datos y permisos del proyecto; cinco páginas físicas |
| S2 | [Rúbrica de la primera evaluación](../../contexto/Ru%CC%81brica_Eval_Proyecto_1P.pdf) | Entregables y ponderaciones de la primera entrega; una página |
| S3 | [Rúbrica de la segunda evaluación](../../contexto/Ru%CC%81brica_Eval_Proyecto_2P.pdf) | Entregables y ponderaciones de la segunda entrega; una página |

## Objetivo y requisitos generales

Fuente: S1, p. 1. Requisitos relacionados: RF-01 y RNF-01.

- Desarrollar un sistema gestor de base de datos que gestione citas de un hospital, farmacia, servicios, recetas y consultorios.
- Los equipos pueden tener como máximo cuatro alumnos.
- El lenguaje de programación es libre.
- El manejador de base de datos debe ser Microsoft SQL Server.
- El sistema debe incluir un módulo de inicio de sesión.
- La fuente exige al menos tres perfiles: doctor, paciente y recepcionista. Los perfiles de cajero o farmacéutico son opcionales en la fuente.

Entidades mínimas a desarrollar (S1, p. 2): empleados, doctores, pacientes, citas, consultorios, especialidades, recetas, farmacia/medicamentos, bitácora, pago y servicios.

## Agendamiento de citas y pago

Fuente: S1, pp. 1–2. Requisitos relacionados: RF-05/RF-06/RF-07; reglas RN-01 a RN-06 y RN-09.

- Las citas deben agendarse con al menos 48 horas y como máximo tres meses de anticipación. No se permiten citas para el mismo día ni fechas pasadas.
- No se puede agendar con un doctor que ya esté ocupado en esa fecha y horario.
- Un paciente no puede agendar otra cita con el mismo doctor mientras tenga una cita pendiente con él.
- Las citas deben estar dentro de la jornada laboral del doctor.
- Las citas no se pueden reagendar. Se deben cancelar y solicitar una nueva.
- Al agendar, se conceden ocho horas al paciente para confirmar el pago.
- La cancelación por falta de pago libera el horario de la cita.

Los siete estados de cita incluidos en la fuente son:

1. Agendada pendiente de pago.
2. Pagada pendiente por atender.
3. Cancelada por falta de pago (se libera el horario).
4. Cancelada por el paciente (aplica la política de cancelación).
5. Cancelada por el doctor (devolución del 100%).
6. Atendida.
7. No acudió.

## Cancelaciones y devoluciones

Fuente: S1, pp. 1–3 y 5. Requisitos relacionados: RF-09/RF-10; reglas RN-07/RN-08.

La política de cancelación del paciente se expresa en la fuente de la siguiente manera:

| Anticipación indicada en la fuente | Devolución del pago |
| --- | --- |
| 48 horas | 100% |
| 24 horas | 50% |
| Menos de 24 horas | 0% |

Los pacientes pueden cancelar sus citas conforme a esta política. Los doctores requieren la aprobación previa de recepción para cancelar una cita, y las cancelaciones del doctor reciben una devolución del 100%. Recepción puede cancelar citas por parte del paciente o del doctor.

Nota para la planeación: la fuente no define explícitamente intervalos de tiempo completos, cancelaciones después del inicio de la cita, la base para calcular la devolución ni cómo se entrega. La interpretación de intervalos en RN-07 y las preguntas P-06/P-07 siguen sujetas a revisión; no se resuelven aquí.

## Funciones del paciente y flujo de agendamiento

Fuente: S1, pp. 2–3. Requisitos relacionados: RF-02/RF-05/RF-06/RF-08/RF-09; reglas RN-10/RN-18/RN-19.

Los pacientes pueden registrarse, consultar sus datos personales, consultar su historial de citas y cancelar sus citas. La lista debe mostrar todas las citas que haya realizado el paciente, con todos sus datos y estado actual, permitir la cancelación y filtrar por fecha(s) o estado.

La interfaz de ejemplo para pacientes tiene secciones de datos personales, citas agendadas y agendamiento de una nueva cita. Su secuencia de agendamiento es:

1. Seleccionar una especialidad. El costo de la consulta depende de la especialidad y debe haber al menos diez especialidades.
2. Seleccionar un doctor. Debe haber al menos cuatro doctores por especialidad.
3. Seleccionar una fecha, mostrando únicamente las fechas disponibles.
4. Seleccionar un horario, mostrando únicamente los horarios disponibles.
5. Si la operación tiene éxito, generar un comprobante de cita y una línea de pago. Si falla, mostrar los errores mediante un mensaje y reiniciar el flujo.

Las especialidades enumeradas son cardiología, dermatología, ginecología, medicina general, nefrología, nutriología, oftalmología, oncología, ortopedia y pediatría.

El comprobante de cita incluye:

- Folio de la cita.
- Nombre del paciente.
- Fecha y horario.
- Consultorio.
- Especialidad y doctor.
- Línea de pago.
- Una leyenda con el plazo de ocho horas para pagar.
- Una leyenda con la política de cancelación.

## Funciones del doctor y datos clínicos

Fuente: S1, p. 3. Requisitos relacionados: RF-03/RF-04/RF-08/RF-11/RF-12; reglas RN-11/RN-12/RN-13.

La interfaz de ejemplo para doctores incluye datos del doctor, recetas, datos del paciente, citas e historial médico del paciente.

- Los doctores no pueden registrarse por sí mismos; recepción los registra.
- Los doctores no pueden editar su número de empleado, cédula profesional, CURP, nombre ni especialidad.
- Los doctores solo pueden cancelar una cita con la aprobación previa de una recepcionista.
- Un doctor solo puede ejercer una especialidad a la vez.
- Cada doctor tiene una jornada laboral; no se pueden agendar citas fuera de ella.

| Documento | Campos enumerados en la fuente |
| --- | --- |
| Receta | Folio de receta, fecha, nombre del doctor, cédula profesional, nombre del paciente, edad, diagnóstico, medicamento(s), tratamiento(s), observaciones |
| Historial médico del paciente | Identificador del historial médico, identificador del paciente, nombre del paciente, alergias, tipo de sangre, padecimientos previos, peso, estatura |

## Recepción, farmacia, servicios y ventas

Fuente: S1, pp. 3–5. Requisitos relacionados: RF-03/RF-04/RF-09/RF-13/RF-14; reglas RN-14/RN-15/RN-16/RN-18.

La interfaz de ejemplo de recepción incluye recepcionistas, doctores, especialidades, consultorios, pacientes, citas, servicios adicionales, farmacia/inventario de medicamentos, cobros/tickets y las dos bitácoras descritas más adelante.

- Una recepcionista puede ser registrada por otra recepcionista o por un administrador.
- Recepción puede registrar y consultar recepcionistas, doctores y pacientes.
- Recepción no puede consultar recetas médicas ni el historial médico de un paciente.
- Recepción puede cancelar citas por parte del paciente o del doctor.
- La fuente permite que una recepcionista cobre medicamentos y servicios, o que se cree un perfil específico para esa actividad. La reasignación posterior del equipo se indica más adelante.
- Los servicios adicionales deben ser distintos de las consultas y los medicamentos. Se requieren al menos tres. Ejemplos: inyección, vacuna, curación y estudio de sangre.
- La sección de farmacia abarca el inventario de medicamentos.
- La sección de cobros/tickets suma los importes de servicios y medicamentos, según corresponda.
- Un cliente no necesita estar registrado como paciente del hospital para comprar un servicio o medicamento.

## Bitácoras y permisos

Fuente: S1, pp. 4–5. Requisito relacionado: RF-15; regla RN-17.

| Bitácora | Campos enumerados en la fuente |
| --- | --- |
| Estado de la cita | Folio de cita, fecha del movimiento, estado de la cita, fecha de la cita, identificador de especialidad, costo, política de cancelación, monto devuelto |
| Historial de citas médico–paciente | Identificador del historial, usuario que realiza el movimiento (paciente/doctor/recepcionista), máquina/IP (opcional), folio de cita, fecha de la cita, hora de la cita, identificador del paciente, folio de receta, identificador del doctor, estado de la consulta (atendida/no asistió), especialidad, consultorio |

Las bitácoras permiten únicamente consulta e inserción. Actualizar y eliminar registros está prohibido para todos los usuarios. Incluir un folio de receta en una bitácora no anula la prohibición de que recepción consulte las recetas.

## Entregables de la primera evaluación

Fuente: S2, p. 1.

| Entregable | Instrucciones de la fuente | Ponderación |
| --- | --- | --- |
| Problemática | Describir la problemática que se pretende resolver | 5% |
| Reglas de negocio | Definir las reglas aplicables al proyecto; solo algunas fueron proporcionadas | 5% |
| Requerimientos funcionales | Sin observación adicional en la rúbrica | 8% |
| Requerimientos no funcionales | Sin observación adicional en la rúbrica | 7% |
| Tres diagramas de contexto | Niveles 0, 1 y 2 | 30% |
| Diagrama entidad–relación | Indicar PK, FK, cardinalidad, atributos multivaluados y compuestos, etc. | 30% |
| Diccionario de datos en tablas de Excel | Incluir llave, campo, tipo de dato, tamaño y si acepta nulos | 15% |
| Total | | 100% |

## Entregables de la segunda evaluación

Fuente: S3, p. 1.

| Entregable | Instrucciones de la fuente | Ponderación |
| --- | --- | --- |
| Diagrama de casos de uso | Documentación | 10% |
| Diagramas de secuencia | Documentación | 10% |
| Modelo relacional normalizado | Documentación | 10% |
| Script de estructura de la base de datos | Adjuntar un script `.sql` | 10% |
| Conexión a la base de datos | Demostrar durante la revisión en clase | 10% |
| Al menos diez registros por tabla, cuando aplique | Insertar antes de la revisión | 5% |
| Cuatro vistas | Documentar y programar en SQL | 7.5% |
| Cuatro funciones | Documentar y programar en SQL | 7.5% |
| Insertar una cita desde la aplicación, con sus validaciones | Desde una aplicación o página web | 30% |
| Total | | 100% |

## Expectativas de validación y entrega

Fuente: S1, p. 5.

Conforme se aborden los temas en clase, los alumnos deben desarrollar los entregables indicados en la presentación de bienvenida. Se anunciarán la rúbrica, las ponderaciones y la fecha de cada entrega. Los alumnos deben analizar, diseñar e implementar todas las validaciones necesarias para el funcionamiento correcto del sistema. La fuente no enumera todas las validaciones ni resuelve cada detalle de negocio.

## Decisiones posteriores del equipo y preguntas pendientes

Esta sección es contexto para la planeación, no texto de los PDFs. Consultar [00-context.md](00-context.md) como registro de referencia de decisiones y preguntas.

- D-01 confirma cinco roles: paciente, doctor, recepcionista, cajero y administrador. El carácter opcional del cajero en la fuente no revierte esta decisión.
- D-02 confirma una aplicación completamente web. D-03 exige acceso por VPN para recepcionistas, cajeros y administradores; son decisiones posteriores del equipo, no requisitos expresados en S1.
- D-04 asigna los cobros al cajero. La posibilidad de cobrar que la fuente concede a recepción no debe usarse como permiso actual del equipo.
- Siguen pendientes el método y la confirmación del pago (P-01), los permisos administrativos (P-02), la duración de consultas y jornadas (P-03), el significado de cita pendiente y el acceso clínico (P-04), y los límites de tiempo exactos (P-05). Los detalles de cancelaciones/devoluciones, reglas de farmacia, datos personales, infraestructura, conflictos de consultorios y correcciones clínicas/acceso a bitácoras permanecen en P-06 a P-12.

Conservar estas distinciones al redactar especificaciones de funcionalidades. Los bocetos y esta extracción no demuestran que la autenticación, los permisos, el acceso por VPN o las reglas de negocio estén implementados.
