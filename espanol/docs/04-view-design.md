# Mapa general y brief para Claude Design

Estado: borrador v0.1, 2026-10-12. Objetivo confirmado D-06: explorar el mapa general de los cinco roles. Bocetos pendientes; este documento es el encargo de diseño.

## Qué entregar primero

1. Mapa de navegación de los cinco perfiles y puntos donde se relacionan sus tareas.
2. Bocetos de baja fidelidad de login y una pantalla principal por rol: seis vistas iniciales.
3. Prototipo navegable mínimo entre las vistas iniciales, con datos ficticios.
4. Inventario de pantallas secundarias y lista de decisiones/preguntas detectadas.

El selector de rol, si se usa para presentar el prototipo, debe indicar **modo demostración**. En producción el acceso depende de la cuenta autenticada; el selector no concede permisos.

Después de revisar el mapa, detallar un flujo por vez. No diseñar todas las pantallas con acabado final en la primera iteración.

## Acuerdos que el boceto debe conservar

- Todo es web. Paciente: móvil y computadora. Doctor: computadora/tableta. Recepción, caja y administración: web enfocada en computadora.
- Recepcionista, cajero y administrador requieren VPN. Puede existir una vista de acceso denegado con indicación de conectarse a VPN; el prototipo solo representa el comportamiento.
- Recepción gestiona agenda y cancelaciones; caja cobra y, como propuesta, ejecuta devoluciones. Cancelar no significa que el reembolso ya fue entregado.
- Recepción no tiene recetas, historial médico ni acciones de cobro.
- Doctor no se registra solo ni edita nombre, CURP, cédula, número de empleado o especialidad. Solicita cancelación para aprobación de recepción.
- No hay botón Reagendar. Cancelar y solicitar una nueva cita son operaciones distintas.
- Agendamiento: especialidad/costo → doctor → fecha → horario → revisión → comprobante con línea de pago y plazo de 8 horas.
- Fechas desde 48 horas hasta tres meses; horarios disponibles dentro de jornada; sin otra cita pendiente con el mismo doctor.
- El pago real, permisos detallados de administrador y reglas de inventario siguen pendientes. No convertir un control visual en una decisión de negocio.

## Navegación propuesta

| Perfil | Menú principal | Vista de entrada |
| --- | --- | --- |
| Paciente | Inicio, Agendar, Mis citas, Mis datos | Próxima cita y plazo de pago, si aplica |
| Doctor | Agenda, Consultas, Recetas, Solicitudes, Mi perfil | Agenda del día |
| Recepcionista | Inicio, Agenda, Pacientes, Personal, Cancelaciones | Citas y solicitudes pendientes |
| Cajero | Inicio, Pagos de citas, Ventas, Tickets, Devoluciones, Existencias | Cobros pendientes |
| Administrador | Inicio, Usuarios, Catálogos, Farmacia, Servicios, Bitácoras | Resumen administrativo propuesto |

La ubicación de funciones en menús es propuesta. Los permisos de altas administrativas compartidas deben resolverse en P-02.

## Inventario de vistas y trazabilidad

Los IDs se conservan aunque cambien los nombres. Una vista puede implementarse como página, pestaña o diálogo; esa decisión se valida con el boceto.

