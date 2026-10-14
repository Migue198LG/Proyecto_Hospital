# Contexto y decisiones

Estado: borrador v0.1, 2026-10-12. Nombre provisional: Sistema hospitalario.

## Fuentes y estatus

| Clave | Fuente | Uso |
| --- | --- | --- |
| S1 | `contexto/ESPECIFICACIONES PROYECTO FINAL BASES DE DATOS 26-2.pdf`, cinco páginas | Funciones, reglas, datos y permisos académicos |
| S2 | `contexto/Rúbrica_Eval_Proyecto_1P.pdf` | Entregables de primera evaluación |
| S3 | `contexto/Rúbrica_Eval_Proyecto_2P.pdf` | Entregables de segunda evaluación |
| EQUIPO | Conversación con el equipo del 2026-10-12 | Decisiones explícitas de alcance y forma de trabajo |

**Confirmado:** proviene de una instrucción explícita del equipo. **Fuente:** requerido por un PDF. **Propuesto:** recomendación todavía revisable. **Pendiente:** información sin decidir. Todo el paquete está en borrador; la extracción de un requisito no equivale a la aprobación de su redacción final.

## Decisiones confirmadas

| ID | Decisión | Origen |
| --- | --- | --- |
| D-01 | Cinco roles: paciente, doctor, recepcionista, administrador y cajero | EQUIPO |
| D-02 | Todas las interfaces serán web; se descarta la aplicación de escritorio | EQUIPO |
| D-03 | Recepcionista, administrador y cajero trabajan con acceso restringido por VPN | EQUIPO |
| D-04 | El cajero se encarga de cobrar; recepción deja de cobrar | EQUIPO |
| D-05 | Desarrollo guiado por especificaciones, usando Codex y Claude | EQUIPO |
| D-06 | Primer trabajo de Claude Design: mapa general de los cinco roles | EQUIPO |

Restricción académica: Microsoft SQL Server (S1, p. 1). El lenguaje de programación es libre. La implementación concreta de la VPN sigue pendiente; la decisión de exigirla está confirmada.

## Alcance

Incluye cuentas y roles, pacientes, doctores y jornadas, empleados, especialidades, consultorios, citas con prepago, cancelaciones, consultas, historial médico, recetas, farmacia, servicios extras, cobros, tickets, devoluciones y bitácoras.

No comprometidos para esta versión: pasarela bancaria real, aseguradoras, hospitalización, telemedicina, facturación fiscal, aplicación móvil nativa o escritorio. Son límites propuestos, no prohibiciones académicas.

## Distribución de responsabilidades

| Rol | Responsabilidad | Restricción / estatus |
| --- | --- | --- |
| Paciente | Registro propio; sus datos y citas; agendar y cancelar | S1. Acceso a recetas propias aún por decidir |
| Doctor | Agenda, atención, historial médico, recetas y solicitud de cancelación | S1. Sin autorregistro ni edición de datos sensibles |
| Recepcionista | Altas administrativas, agenda y cancelaciones; aprobación de solicitudes del doctor | S1 + D-04. Sin cobros, recetas ni historial médico |
| Cajero | Cobros de citas, ventas, tickets y devoluciones | Cobros confirmados por D-04; detalle de permisos propuesto |
| Administrador | Cuentas, roles, catálogos, inventario y consulta de bitácoras | Distribución propuesta; S1 solo explicita su posibilidad de registrar recepcionistas |

S1 permite a recepción registrar doctores y otras recepcionistas. No se elimina ese permiso automáticamente al añadir administrador. Compartir o reasignar esas operaciones debe resolverse en P-02. Como propuesta inicial, cajero y administrador no reciben acceso al contenido clínico por el solo hecho de tener esos roles.

## Decisiones pendientes

| ID | Pregunta | Impacta |
| --- | --- | --- |
| P-01 | ¿Cómo paga el paciente dentro de las 8 horas: en caja, transferencia, simulación o pasarela? ¿Quién confirma cada método y qué evidencia conserva? | Flujo de pago; no ofrecer pago en línea real en el boceto |
| P-02 | ¿Qué altas/ediciones comparten administración y recepción? ¿Quién administra jornadas, precios e inventario? ¿Un usuario puede tener varios roles? | Matriz definitiva de permisos |
| P-03 | ¿Cuánto dura una consulta y cómo se representa una jornada con descansos? | Disponibilidad, traslapes y agenda |
| P-04 | ¿Qué estados cuentan como cita pendiente? ¿El doctor ve solo pacientes vinculados a sus citas? ¿El paciente puede ver sus recetas? | Permisos y agendamiento |
| P-05 | ¿Las 8 horas empiezan al crear la cita? ¿Qué pasa con un pago exactamente al vencer o recibido antes pero registrado después? ¿Tres meses son meses calendario? | Límites temporales |
| P-06 | ¿Se permite cancelar después de la hora de cita? ¿Quién registra Atendida/No acudió y cuándo? ¿Qué ocurre al rechazar una solicitud del doctor? | Transiciones de estados |
| P-07 | ¿Cómo y cuándo se ejecuta una devolución? ¿Se aplica sobre el importe pagado? ¿Se pueden anular ventas? | Operación de caja |
| P-08 | ¿Una venta de medicamento exige receta? ¿Se controlan lotes/caducidad y unidades? ¿Cómo se registran existencias iniciales? | Farmacia; S1 no establece estas reglas |
| P-09 | Nombre, identidad visual y campos personales obligatorios. ¿Se manejan menores y tutores? | Bocetos y formularios |
| P-10 | Stack, despliegue, topología de VPN, cierre de sesión y comportamiento si se pierde VPN durante una operación | Diseño técnico y acceso interno |
| P-11 | ¿Cómo se reservan consultorios y se impiden traslapes entre doctores que comparten uno? | Agenda; regla adicional propuesta |
| P-12 | ¿Qué acciones clínicas requieren corrección posterior y cómo se conserva su historial? ¿Quién puede consultar cada bitácora? | Historial, recetas y auditoría |

Los bocetos pueden representar los pendientes como alternativas explícitas; una opción visual no los resuelve por sí sola. Definir P-01/P-02/P-03 antes de concretar los flujos operativos correspondientes.

## Próximo ciclo

1. Revisar problemática, RF/RNF y reglas con el equipo.
2. Elaborar el mapa general y navegación de cinco roles en Claude Design.
3. Registrar lo aprendido del boceto; resolver los pendientes que afecten al siguiente flujo.
4. Especificar el agendamiento y su pago; después elaborar modelo de datos y diseño técnico.
