# Sistema de gestión hospitalaria — plan del proyecto revisado

Estado: propuesta de revisión, 2026-10-16; actualizada con la aclaración confirmada de D-04 por el usuario: caja maneja solo medicamentos/servicios adicionales, mientras pagos por línea de captura, cancelaciones y reembolsos de consultas son en línea. Esta aclaración no aprueba las demás propuestas D-10–D-23. Registrar fecha y alcance reales cuando se aprueben; no marcar todos los documentos como aprobados automáticamente.

## Fundamento y prioridades

Conservar D-01–D-09 y todos los identificadores RF/RNF/RN/UI/SPEC/CA existentes. Los PDF originales siguen siendo la autoridad académica; la [extracción de fuentes](../docs/06-source-requirements.md) es la referencia de trabajo, y el [contexto](../docs/00-context.md) registra decisiones posteriores del equipo. Documentar cualquier diferencia respecto de un requisito de fuente y la validación necesaria con el profesor. Revisar un plan no demuestra que el sistema funcione.

La primera entrega está prevista para el **2026-10-20**, según lo indicado por el usuario. Priorizar la rúbrica: planteamiento del problema, reglas de negocio, RF/RNF, tres diagramas de contexto/flujo de datos, diagrama ER y diccionario de datos en Excel. SQL Server, consultas, recetas, inventario, servicios, ventas y bitácoras siguen dentro del alcance, aunque la segunda rúbrica demuestre específicamente la inserción de citas. No son ampliaciones opcionales.

Se deben conservar los cambios existentes en el árbol de trabajo. Los archivos y habilidades de agentes están actualmente ignorados por Git; `.agents/skills` apunta a `../.claude/skills`. Conservar esta organización. Los procedimientos de ingeniería compartidos que necesiten los compañeros también deben aparecer en documentación y scripts versionados.

## Propuestas revisadas D-10–D-23

### D-10 — Stack y entorno de base de datos soportado