| ID | Vista | Contenido y acción principal | Referencias |
| --- | --- | --- | --- |
| UI-C01 | Login | Credenciales, entrada por cuenta, enlace de registro de paciente | RF-01 |
| UI-C02 | Registro de paciente | Datos personales y acceso; campos pendientes | RF-02; P-09 |
| UI-C03 | Acceso interno no disponible | Explicar restricción de VPN y permitir reintentar; representar también sesión vencida | RNF-03; P-10 |
| UI-P01 | Inicio paciente | Próxima cita, estado, plazo de pago y acceso a agendar | RF-06/08 |
| UI-P02 | Mis datos | Consulta de ficha personal; edición solo si se acuerda | RF-02; P-09 |
| UI-P03 | Agendar cita | Pasos de especialidad, doctor, fecha, horario y revisión | RF-05; RN-01/02/03/04 |
| UI-P04 | Comprobante | Folio, datos de cita, línea, plazo e instrucciones del método aún pendiente | RF-06; P-01 |
| UI-P05 | Mis citas y detalle | Filtros de fecha/estado, comprobante, cancelación e historial | RF-08/09 |
| UI-P06 | Confirmar cancelación | Política aplicable y devolución estimada antes de aceptar | RF-09/10; RN-07 |
| UI-D01 | Agenda doctor | Día/semana, pacientes, horarios y consultorios | RF-08 |
| UI-D02 | Consulta | Datos de cita/paciente, accesos clínicos y resultado de atención | RF-11; P-06 |
| UI-D03 | Historial médico | Alergias, sangre, antecedentes, peso, estatura y consultas | RF-11; P-04/P-12 |
| UI-D04 | Recetas | Listado, emisión y vista imprimible | RF-12 |
| UI-D05 | Mi perfil | Datos sensibles de consulta y jornada | RN-12/13 |
| UI-D06 | Solicitudes de cancelación | Solicitar y seguir respuesta de recepción | RF-09; RN-08 |
| UI-R01 | Inicio recepción | Agenda de hoy y solicitudes de cancelación | RF-08/09 |
| UI-R02 | Agenda general | Filtros por doctor, especialidad, consultorio y fecha; alta y detalle de cita | RF-05/08/09 |
| UI-R03 | Pacientes | Búsqueda, registro, ficha administrativa y citas | RF-02/08; RN-14 |
| UI-R04 | Personal | Altas/consulta de doctores y recepcionistas; jornadas según permisos acordados | RF-03/04; RN-11/15; P-02 |
| UI-R05 | Cancelaciones | Solicitudes del doctor, aprobación y cancelación por paciente | RF-09; RN-07/08 |
| UI-K01 | Inicio cajero | Cobros pendientes y resumen propuesto del día | RF-07/14 |
| UI-K02 | Pagos de citas | Buscar folio y registrar confirmación según método acordado | RF-07; P-01 |
| UI-K03 | Venta | Medicamentos/servicios, cantidades, total y cobro; cliente sin cuenta | RF-14; RN-16/22 |
| UI-K04 | Tickets | Consultar y volver a obtener comprobantes | RF-14; reimpresión propuesta |
| UI-K05 | Devoluciones | Importe que corresponde devolver y ejecución separada | RF-10; P-07 |
| UI-K06 | Existencias | Consulta de medicamentos disponibles, sin contenido clínico | RF-13; permisos propuestos P-02 |
| UI-A01 | Inicio administrador | Resumen administrativo; métricas a validar | Propuesta; RF-08/13/15 |
| UI-A02 | Usuarios y empleados | Cuentas, perfiles y accesos; permisos por resolver | RF-03; P-02 |
| UI-A03 | Catálogos | Especialidades/costos, consultorios y jornadas según P-02 | RF-04 |
| UI-A04 | Farmacia | Medicamentos, precios, inventario y entradas propuestas | RF-13; P-02/P-08 |
| UI-A05 | Servicios | Catálogo y precios de servicios extras | RF-14; RN-18; P-02 |
| UI-A06 | Bitácoras | Filtros y consulta de movimientos; sin editar/borrar ni abrir contenido clínico por defecto | RF-15; RN-17; P-12 |

No dar al administrador todos los accesos por defecto: su matriz detallada se debe acordar. En este inventario sus funciones ampliadas son propuestas.

## Relaciones entre perfiles

- **Cita:** paciente o recepción agenda → comprobante/plazo → caja confirma pago → doctor consulta agenda y atiende.
- **Vencimiento:** cita sin confirmación dentro del plazo → cancelación por falta de pago → disponibilidad liberada. El proceso automático real se diseña después.
- **Cancelación por doctor:** doctor solicita → recepción resuelve → si se aprueba, cita cancelada y devolución del 100% que caja procesa según el mecanismo pendiente.
- **Cancelación por paciente:** paciente o recepción cancela → cálculo conforme a política → caja procesa devolución, cuando corresponda.
- **Venta:** cajero selecciona medicamento/servicio → registra cobro y ticket → inventario se actualiza según reglas por validar.
- **Administración:** mantiene los catálogos y cuentas que consumen los demás perfiles, según permisos aún por acordar.

La fecha límite de pago se muestra como información de la cita; no inventar que el paciente tenga que presentarse físicamente en caja o que haya pasarela bancaria mientras P-01 esté pendiente.

## Estados a explorar

| Área | Estados y variantes |
| --- | --- |
| Común | Cargando, vacío, error, sesión vencida, acceso denegado por rol/VPN |
| Agenda | Con citas, sin citas, sin horarios, horario tomado durante confirmación, fecha inválida |
| Paciente | Sin próxima cita, pendiente de pago, pagada, vencida, cancelada, atendida, no acudió |
| Cancelación | Devolución de 100/50/0%; solicitud del doctor pendiente/aprobada/rechazada, como propuesta |
| Caja | Folio no encontrado, pago ya confirmado, venta sin artículos, existencias insuficientes, devolución pendiente/ejecutada como propuesta |
| Doctor | Paciente sin antecedentes, alergia registrada, receta nueva y receta existente |

