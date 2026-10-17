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
| D-03 | Las funciones de recepcionista, administrador y cajero están restringidas a la red privada del hospital mediante VPN | EQUIPO; alcance de red aclarado por el usuario, 2026-10-16 |
| D-04 | El cajero cobra únicamente medicamentos y servicios adicionales del hospital. Las consultas se pagan por anticipado en línea mediante línea de captura; sus pagos, cancelaciones y reembolsos se gestionan en línea, fuera del flujo de caja. Recepción no cobra | EQUIPO; aclaración explícita del usuario, 2026-10-16 |
| D-05 | Desarrollo guiado por especificaciones, usando Codex y Claude | EQUIPO |
| D-06 | Primer trabajo de Claude Design: mapa general de los cinco roles | EQUIPO |
| D-07 | Claude Code y Codex comparten las skills del proyecto; las actualizaciones de las skills del proyecto de Claude también deben estar disponibles para Codex | Instrucción explícita del usuario, 2026-10-15 |
| D-08 | Usar nombres de documentos Markdown en inglés en ambas versiones de idioma; la documentación principal está en inglés con espejos en español. El documento 06 extrae el contenido de las fuentes pertinente al proyecto; los PDFs originales conservan sus nombres | Instrucción explícita del usuario, 2026-10-16; conservar los PDFs sigue las instrucciones del proyecto |
| D-09 | El doctor debe usar el mismo acceso por VPN a la red del hospital para las funciones de consultorio: atención, datos del paciente/clínicos, historial médico, diagnósticos, tratamientos y recetas | Instrucción explícita del usuario, 2026-10-16 |

Restricción académica: Microsoft SQL Server (S1, p. 1). El lenguaje de programación es libre. La implementación concreta de la VPN sigue pendiente; la decisión de exigirla está confirmada.

## Acceso a la red del hospital mediante VPN

D-03 y D-09 restringen las operaciones de recepción, administración y caja, y las funciones de consultorio del doctor, a la red privada del hospital mediante una conexión VPN autorizada. Estas funciones protegidas no deben ser accesibles directamente desde Internet público, aunque se tengan credenciales válidas de la aplicación.

Para el doctor, la restricción abarca leer datos del paciente y datos clínicos durante la atención, consultar el historial médico, registrar la consulta, diagnósticos y tratamientos, y emitir o consultar recetas (RF-11/RF-12; UI-D02/UI-D03/UI-D04). Esta decisión no extiende automáticamente la misma restricción a todas las funciones del doctor: la política de red para agenda, perfil y solicitudes de cancelación queda por definir en P-10.

El acceso por VPN complementa la autenticación y autorización por rol de la aplicación; el servidor debe aplicar ambas. Una conexión VPN por sí sola no concede permisos clínicos ni elimina la prohibición de que recepción consulte recetas e historiales médicos. Es un requisito documentado, no un control implementado.

P-10 debe distinguir el acceso a la red del hospital de la presencia física en él: sigue pendiente si la VPN admitirá conexiones originadas fuera de las instalaciones. También están pendientes el proveedor, la topología y el comportamiento ante la pérdida de conexión. D-03/D-09 son decisiones del equipo adicionales a la fuente académica, que no especifica una VPN.

## Alcance

Incluye cuentas y roles, pacientes, doctores y jornadas, empleados, especialidades, consultorios, citas con prepago, cancelaciones, consultas, historial médico, recetas, farmacia, servicios extras, cobros, tickets, devoluciones y bitácoras.

El prepago de consultas en línea mediante línea de captura y la gestión en línea de cancelaciones/reembolsos están confirmados por D-04. El proveedor, el mecanismo de verificación/conciliación y si la demostración académica usa una integración real o una simulación explícitamente identificada siguen pendientes en P-01/P-05/P-07. Estos flujos no involucran al cajero. La cancelación del doctor sigue requiriendo aprobación de recepción mediante la aplicación web (RN-08).

No comprometidos para esta versión: aseguradoras, hospitalización, telemedicina, facturación fiscal, aplicación móvil nativa o escritorio. Son límites propuestos, no prohibiciones académicas.

## Distribución de responsabilidades

