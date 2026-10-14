# Instrucciones comunes del proyecto

## Contexto

Etapa actual: documentación básica y exploración de vistas. Leer `README.md` y `docs/00-contexto.md` al iniciar una tarea; después, solo las especificaciones necesarias.

Acuerdos del equipo: cinco roles (paciente, doctor, recepcionista, cajero y administrador), aplicación totalmente web, VPN para recepcionista/cajero/administrador y cobros a cargo del cajero. Microsoft SQL Server es un requisito académico. Stack, proveedor de VPN y método de pago aún no están decididos.

## Trabajo guiado por especificaciones

- Los documentos distinguen requisito de la fuente, decisión confirmada, propuesta y pendiente. No convertir propuestas ni supuestos de diseño en decisiones del equipo.
- Consultar RF/RNF en `docs/02-requerimientos.md` y RN en `docs/03-reglas-negocio.md`. Mantener identificadores estables y vincular cambios con esos IDs.
- Para una funcionalidad nueva, usar `specs/plantilla.md` con alcance, actores, reglas, criterios de aceptación y preguntas relevantes. Una especificación puede ser corta.
- Si el usuario ya autorizó una decisión, incorporarla a `docs/00-contexto.md` y actualizar los documentos afectados. Si modifica una regla académica, registrar la diferencia y el punto a validar con la profesora.
- Cuando falte una decisión de negocio que cambie el resultado, exponer el pendiente y avanzar en trabajo independiente. No completar silenciosamente esa regla.
- Los bocetos usan datos ficticios. Documentar decisiones visuales, estados vacíos, errores y permisos por pantalla. El prototipo no demuestra que los permisos, la VPN o las reglas estén implementados.
- Antes de código de producción, concretar el comportamiento y los criterios de aceptación de la tarea. Verificar reglas y límites relevantes, no solo el caso feliz.
- Mantener los PDFs de `contexto/` como fuentes originales. Actualizar la documentación derivada sin alterar esos PDFs.
- No elegir herramientas, frameworks o infraestructura como parte de una tarea de bocetado, salvo que el usuario lo pida.
- Cuando varias tareas se hagan en paralelo, acordar un responsable por archivo y comunicar dependencias. No reemplazar cambios de otro colaborador.

## Permisos que deben conservarse

- Recepción no cobra ni procesa devoluciones monetarias; cajero realiza esas operaciones.
- Recepción no ve recetas ni historial médico.
- Doctor no se registra a sí mismo ni modifica sus datos sensibles; su cancelación requiere aprobación de recepción.
- Bitácoras: consulta e inserción; nadie actualiza ni borra entradas. Se propone que los eventos se inserten desde las operaciones del sistema.
- La VPN complementa la autenticación y autorización por rol; estas deben aplicarse en el servidor.

## Entregas

Comunicar brevemente qué cambió, qué sigue pendiente y qué se verificó. No declarar aprobado, probado, conectado o implementado lo que solo está documentado o bocetado.