Los estados de error que se presentan son escenarios de diseño; deben vincularse con criterios de aceptación antes de implementar. No crear nuevos estados de cita sin actualizar su especificación.

## Dirección visual provisional

Interfaz en español, legible y sobria; contenido operativo primero. Componentes consistentes entre perfiles: buscadores, formularios, tablas, tarjetas de citas, etiquetas de estado y confirmaciones. Las etiquetas llevan texto, no solo color.

La marca, paleta y tipografía se elegirán después. Usar nombre provisional y datos ficticios. No agregar fotografías o decoración que compitan con agendas y formularios. Moneda, fechas y campos de ejemplo son de demostración hasta que se acuerden sus formatos.

## Prompt inicial para copiar en Claude Design

```text
Estamos diseñando un proyecto académico de sistema hospitalario en etapa temprana. Queremos explorar navegación y distribución de contenido antes de desarrollar el sistema.

Lee el PDF original «ESPECIFICACIONES PROYECTO FINAL BASES DE DATOS 26-2.pdf» y los cuatro documentos derivados adjuntos: 00-context.md, 02-requirements.md, 03-business-rules.md y 04-view-design.md. Usa el PDF para comprobar las exigencias académicas; los Markdown registran también las decisiones posteriores del equipo. Distingue decisiones confirmadas de propuestas y preguntas pendientes. Si detectas una discrepancia, señálala para revisión. Conserva los IDs UI/RF/RN para poder relacionar diseño y especificaciones.

Toda la aplicación es web y tiene cinco roles: paciente, doctor, recepcionista, cajero y administrador. Recepción, caja y administración trabajan con VPN. El paciente necesita adaptación móvil; los otros perfiles necesitan una distribución cómoda en computadora, y doctor también en tableta.

Primero crea el mapa general de navegación de los cinco roles y bocetos de baja fidelidad de seis vistas: login (UI-C01), inicio paciente (UI-P01), agenda doctor (UI-D01), inicio recepción (UI-R01), inicio cajero (UI-K01) e inicio administrador (UI-A01). Incluye menús para sus vistas secundarias, identificando cuáles están pendientes de diseñar. Haz navegable esta presentación mínima con datos ficticios. Si usas un selector de perfil para recorrer el prototipo, identifícalo como modo demostración.

Reglas críticas: recepción no cobra ni ve recetas o historial médico; caja cobra; la cancelación del doctor requiere aprobación de recepción. No hay reagendamiento. Las citas se solicitan entre 48 horas y tres meses de anticipación, con doctor y horario disponibles dentro de su jornada; no puede haber otra cita pendiente del paciente con ese mismo doctor. El comprobante incluye línea de pago y plazo de 8 horas. El método real de pago está pendiente. Cancelación de paciente: propuesta de intervalos 100% a partir de 48 horas, 50% de 24 a menos de 48 y 0% antes de 24; cancelación por doctor devuelve 100%. La ejecución del reembolso es distinta de cancelar. Las bitácoras no se editan ni borran.

Los permisos detallados del administrador y algunas reglas siguen pendientes. No le otorgues acceso clínico o permisos universales por defecto. Señala toda propuesta nueva en una lista aparte, sin presentarla como requisito confirmado.

Incluye variantes de vista vacía y con datos, y representación de error/acceso interno sin VPN. No hace falta detallar todas las pantallas ahora. Propón una distribución visual coherente en español y registra las decisiones. El resultado es un boceto con simulaciones; no conectes base de datos, VPN o pagos reales.

Entrega: mapa por rol, seis vistas iniciales, recorrido navegable mínimo, inventario de secundarias con sus IDs y lista breve de dudas. No elijas el stack de producción. Cuando una duda no impida el mapa general, déjala registrada y continúa.
```

## Cómo revisar y devolver el diseño al proyecto

- Comprobar que aparecen los cinco perfiles y las seis vistas iniciales solicitadas.
- Comprobar separación de recepción/caja y acceso clínico del doctor.
- Revisar si la navegación permite comprender quién agenda, confirma, atiende y cancela.
- Verificar estados vacíos/errores y que el prototipo no presente propuestas como funciones aprobadas.
- Guardar exportación y decisiones junto a una spec del flujo que se vaya a implementar. Usar IDs UI-* para nombrar vistas y enlazarlas con RF/RN.
- Incorporar cambios de negocio en los documentos compartidos antes de pedir a Codex o Claude Code que implemente ese comportamiento.

Referencia sobre flujos, prototipos y entrega de diseños: [guía oficial de Claude Design](https://academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux).