| Rol | Responsabilidad | Restricción / estatus |
| --- | --- | --- |
| Paciente | Registro propio; sus datos y citas; agendar y cancelar | S1. Acceso a recetas propias aún por decidir |
| Doctor | Agenda, atención, historial médico, recetas y solicitud de cancelación | S1. Sin autorregistro ni edición de datos sensibles; las funciones de consultorio requieren acceso por VPN a la red del hospital (D-09) |
| Recepcionista | Altas administrativas, agenda y cancelaciones; aprobación de solicitudes del doctor | S1 + D-04. Sin cobros, recetas ni historial médico |
| Cajero | Ventas, cobros y tickets de medicamentos y servicios adicionales | D-04; sin pagos, cancelaciones ni reembolsos de consultas |
| Administrador | Cuentas, roles, catálogos, inventario y consulta de bitácoras | Distribución propuesta; S1 solo explicita su posibilidad de registrar recepcionistas |

S1 permite a recepción registrar doctores y otras recepcionistas. No se elimina ese permiso automáticamente al añadir administrador. Compartir o reasignar esas operaciones debe resolverse en P-02. Como propuesta inicial, cajero y administrador no reciben acceso al contenido clínico por el solo hecho de tener esos roles.

## Decisiones pendientes

| ID | Pregunta | Impacta |
| --- | --- | --- |
| P-01 | El prepago de consultas en línea mediante línea de captura está confirmado (D-04). ¿Qué proveedor emite/verifica la referencia, qué evidencia se conserva y la integración académica será real o simulada? | Integración de pago en línea; los bocetos no deben afirmar una conexión real |
| P-02 | ¿Qué altas/ediciones comparten administración y recepción? ¿Quién administra jornadas, precios e inventario? ¿Un usuario puede tener varios roles? | Matriz definitiva de permisos |
| P-03 | ¿Cuánto dura una consulta y cómo se representa una jornada con descansos? | Disponibilidad, traslapes y agenda |
| P-04 | ¿Qué estados cuentan como cita pendiente? ¿El doctor ve solo pacientes vinculados a sus citas? ¿El paciente puede ver sus recetas? | Permisos y agendamiento |
| P-05 | ¿Las 8 horas empiezan al crear la cita? ¿Qué fecha verificada determina la puntualidad del pago en línea y cómo se concilian notificaciones tardías o dinero recibido después del vencimiento sin duplicar reservas? ¿Tres meses son meses calendario? | Límites temporales y conciliación en línea |
| P-06 | ¿Se permite cancelar después de la hora de cita? ¿Quién registra Atendida/No acudió y cuándo? ¿Qué ocurre al rechazar una solicitud del doctor? | Transiciones de estados |
| P-07 | Los reembolsos de consultas se gestionan en línea, fuera de caja (D-04). ¿Qué proveedor/proceso los ejecuta, con qué plazos, evidencia, base de cálculo y responsable de excepciones? Por separado, ¿se pueden anular ventas de medicamentos/servicios? | Reembolsos de consultas en línea; política separada de ventas |
| P-08 | ¿Una venta de medicamento exige receta? ¿Se controlan lotes/caducidad y unidades? ¿Cómo se registran existencias iniciales? | Farmacia; S1 no establece estas reglas |
| P-09 | Nombre, identidad visual y campos personales obligatorios. ¿Se manejan menores y tutores? | Bocetos y formularios |
| P-10 | Stack, despliegue, proveedor/topología de VPN, si se permiten conexiones VPN desde fuera de las instalaciones del hospital, política de red para las funciones no clínicas del doctor, cierre de sesión y comportamiento si se pierde VPN durante una operación | Diseño técnico y acceso a la red del hospital; D-03/D-09 definen las funciones protegidas |
| P-11 | ¿Cómo se reservan consultorios y se impiden traslapes entre doctores que comparten uno? | Agenda; regla adicional propuesta |
| P-12 | ¿Qué acciones clínicas requieren corrección posterior y cómo se conserva su historial? ¿Quién puede consultar cada bitácora? | Historial, recetas y auditoría |

Los bocetos pueden representar los pendientes como alternativas explícitas; una opción visual no los resuelve por sí sola. Definir P-01/P-02/P-03 antes de concretar los flujos operativos correspondientes.

## Próximo ciclo

1. Revisar problemática, RF/RNF y reglas con el equipo.
2. Elaborar el mapa general y navegación de cinco roles en Claude Design.
3. Registrar lo aprendido del boceto; resolver los pendientes que afecten al siguiente flujo.
4. Especificar el agendamiento y su pago; después elaborar modelo de datos y diseño técnico.
