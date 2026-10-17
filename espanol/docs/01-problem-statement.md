# Problemática y objetivos

Estado: borrador para revisar con el equipo. Fuente del alcance: S1; estructura de entrega: S2, definidas en `00-context.md`.

## Problemática

La operación de un hospital requiere coordinar pacientes, disponibilidad de doctores, consultorios, citas, pagos y atención médica. Cuando esa información se administra en registros separados, pueden aparecer conflictos de horario, inconsistencias entre el estado de una cita y su pago, y dificultades para consultar el historial de movimientos.

La gestión también necesita aplicar consistentemente políticas de anticipación, prepago de consultas en línea mediante línea de captura, cancelación en línea y reembolso en línea (D-04). El cajero cobra únicamente medicamentos y servicios adicionales; esas ventas y existencias se separan de los pagos de consultas. Los datos clínicos deben consultarse según las responsabilidades de cada usuario.

El proyecto propone un sistema web centralizado para apoyar estas operaciones, con cinco roles y una base Microsoft SQL Server. Separa las tareas de recepción y caja, conserva trazabilidad y restringe las operaciones de recepción, administración y caja, y las funciones de consultorio del doctor, a la red privada del hospital mediante VPN.

**Nota de evidencia:** los riesgos anteriores describen el problema que el proyecto busca resolver. No se ha estudiado un hospital real ni se ha demostrado que use registros separados o presente esos problemas. Si el equipo tiene una institución de referencia, sustituir esta formulación general por evidencia de esa operación.

## Objetivo general

Desarrollar un sistema web que gestione citas y operaciones asociadas de un hospital, aplicando reglas de negocio, permisos por rol y registro de movimientos sobre Microsoft SQL Server.

## Objetivos específicos

- Facilitar el registro de pacientes y la solicitud de citas con disponibilidad válida.
- Mantener sincronizados estados de cita, pagos, cancelaciones y devoluciones.
- Apoyar al doctor en la consulta de antecedentes y emisión de recetas.
- Facilitar ventas de medicamentos y servicios con tickets y control de existencias.
- Separar responsabilidades de paciente, doctor, recepción, caja y administración.
- Registrar movimientos de citas y consultas en bitácoras que no puedan editarse ni borrarse.

## Evidencia de éxito propuesta

Los criterios detallados se encuentran en `02-requirements.md`. La demostración debe permitir agendar una cita válida, rechazar una que incumpla las reglas, confirmar un pago, cancelar aplicando su política, realizar una atención con receta y generar un ticket por una venta.

También se verificará que recepción no pueda cobrar ni consultar contenido clínico, y que las operaciones de recepción, administración y caja, y las funciones de consultorio del doctor, rechacen el acceso sin la VPN a la red del hospital. La autenticación y los permisos del rol deben seguir aplicándose dentro de la VPN. Son criterios del proyecto, no resultados ya obtenidos.
