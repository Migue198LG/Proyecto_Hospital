# Guía práctica: desarrollar este proyecto con especificaciones

Estado: guía de trabajo inicial, 2026-10-12. Leer después de `README.md` y `docs/00-context.md`.

## Idea central

Describir **qué debe ocurrir y cómo comprobarlo** antes de decidir **cómo programarlo**. Cada cambio funcional debe poder rastrearse desde su fuente hasta un comportamiento verificado. La especificación sigue viva: cuando el equipo aprende algo al bocetar o implementar, actualiza el documento correspondiente y luego ajusta diseño, código y pruebas.

El proceso se parece al flujo *Specify → Plan → Tasks → Implement → Converge* de [GitHub Spec Kit](https://github.com/github/spec-kit/blob/main/docs/index.md). Aquí se usa una versión ligera en Markdown; no depende de instalar Spec Kit ni de elegir un framework ahora.

## Dos niveles de especificación

1. **Nivel de proyecto:** `docs/00-context.md` registra decisiones y pendientes; `01-problem-statement.md` explica el problema; `02-requirements.md` reúne RF/RNF; `03-business-rules.md` contiene RN; `04-view-design.md` identifica las pantallas. El PDF de `contexto/` es la fuente académica original.
2. **Nivel de funcionalidad:** un archivo en `specs/` concreta un recorrido que una persona puede completar o una operación del sistema. Ejemplo: `specs/001-schedule-appointment.md`. Se crea desde `specs/template.md`, con referencias a los IDs globales, criterios de aceptación, casos límite y preguntas abiertas.

El documento de proyecto se modifica cuando cambia una regla o decisión compartida. La spec de una funcionalidad se modifica cuando cambia el comportamiento de esa funcionalidad. Un boceto no reemplaza ninguno de los dos.

## Ciclo para cada funcionalidad

| Paso | Pregunta que debe responder | Evidencia que queda |
| --- | --- | --- |
| 1. Delimitar | ¿Quién necesita hacer qué y qué queda fuera? | Necesidad, actores y alcance en la spec |
| 2. Especificar | ¿Qué reglas, entradas, salidas, estados y permisos aplican? | Referencias RF/RN y flujo observable |
| 3. Aclarar | ¿Qué decisión falta para que dos personas implementen lo mismo? | P-* resuelto en `00-context.md` o señalado como bloqueo de esa parte |
| 4. Bocetar | ¿Cómo verá y completará el recorrido cada rol? | Prototipo con IDs UI-*, estados y errores |
| 5. Planear | ¿Qué datos, contratos, transacciones y componentes hacen falta? | Plan técnico de esa funcionalidad; stack solo cuando se acuerde |
| 6. Dividir | ¿Qué tareas pequeñas pueden construirse y comprobarse? | Lista de tareas con responsable y dependencias |
| 7. Implementar | ¿La aplicación cumple cada criterio, incluido un rechazo? | Código, esquema y pruebas necesarias |
| 8. Converger | ¿Coinciden PDF, decisiones, spec, boceto, código y pruebas? | Revisión de trazabilidad y pendientes cerrados |

Un prototipo se puede elaborar antes de cerrar todos los pendientes: sirve para descubrir preguntas. Solo los comportamientos que se implementarán necesitan definiciones precisas. Evitar que una opción visual se convierta por accidente en regla de negocio.

## Ejemplo de trazabilidad

```text
PDF de especificaciones, p. 1: al menos 48 horas de anticipación
  → RN-01: límite para solicitar cita
  → RF-05: agendamiento con disponibilidad válida
  → UI-P03: selección de fecha y horario
  → SPEC-001 / CA-02: fecha anterior al mínimo se rechaza
  → prueba: el servidor rechaza la solicitud y no crea la cita
```

La pantalla ayuda a evitar un error; la regla debe cumplirse también cuando la solicitud llega directamente al servidor. Cuando se agregue un cambio, revisar las referencias conectadas antes de declarar terminada la tarea.

## Ejercicio con el proyecto actual

1. Leer [la especificación de ejemplo de agendamiento](../specs/001-schedule-appointment.md). Separar lo confirmado de P-03/P-04/P-05/P-11.
2. Comparar sus criterios con el boceto UI-P03/UI-P04 de Claude Design. Anotar campos o estados que falten.
3. Resolver con el equipo las preguntas que afecten la cita antes del plan técnico: duración, qué significa cita pendiente, bordes de tiempo y asignación de consultorio.
4. Elaborar la primera spec implementable del flujo acordado. Después decidir arquitectura y esquema para ese flujo, no para todo el hospital de una vez.
5. Pedir a Codex o Claude Code un plan de tareas que cite los criterios CA-* y comprobar las tareas antes de implementar.

**Prompt de revisión para un agente, antes de programar:**

```text
Lee el PDF de contexto, docs/00-context.md, docs/02-requirements.md,
docs/03-business-rules.md y specs/001-schedule-appointment.md.
Revisa la spec contra la fuente: identifica contradicciones, reglas sin criterio
de aceptación, criterios sin fuente y decisiones P-* todavía necesarias.
Propón correcciones concretas al documento. No elijas stack ni escribas código.
```

**Prompt de planificación, después de resolver los pendientes que afectan al flujo:**

```text
Lee la spec acordada y el diseño UI-P03/UI-P04 aprobado por el equipo.
Propón un plan y tareas pequeñas para implementar cada CA-* con SQL Server.
Indica modelo de datos, operaciones del servidor, validaciones,
autorización, concurrencia y pruebas pertinentes. Usa únicamente el stack
registrado como decisión del proyecto; señala cualquier hueco.
```

## Cómo dividir el trabajo sin perder contexto

Claude Design explora la interfaz y registra decisiones visuales. Codex y Claude Code pueden revisar una spec, planear, implementar o comprobar; cada tarea debe nombrar los mismos archivos y criterios. Cuando dos personas o agentes trabajen a la vez, asignar responsables por archivo o módulo y acordar el contrato entre sus tareas antes de hacer cambios dependientes.

Al terminar una tarea, el resultado debe decir qué RF/RN/CA cubre, qué se verificó y qué sigue pendiente. El equipo incorpora cualquier decisión nueva a `docs/00-context.md`, después actualiza la spec, el boceto y el código afectado. Mantener estos documentos bajo control de versiones permitirá revisar quién cambió una regla y por qué.

## Orden recomendado ahora

1. Revisar en equipo los borradores de problemática, RF/RNF y RN. Identificar qué proviene del PDF y qué es propuesta.
2. Obtener en Claude Design el mapa general de cinco roles y seis vistas iniciales, usando `docs/04-view-design.md`.
3. Preparar los diagramas de contexto, entidad-relación y diccionario de datos de la primera rúbrica; resolver preguntas de negocio que afecten esos modelos.
4. Refinar `SPEC-001` y elegir el stack cuando se vaya a planear su implementación.
5. Implementar y verificar primero un recorrido pequeño: registro/login, agendamiento, comprobante y confirmación de pago según el método que acuerden.
6. Continuar con cancelaciones, consulta/receta, venta/inventario, administración y bitácoras, cada una con su propia spec y criterios.

Los pasos 2 y 3 pueden avanzar a la vez, con revisión cruzada: el boceto puede revelar datos que falten en el modelo, y el modelo puede revelar preguntas de interfaz. La segunda rúbrica exige agendar una cita desde aplicación o web con validaciones; por eso este recorrido merece atención temprana.

## Scripts y verificaciones compartidos

Los archivos de configuración de agentes (`AGENTS.md`, `CLAUDE.md`, `SKILLS.md`, `.claude/`, `.agents/`) son locales y no se versionan, así que los procedimientos que el equipo necesita viven aquí y en `scripts/`. Los scripts solo requieren Python 3 y Bash; se ejecutan desde la raíz del repositorio.

| Comando | Propósito | Lo que no demuestra |
| --- | --- | --- |
| `python3 scripts/trace_check.py` | Verifica que cada identificador RF/RNF/RN/PRN/UI/D/P/SPEC/CA citado esté definido en su documento propietario, que los enlaces locales resuelvan, que cada `.md` en inglés tenga su espejo en `espanol/` con la misma estructura de encabezados e identificadores, y lista como propuestas los identificadores que solo existen en `plans/` | Traducción correcta, consistencia de permisos, balanceo de diagramas ni cobertura completa de requerimientos; eso requiere revisión manual |
| `scripts/new_spec.sh <slug> ["Name"] ["Nombre"]` | Crea `specs/NNN-<slug>.md` y `espanol/specs/NNN-<slug>.md` a partir de ambas plantillas con el siguiente número libre y estado borrador | Que las referencias sean correctas; tomarlas de los documentos propietarios y revisarlas |

Definición de terminado para una tarea de documentación: el documento propietario define cualquier identificador nuevo, los documentos afectados lo citan, el espejo en español está actualizado, `trace_check.py` no reporta errores y la entrega indica lo que queda pendiente. Para tareas de implementación, agregar los criterios de aceptación ejecutados y su evidencia; pasar la verificación estructural no es una prueba funcional.

Las rutas sin espejo en español están listadas en `scripts/mirror-exclusions.txt`, la única lista que usan la verificación y el hook de Claude Code.