Usar Node.js 24 LTS con una versión de mantenimiento vigente, TypeScript, Express, EJS, JavaScript mínimo en el navegador, `mssql`, Vitest, ESLint y Prettier. Fijar la versión principal del entorno y el archivo de bloqueo de dependencias. El Node 22.14 instalado es una observación del inventario, no una razón para congelar una versión antigua; Node 22 está en mantenimiento y 24 ofrece una base con mayor horizonte de soporte. [Calendario de versiones de Node](https://github.com/nodejs/Release).

Usar SQL Server 2022 Developer para el entorno académico de desarrollo. Disponer de un equipo Linux x86-64 para el contenedor de SQL Server, accesible desde la Mac por una conexión privada autorizada. Una instalación soportada de SQL Server en Windows es la alternativa si ese es el equipo disponible. Asignar al responsable del servidor antes de M3. No exigir la emulación en Apple Silicon como vía de desarrollo: `platform: linux/amd64` no la convierte en una plataforma soportada. Microsoft excluye del soporte los entornos de traducción/emulación. [Despliegue de contenedores de SQL Server](https://learn.microsoft.com/en-us/sql/linux/containers/deploy?view=sql-server-ver17).

Antes de desarrollar la aplicación, verificar conexión real, reversión de transacciones, persistencia después de reiniciar e integración del almacenamiento de sesiones elegido en ese servidor. Es una comprobación futura de preparación, no una afirmación sobre la máquina actual.

### D-11 — Transacciones, migraciones y reintentos

Conservar las operaciones críticas en procedimientos almacenados con `SET XACT_ABORT ON`, responsabilidad explícita sobre la transacción, manejo de errores/reversión e inserción de auditoría dentro de la misma transacción. Usar restricciones en la base de datos, autorización en el servidor y llamadas parametrizadas. La identidad de ejecución recibe únicamente los permisos necesarios sobre procedimientos/vistas; no debe ser `sa`, propietaria de la base, propietaria del esquema ni la identidad de migración.

Usar migraciones ordenadas y versionadas con un registro de versiones aplicadas. Utilizar `CREATE OR ALTER` para objetos programables cuando corresponda; no ocultar diferencias del esquema con comprobaciones generales de existencia llamadas “idempotentes”. Generar el script SQL completo de la rúbrica a partir de un orden de aplicación determinista. Separar privilegios de ejecución, migración y carga de datos de prueba.

Agregar identificadores persistentes de operación para reserva, pago, emisión de reembolso y venta. Reintentar la misma solicitud devuelve el resultado original; reutilizarla con datos diferentes falla. Definir unicidad y retención en el modelo. Bloquear recursos en un orden consistente, limitar reintentos por interbloqueo e informar los errores según la restricción violada: una reserva duplicada paciente/doctor no siempre significa “horario ocupado”.

### D-12 — Prepago de consultas en línea y vencimiento confiable

D-04 confirma el prepago de consultas en línea mediante línea de captura, separado de ventas de medicamentos/servicios adicionales en caja. Proponer un único pago completo en MXN por el costo congelado, sin parcialidades ni sobrepagos. Proveedor/emisor de referencia e integración académica real o simulada siguen en P-01. Un simulador identificado puede demostrar el comportamiento solo si se elige; no es una conexión real de pagos. El cajero no puede confirmar ni conciliar pagos de consultas.

Proponer que las ocho horas consecutivas comiencen en el `created_at` registrado por la base para la reserva exitosa; mostrar vencimiento exacto, línea de captura, importe e instrucciones en línea. P-05 debe decidir la fecha autorizada de pago y el tratamiento de notificaciones tardías antes de implementar en producción. Verificar evidencia del pago en el servidor, incluidos referencia, importe, moneda e identificador único de transacción; una redirección exitosa del navegador o un comprobante cargado no deben marcar por sí solos la consulta pagada. Nunca reactivar automáticamente una cita vencida/cancelada al recibir un pago tardío: su turno podría haberse reasignado. Registrar la discrepancia financiera para conciliación/reembolso en línea, con ejecución y responsabilidad de excepciones definidas en P-07.

Conservar un proceso de vencimiento cada minuto, con recuperación al arrancar, seguimiento de última ejecución exitosa y lotes transaccionales acotados. Resolver reservas vencidas al reservar y aplicar la misma regla al consultar disponibilidad. Procesar pagos en línea y vencimientos debe compartir un protocolo de bloqueos; cuando P-05 defina la fecha autorizada, especificar el resultado exacto de la concurrencia. Persistir eventos del proveedor separados del estado de cita, deduplicar/conciliar notificaciones y conservar eventos fallidos o sin correspondencia para seguimiento en línea. La falla de un proceso o una notificación duplicada/tardía no deben causar retención indefinida de turnos, cobros duplicados ni reservas dobles.

### D-13 — Turnos, consultorios y cambios de horario

Usar turnos de 30 minutos alineados a `:00`/`:30` en todo el hospital. Representar intervalos con inicio incluido y fin excluido; los bloques y citas no cruzan medianoche en v1. Los bloques semanales incluyen día de semana, inicio/fin, consultorio y fechas de vigencia. Los descansos se representan con bloques separados. Las indisponibilidades usan intervalos fechados. Congelar inicio, fin, doctor, especialidad, consultorio, precio y política de la cita.

Serializar reservas, ediciones de bloques y cambios de indisponibilidad sobre los mismos recursos de doctor/consultorio; las indicaciones de bloqueo sin estrategia de acceso indexado y protocolo compartido no constituyen un diseño de concurrencia. Rechazar cambios de horario, consultorio, especialidad o disponibilidad que invaliden reservas futuras; resolver primero las citas afectadas mediante cancelación. Conservar las versiones de horario referenciadas.

Conservar índices únicos filtrados para reservas activas `(doctor_id, start_at)` y `(patient_id, doctor_id)`; agregar `(room_id, start_at)` activo. Proponer que un paciente no tenga citas simultáneas con distintos doctores, mediante un índice activo `(patient_id, start_at)`. Esta última restricción es una propuesta del equipo adicional a RN-03. Estas claves evitan traslapes únicamente porque todos los turnos siguen la misma alineación y duración fija; validar esa condición en la base. Los índices no sustituyen la validación del horario laboral.

### D-14 — Límites temporales y monetarios

Guardar instantes de eventos en UTC como `datetime2(3)` y usar `SYSUTCDATETIME()` de la base como reloj autorizado. Guardar fechas de nacimiento como `date` y horarios recurrentes como hora local. Mostrar la hora del hospital en `America/Mexico_City`; documentar y verificar explícitamente la correspondencia con la zona horaria de SQL Server. Así se evita depender de la configuración local del contenedor. [Reloj UTC de SQL Server](https://learn.microsoft.com/en-us/sql/t-sql/functions/sysutcdatetime-transact-sql?view=sql-server-ver17).

Capturar una única hora autorizada de la base después de adquirir los bloqueos relevantes de la operación. La reserva exige al menos 48 horas transcurridas; el máximo son tres meses calendario desde ese instante expresado en hora local del hospital y convertido después a UTC. Definir el ajuste al último día del mes y probar años bisiestos. La fecha del pago en línea y la política de notificaciones tardías siguen en P-05; no sustituir la hora del pago por la recepción de la notificación sin esa decisión. Los intervalos de reembolso usan el tiempo previo al inicio congelado.

Usar `decimal(12,2)` para importes MXN, cantidades enteras positivas, restricciones de precio/existencias no negativos y una regla explícita de redondeo: redondear reembolsos calculados a dos decimales. Nunca usar punto flotante para totales. Los folios son únicos, pero pueden contener saltos de secuencia.

### D-15 — Citas pendientes y acceso clínico

Los estados 1 y 2 cuentan como pendientes según RN-03 después de resolver vencimientos. Tener una cita no debe otorgar acceso perpetuo a todo el expediente del paciente.

Propuesta: el doctor asignado puede leer el expediente de una cita pagada desde 24 horas antes de su inicio hasta cerrar la consulta; las escrituras clínicas requieren que esa cita pagada haya comenzado. Después de completarla, el doctor puede leer su propia consulta y las recetas emitidas. El acceso al expediente más amplio requiere otra cita pagada que cumpla las condiciones. Una cita no pagada, cancelada o con inasistencia no concede acceso clínico. Las correcciones usan un flujo explícito de adendas vinculadas; los resultados de las citas permanecen finales. Aplicar el alcance por paciente en cada lectura, escritura, impresión y descarga.

Excluir un portal de recetas para pacientes en v1 es una propuesta de alcance, no una consecuencia de D-09: la obligación de VPN para el doctor no prohíbe lógicamente un portal de pacientes autorizado por separado. Registrar esa posible ampliación en la propuesta P-17.

### D-16 — Cancelaciones, resultados y reembolsos

Conservar los intervalos: al menos 48 horas → 100%; al menos 24 y menos de 48 → 50%; menos de 24 horas pero antes del inicio → 0%. Tanto la cancelación del paciente como la del doctor deben confirmarse antes del inicio. Enviar una solicitud de doctor no reserva el derecho a cancelar después; la aprobación de recepción vuelve a verificar hora y estado. Rechazar solicitudes obsoletas sin modificar una cita ya vencida, cancelada o completada.

Las transiciones permitidas siguen siendo: 1→2 sistema de pago en línea verificado; 1→3 sistema de vencimiento; 1/2→4 paciente o recepcionista en línea; 1/2→5 recepcionista en línea por aprobación o cancelación directa; 2→6 doctor asignado; 2→7 recepcionista. Resolver concurrencia de vencimiento/pago según P-05 antes de aplicar una transición. Rechazar una solicitud de cancelación deja intacta la cita. La cancelación directa de recepción por el doctor registra motivo y usuario actuante. El cajero no tiene permisos de transición de consultas.

Completar exige que haya pasado el inicio programado y que se cierre una consulta. Proponer inasistencia solo al terminar el turno o después, sin inicio de consulta registrado; bloquear frente al inicio/cierre concurrente de una consulta. La inasistencia no genera reembolso automático. No permitir que completar e indicar inasistencia compitan de forma independiente.

La cancelación calcula el derecho de reembolso sobre el pago confirmado real; la cancelación del doctor devuelve el 100%. Crear un reembolso en línea pendiente solo cuando el importe sea positivo; conservar el derecho de importe cero en la auditoría de cancelación. Enviar una solicitud idempotente mediante el mecanismo en línea elegido y marcar ejecutado solo tras evidencia verificada; pendiente, en proceso, fallido y completado son estados del flujo financiero, no estados adicionales de cita. Usar una solicitud persistente/outbox y conciliación: una transacción de base no puede hacer atómico un reembolso externo. Definir ejecutor, responsable de excepciones, evidencia y plazos en P-07; ni caja ni recepción ejecutan reembolsos monetarios de consultas. Un reembolso pendiente no mantiene ocupado el turno. No hay anulaciones de venta en la v1 académica; registrar explícitamente esa limitación.

### D-17 — Permisos y cuentas

Conservar la asignación de roles con D-04 corregida: recepción registra doctores/recepcionistas, lee ambas bitácoras, comparte horarios con administración y realiza cancelaciones/aprobaciones de doctores autorizadas en línea. Las operaciones monetarias de caja cubren solo medicamentos y servicios adicionales; no pagos, cancelaciones ni reembolsos de consultas. Recepción, cajero y administrador no acceden a contenido clínico. Recepción conserva lectura de información administrativa de catálogos/inventario de S1; editar catálogos corresponde a administración.

La matriz debe especificar crear/leer/actualizar/desactivar/aprobar/emitir/imprimir, registros propios frente a ajenos, campos sensibles y alcance de red. “Gestionar cuentas” no debe implicar elevación de roles por recepción. Solo administración crea cuentas de cajero/administrador; el primer administrador se provisiona mediante una operación de configuración documentada. Auditar registros y cambios de rol. Desactivar cuentas en lugar de eliminar personas referenciadas; revocar sesiones al desactivar o cambiar roles. No eliminar físicamente catálogos referenciados.

Una cuenta tiene un rol en v1. Separar registros de pacientes y cuentas de acceso: un paciente registrado por recepción no necesita cuenta. El acceso de empleado no funciona también como acceso de paciente; cualquier modelo futuro de roles combinados requiere otra decisión.

### D-18 — Farmacia y ventas académicas

Conservar inventario por unidad, entradas del administrador, decrementos atómicos, precios congelados por partida y ventas a pacientes registrados o clientes de mostrador identificados por nombre. Agrupar partidas repetidas de un medicamento antes de validar existencias, bloquear medicamentos en orden estable y confirmar venta, pago, movimientos y referencia de recibo juntos. Una partida referencia exactamente un medicamento o un servicio; especificar esa restricción y sus FK.

La comprobación de recetas para venta, lotes, caducidades, anulación de ventas y facturación fiscal quedan fuera de este prototipo académico ficticio. Esta exclusión no establece permiso de dispensación real. No almacenar datos reales de pacientes o tarjetas en los datos de prueba. Definir existencias como un saldo almacenado conciliado con movimientos inmutables; cada entrada/decremento se registra en la misma transacción. Los ajustes positivos y negativos requieren motivos explícitos y permiso de administrador.

### D-19 — Identidad, menores y documentos históricos

Conservar el nombre ficticio “Hospital San Mateo”, nombres estructurados, fecha de nacimiento, sexo, CURP, contacto, número/fecha de contratación del empleado y cédula/especialidad del doctor. Especificar longitudes, unicidad y opcionalidad en el diccionario; distinguir correo de acceso y correo de contacto del paciente. La validación de CURP en el prototipo verifica formato, no identidad.

Proponer autorregistro de v1 solo para adultos. Recepción registra menores con nombre del adulto responsable, parentesco y teléfono obligatorios; recepción realiza sus reservas/cancelaciones. No asignar a la cuenta de un menor el acceso compartido de su tutor ni exigir un correo único por cada menor. El portal de tutores es una función futura. Esto limita la formulación general de autorregistro de pacientes de S1; registrar la diferencia y validar con el profesor la excepción para menores. Calcular edad en la fecha pertinente; congelar al emitir la receta la edad, cédula/nombre del doctor, nombre del paciente y texto clínico para que cambios posteriores del perfil no alteren la receta emitida.

### D-20 — Límite de red y seguridad web

Usar Tailscale sujeto a verificar elegibilidad de la cuenta, límites de equipo/dispositivos y servidor elegido. No prometer gratuidad incondicional. Proponer que personal autorizado pueda conectarse por VPN desde fuera del hospital; esto resuelve explícitamente la parte de origen remoto de P-10. Todas las rutas de doctores y de recepción/cajero/administración usan el punto de entrada privado.

Exponer rutas de pacientes por una entrada pública y montar las protegidas solo en la privada. Vincular/proteger con cortafuegos el servicio privado a la ruta autorizada de la tailnet y configurar grants para personal y puerto previstos. Pertenecer a `100.64.0.0/10` no demuestra por sí solo una identidad autorizada en la tailnet. Documentar IPv4/IPv6 y cualquier proxy inverso; aceptar metadatos reenviados solo de infraestructura explícitamente confiable. Conservar sesiones, comprobación de roles y autorización por registro después del límite de red. Esta topología es una recomendación de diseño basada en [grants de Tailscale](https://tailscale.com/docs/features/access-control/grants), no un despliegue probado.

La excepción local solo se permite con configuración explícita de desarrollo, enlace a loopback y datos ficticios. El arranque de despliegue falla si está habilitada. Usar HTTPS, protección CSRF en cambios, escape de salida, consultas parametrizadas, limitación de intentos de acceso, cookies secure/HttpOnly/SameSite, regeneración de sesión al iniciar y revocación. Usar Argon2id con parámetros medidos y documentados en lugar de adoptar bcrypt por defecto para credenciales nuevas. [Almacenamiento de contraseñas de OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).

Guardar sesiones de servidor en SQL Server con limpieza por vencimiento; validar el adaptador antes de fijarlo. No usar MemoryStore predeterminado de Express fuera del desarrollo local. Establecer duración absoluta de ocho horas y 30 minutos de inactividad para personal; ocho horas absolutas/60 minutos de inactividad para pacientes. [Documentación de sesiones de Express](https://expressjs.com/en/resources/middleware/session/).

Las notificaciones de pagos en línea usan un endpoint dedicado de integración con verificación de autenticidad en servidor y protección contra repetición según el proveedor elegido; no deben pasar por permisos de caja ni exigir al proveedor unirse a la VPN del personal. No exponer rutas internas del personal para habilitar notificaciones.

Al perder VPN, falla la siguiente solicitud protegida. Una solicitud ya aceptada todavía puede confirmarse aunque se pierda la respuesta; una transacción no equipara desconexión con reversión. Reconectar y consultar/reintentar con el identificador de operación antes de repetir una acción monetaria.

### D-21 — Auditoría y correcciones clínicas

Conservar ambas bitácoras exigidas por la fuente, inserciones desde procedimientos, permisos que niegan actualización/eliminación y triggers de bloqueo como defensa adicional. Ningún rol de aplicación puede alterar, truncar, actualizar o eliminar sus entradas. No afirmar que estos controles limitan a un sysadmin de SQL Server que puede modificar los propios controles. Separar ese privilegio de infraestructura del rol administrador de la aplicación.

El proceso programado usa un actor de sistema identificable, no un paciente/doctor ficticio. Auditar cambios con estado anterior/nuevo, actor, motivo, fecha y campos históricos exigidos por la fuente. Distinguir derecho al reembolso y emisión real; emitir agrega un evento. Proteger contenido clínico mientras recepción ve únicamente metadatos permitidos y la referencia opaca de receta.

Alergias y padecimientos previos usan tablas hijas con estado vigente/inactivo, autor, fecha y motivo de corrección. No eliminar filas físicamente ni suponer que la bitácora de consultas registra ediciones clínicas hechas fuera del cierre. Mantener revisiones clínicas detalladas inaccesibles a recepción. Peso/talla pertenecen a consultas; distinguir desconocido, no medido y ausencia de alergias conocidas. Las recetas emitidas son inmutables; las correcciones referencian la receta sustituida y conservan su contenido original.

### D-22 — Convenciones y responsabilidad sobre artefactos

Conservar interfaz en español, Markdown principal en inglés con espejos en español, identificadores de base de datos en inglés con `snake_case` y fuentes Mermaid versionadas. Cambiar el prefijo de procedimientos de `sp_` a `usp_`; Microsoft reserva la primera convención para procedimientos del sistema. Conservar `fn_`, `vw_` y `trg_`. [Nombres de procedimientos de SQL Server](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-procedure-transact-sql?view=sql-server-ver17).

Conservar ramas `feat/<slug>` y revisión de un compañero para código. Proponer revisión también para cambios de decisiones, permisos, modelo e interpretaciones de fuente; documentación editorial menor puede ir directamente a `main`. Esta revisión no realiza commit ni push. Fijar versiones de herramientas de diagramas/exportación en lugar de descargar una última versión indeterminada en cada ejecución.

Para M1, las tablas del diccionario en `docs/07-data-model.md` son canónicas; generar Excel desde un formato estricto y documentado. Incluir destino PK/FK, tipo/longitud, precisión/escala, nulabilidad, valores predeterminados, unicidad/restricciones y descripción. Fallar ante tablas incorrectas o ausentes en lugar de exportar silenciosamente datos parciales. Cuando exista SQL, comprobar concordancia esquema/diccionario contra metadatos de SQL Server.

### D-23 — Datos de prueba y cobertura de rúbrica

Conservar al menos 10 especialidades, 40 doctores con cuatro por especialidad, 10 consultorios, 10 servicios, 20 medicamentos y 30 pacientes. “Diez registros cuando corresponda” no permite inventar diez estados o filas hijas arbitrarias; documentar excepciones como los siete estados fijos y las tablas de metadatos técnicos.

Usar datos ficticios deterministas con una fecha base relativa. Las citas futuras usan procedimientos de negocio. Los escenarios históricos pueden usar un cargador privilegiado solo en una base de desarrollo desechable; marcar procedencia y validar relaciones, estados, totales y auditorías. Poder insertar bitácoras no autoriza al flujo normal de ejecución a eludir reglas. Ejecutar la carga dos veces sin duplicar datos y nunca deshabilitar restricciones o triggers protectores como estrategia habitual.

## Cambios de documentación y modelo

Conservar el inventario propuesto de archivos, con estos ajustes:

| Artefacto | Requisito revisado |
| --- | --- |
| `docs/00-context.md` | Registrar decisiones aprobadas solo después de su aprobación. Resolver explícitamente cada parte de P-10. Conservar entradas P resueltas e historia PRN-a-RN en lugar de borrar el rastro de decisiones. |
| `docs/01-problem-statement.md` | Identificar hospital y problemas operativos como supuestos del caso ficticio, no hallazgos observados. Vincular objetivos con RF. |
| `docs/02-requirements.md` | Conservar RF/RNF. Precisar RF-04/RF-07/RF-11 antes de agregar RF-16/RF-17/RF-18 superpuestos; crear identificadores solo para requisitos realmente separados. Distinguir mediciones clínicas de la inasistencia registrada por recepción. |
| `docs/03-business-rules.md` | Matriz completa de acciones/datos/red; condiciones de transición además de flechas; límites de reembolso/vencimiento; conservar PRN-01–PRN-06 como alias sustituidos si se promueven a RN-23–RN-28. |
| `docs/04-view-design.md` | Incluir estados vacío/error/carga/conflicto/permiso. Retirar UI-K02/UI-K05 de navegación conservando identificadores históricos; UI-P07/UI-P08 cubren pago/seguimiento de reembolso de consultas en línea. Conservar aprobación de cancelaciones del doctor en recepción. |
| `docs/05-spec-driven-development.md` | Mantener aquí comandos compartidos y definición de terminado porque los archivos de agentes ignorados no llegarán a compañeros. Distinguir validación documental de pruebas de aceptación implementadas. |
| `docs/06-source-requirements.md` | Conservar extracción de fuentes. Cambiar solo la sección explícitamente marcada como decisiones posteriores del equipo, con estado de aprobación correcto. |
| `docs/07-data-model.md` | Partir de las 26 tablas propuestas, sin fijar cantidad. Separar finanzas de consultas y ventas de caja; modelar líneas de captura, eventos verificados del proveedor, solicitudes/outbox de reembolso y conciliación. Agregar vigencias de horarios, cuentas opcionales de pacientes, revisiones clínicas, deduplicación, sesiones y metadatos de migración cuando se necesiten; definir cardinalidades/eliminación. |
| `docs/08-architecture.md` | Servidor de base soportado, separación de rutas públicas/privadas, límites de confianza, sesiones, protocolo de bloqueos, reintentos, migraciones, privilegios mínimos, respaldo/restauración, cuatro vistas y cuatro funciones. Documentar público de cada vista y entradas/salidas de funciones; no ocultar un reloj no determinista en funciones de reglas. |
| `docs/09-roadmap.md` | Relacionar cada elemento de rúbricas S2/S3 y alcance S1 con entregable, responsable, dependencia y evidencia de verificación. Conservar clínica/farmacia/ventas como alcance obligatorio. |
| `docs/diagrams/context-dfd.md` | Nivel 0: un proceso del sistema y entidades externas, incluido servicio de pagos en línea (o simulador identificado). Nivel 1: procesos/almacenes separados para pagos de consultas y ventas de caja. Nivel 2: descomposición numerada de reservas/pagos en línea balanceada con su padre. Etiquetar flujos de datos. |
| `specs/001-schedule-appointment.md` | Reglas exactas de tiempo/alineación/consultorio/costo, vencimiento al reservar, autorización, reservas y ediciones concurrentes de horario, reintentos persistentes y contenido de confirmación. Conservar CA. |
| `specs/template.md` | Decisiones aplicadas, CA con alcance propio, límites de errores/permisos y estado de verificación. Ninguna especificación generada se marca “acordada” automáticamente. |
| `README.md` | Enlazar entregables y hoja de ruta; explicar correctamente archivos locales de agentes, preparación y trabajo completado frente a previsto. |

Para la rúbrica ER, entregar tanto el modelo lógico Mermaid (PK/FK/cardinalidad/opcionalidad) como un diagrama conceptual que represente explícitamente nombres compuestos y alergias/padecimientos multivaluados. Una tabla explicativa sola puede no satisfacer “indicar atributos” en el diagrama. Conservar leyenda y correspondencia con tablas hijas. Solicitar al profesor confirmación de numeración de niveles/notación sin retrasar los diagramas propuestos.

Explicar dependencias funcionales y 1FN/2FN/3FN por entidad pertinente; distinguir datos históricos congelados legítimos de duplicación sin control. Incluir grupo sanguíneo, diagnóstico, tratamiento, observaciones, instrucciones de medicamentos, detalles de recibos, unicidad de pagos/reembolsos y campos de auditoría de S1. Para recetas, decidir qué campos son texto clínico congelado y cuáles referencias opcionales al catálogo; editar un catálogo no debe alterar un documento emitido.

Conservar cuatro vistas y cuatro funciones, pero sustituir la vista propuesta de pagos de consultas en caja `vw_cashier_pending_payments` por `vw_appointment_payment_status`, disponible solo para flujos en línea autorizados; no concederla al cajero. Las vistas solas no hacen cumplir autorización por paciente. `fn_patient_age` recibe fecha de referencia; `fn_refund_percentage` recibe instantes explícitos; `fn_doctor_slots` recibe intervalo acotado y hora de referencia; `fn_sale_total` calcula desde partidas congeladas. Conservar edad histórica sin recalcular al imprimir.

## Configuración de agentes y automatización

Una vez estable el contenido M1, simplificar `AGENTS.md`, usar importación `@AGENTS.md` en `CLAUDE.md` y actualizar `SKILLS.md` mediante `claude-codex-sync`. Conservar `comment-xd` y el activador exacto `/commit-push`. Eliminar el comando instalador de las instrucciones; actualizar herramientas no pertenece al trabajo rutinario del proyecto. No cambiar silenciosamente la habilidad existente de commits mediante notas duplicadas de Claude.

Conservar `.claude/skills` canónico y `.agents/skills` enlazado. Codex documenta descubrimiento de habilidades del repositorio y soporte de enlaces simbólicos, pero leer un archivo no demuestra que la interfaz actual se haya actualizado. No prometer que sintaxis de comandos con barra o hooks de Claude funcionen igual en Codex; documentar el comando directo del script como alternativa portable. [Documentación oficial de habilidades de Codex](https://learn.chatgpt.com/docs/build-skills).

Para `trace-check`, limitar definiciones a documentos propietarios, resolver alias/intervalos y dar espacio de nombres a criterios, como `SPEC-001/CA-01`. Repetir CA-01 en otra especificación es válido. Ignorar marcadores de plantilla, distinguir referencias y definiciones, y registrar identificadores de planes borrador separados de decisiones aprobadas. Comprobar enlaces locales, espejos faltantes, niveles/cantidad de encabezados y conjuntos de identificadores. Son comprobaciones estructurales, no pruebas de traducción correcta, consistencia de permisos, balance de DFD o cobertura RF completa. Agregar una tabla manual: fuente → RF/RN → especificación/CA → artefacto/evidencia de prueba.

Para `new-spec`, asignar el siguiente número libre sin sobrescribir, validar nombres, mantener borrador y tratar referencias por palabras clave como sugerencias por revisar. Generar un espejo real en español antes de declarar éxito; un archivo provisional es trabajo incompleto. No hacer que los compañeros dependan de una habilidad local para crear especificaciones.

Para `sql-conventions`, incorporar D-11/D-13/D-14/D-21/D-22 revisadas, incluidos `usp_`, UTC, alineación fija, alcance del actor y concordancia esquema/diccionario. `db-apply.sh` y la configuración Docker son salidas de M3; no documentarlas como disponibles antes de existir.

Agregar los tres scripts propuestos: `trace_check.py`, `data_dictionary_xlsx.py` y `export-diagrams.sh`. Definir contrato del analizador Markdown y rutas explícitas de entrada/salida. Excel necesita índice, tablas con formato, filtros, encabezados congelados, anchos legibles y correspondencia determinista de nombres de hojas dentro de sus límites. Reabrir el libro generado y comparar cada campo/fila contra la fuente. Exportar todos los bloques Mermaid previstos con nombres únicos estables; inspeccionar legibilidad, recortes y etiquetas. Generar sin errores no basta como verificación visual.

Usar una sola lista de exclusión de espejos de archivos de agentes para habilidad, hook y verificador. Antes de borrar los tres espejos ignorados en español, revisar contenido exclusivo y preservar diferencias. Esta revisión no elimina archivos. La traducción paralela, si se usa al ejecutar, asigna un responsable por archivo y comienza solo cuando las fuentes inglesas estén estables.

## Hitos y orden de ejecución

| Hito | Objetivo | Entregable y condición de salida |
| --- | --- | --- |
| M1a | 16–17 de octubre | Revisar decisiones, estructura del modelo, borradores de problema/RF/RNF/RN y cobertura de rúbrica; registrar preguntas pendientes al profesor. |
| M1b | 18 de octubre | Completar DFD 0/1/2, ER conceptual/lógico, diccionario y libro generado; conciliar entidades, flujos y campos. |
| M1c | 19 de octubre | Espejos en español, revisión visual, comprobaciones estructurales, exportación reproducible y revisión del equipo; reservar tiempo para correcciones. |
| M1 | 20 de octubre | Paquete de primera entrega con todos los elementos S2 y exportaciones finales legibles; el responsable registra evidencia de entrega. |
| M2 | Hasta el 1 de noviembre, provisional | Mockups, casos de uso, secuencias y especificaciones de autenticación/red, reserva, pagos/vencimientos, cancelaciones/reembolsos; comprobación concreta del servidor de base. |
| M3 | Después de M2; fecha según P-14 | Esquema/migraciones, datos de prueba, restricciones/procedimientos, cuatro vistas/funciones, respaldo/restauración, integración y script SQL completo. |
| M4 | Antes de la segunda entrega | Login, límites de rol/red, inserción validada de cita, pago/vencimiento/cancelación; evidencia contra criterios de aceptación. |
| M5 | P-14, fecha del profesor desconocida | Ensayo y entrega S3: casos de uso, secuencias, modelo normalizado, scripts, conexión, datos, cuatro vistas/funciones e inserción validada. |
| M6 | Terminación obligatoria del proyecto; fecha por confirmar | Consultas/recetas, farmacia/servicios/ventas, administración y auditorías; integrar antes si lo exige la fecha final del profesor. |

Ejecutar por dependencias: revisión de decisiones → RF/RN y matriz → modelo/diccionario → DFD/ER → alineación narrativa/especificaciones de primera entrega → exportación Excel/diagramas → espejos/revisión. Ampliar arquitectura y automatizar agentes no debe retrasar M1. Asignar archivos antes del trabajo paralelo; mientras falten nombres, usar responsabilidades concretas sin fingir que “TBD” es una asignación.

## Pendientes y objetivos operativos propuestos

- **P-14 (nueva entrada propuesta):** fecha de segunda entrega del profesor y si todos los flujos S1 deben estar listos entonces. No inventar finales de noviembre como compromiso.
- **P-15 (propuesta):** nombres del equipo, responsables de archivos/módulos, revisor y responsable de entrega. La fuente limita el equipo a cuatro personas; una puede responsabilizarse de varias áreas.
- **P-16 (propuesta):** respaldo completo diario, retención de siete días, copia protegida separada, RPO ≤24 horas y RTO ≤2 horas para el entorno académico. Medir una restauración antes de marcar RNF-09 verificado. Se resuelve solo si se aprueba la propuesta.
- **P-17 (propuesta):** futuros portales opcionales de recetas del paciente y tutores; fuera de v1, sin bloquear M1.
- **Dependencias por validar:** proveedor de líneas de captura, integración real o simulada (P-01), tiempos/conciliación de eventos tardíos (P-05), ejecución de reembolsos en línea y responsabilidad de excepciones (P-07), servidor soportado y responsable, elegibilidad/límites de Tailscale y convenciones de diagramas del profesor. Son condiciones de preparación, no detalles de P-10 resueltos silenciosamente. No inventar ni renumerar P-13 para llenar un salto.

Para RNF-10, proponer p95 ≤2 segundos en el endpoint de reserva con 10,000 citas y 20 usuarios concurrentes, medido durante una carga documentada de cinco minutos en un entorno identificado; registrar tasas de errores/conflictos y excluir tiempo de terminal externa. Es un objetivo, no un resultado medido. Para RNF-07, especificar teclado, foco visible, etiquetas/asociación de errores, contraste e indicaciones de estado independientes del color; evaluar frente a WCAG 2.2 AA sin afirmar cumplimiento completo por una lista breve. [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/).

## Verificación e informe

En esta revisión, verificar únicamente consistencia con la extracción de fuentes del repositorio, decisiones/reglas existentes, identificadores actuales, organización local Git/habilidades y documentación técnica citada. Este plan no implementa ni prueba aplicación, VPN, SQL, scripts de exportación o habilidades nuevas.

Durante la ejecución, M1 comprueba cada elemento de rúbrica, balance de DFD, atributos/cardinalidad ER, concordancia diccionario/ER, contenido/diseño del libro, legibilidad de diagramas, trazabilidad, enlaces locales y equivalencia semántica en español. El éxito de `trace-check` es solo evidencia de apoyo.

Antes de marcar la implementación verificada, probar límites temporales exactos; finales de mes; solicitudes duplicadas/reintentadas; reserva frente a reserva/edición de horarios; pago frente a vencimiento/cancelación; notificaciones duplicadas, desordenadas, sin correspondencia y tardías del proveedor; reintento/falla/conciliación de reembolsos en línea; rechazo de operaciones de consultas al cajero; completar frente a inasistencia; consumo concurrente de existencias; reembolsos duplicados; acceso directo y a otros pacientes; entradas pública/privada incluidos proxy/IPv6; alteración de bitácoras con identidad de ejecución; caída/recuperación del proceso programado; confirmación seguida de respuesta perdida; y restauración de respaldo. Documentar honestamente excepciones de datos y fallas.

Informar artefactos cambiados, estado de aprobación, dependencias pendientes y comprobaciones realmente ejecutadas. No hacer commit/push sin `/commit-push` ni describir controles previstos como implementados.
