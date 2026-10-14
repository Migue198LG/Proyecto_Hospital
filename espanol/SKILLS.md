# Skills del proyecto

Procedimientos reutilizables para los agentes (Claude Code y Codex). Cada skill indica cuándo aplica, los pasos y las reglas que deben cumplirse.

## spanish-sync — mantener `espanol/` sincronizada con los documentos en inglés

**Cuándo:** cada vez que se crea, edita, renombra o elimina un archivo `.md` fuera de `espanol/`. Se excluyen `.claude/` y todo lo que está dentro de `espanol/`. Los PDFs de `contexto/` nunca se modifican.

En Claude Code se ejecuta automáticamente: el hook `PostToolUse` de `.claude/settings.json` (`.claude/hooks/md-changed.sh`) detecta el cambio y pide al agente aplicar esta skill. También puede ejecutarse manualmente con `/spanish-sync <ruta>`. Las ediciones de Codex o de personas no activan el hook; en ese caso, aplicar la skill manualmente.

### Pasos

1. Identificar la fuente en inglés `<ruta>.md` y su espejo `espanol/<ruta>.md` (misma ruta relativa y mismo nombre de archivo; los nombres de archivo no se traducen).
2. Leer la fuente y, si existe, el espejo actual.
3. Comprobar que el espejo no se haya editado directamente. Si contiene contenido sin equivalente en la versión en inglés, no sobrescribirlo: informar la diferencia y preguntar qué versión prevalece.
4. Traducir solo lo que cambió cuando el cambio es local; retraducir el archivo completo cuando cambió la estructura. Conservar el resto del espejo tal como está para que la redacción no varíe entre sincronizaciones.
5. Escribir `espanol/<ruta>.md`. Si la fuente se eliminó o se renombró, eliminar o renombrar el espejo de la misma forma.
6. Informar en la entrega qué espejo se actualizó.

### Reglas de traducción

- Español formal de México, coherente con los archivos existentes en `espanol/`.
- Mantener sin cambios: identificadores (`RF-*`, `RNF-*`, `RN-*`, `UI-*`, `S1`–`S3`, `EQUIPO`), nombres de archivo, rutas, código, SQL, comandos y URLs.
- Etiquetas de estatus: Confirmed → Confirmado, Source → Fuente, Proposed → Propuesto, Open → Pendiente. Roles: patient → paciente, doctor → doctor, receptionist → recepcionista, cashier → cajero, administrator → administrador.
- Misma estructura: encabezados, listas, tablas y enlaces en el mismo orden. Los enlaces relativos entre documentos se mantienen iguales porque la carpeta replica la estructura; los enlaces a los PDFs apuntan a `../contexto/`.
- `espanol/README.md` conserva su nota introductoria sobre la versión en español.
- No agregar, quitar ni suavizar requisitos, decisiones o permisos al traducir. Si el texto en inglés es ambiguo, traducirlo literalmente y señalar la ambigüedad.

### Verificación

- Los encabezados e IDs del espejo coinciden con los de la fuente.
- No falta ningún espejo: cada `.md` fuera de `espanol/` y `.claude/` tiene su contraparte.

## comment-xd — terminar cada comentario de código con "xd"

**Cuándo:** cada vez que un agente escribe o edita un comentario en código (SQL, scripts, código de la aplicación, configuración). No aplica a documentos Markdown, cadenas de texto ni código de terceros o generado.

### Reglas

- Todo comentario termina con ` xd` (un espacio y luego `xd` en minúsculas), después de la puntuación final.
- Comentarios de línea (`--`, `//`, `#`): `xd` va al final de la línea.
- Comentarios de bloque (`/* */`) y docstrings: `xd` va al final de la última línea de texto, antes del delimitador de cierre.
- No agregar `xd` a cadenas, mensajes de error ni datos; solo a comentarios.
- Los comentarios existentes se actualizan solo cuando el agente los edita por otro motivo.

### Ejemplo

```sql
/* Crea la tabla de citas para el flujo de agendamiento.
   Datos ficticios; las reglas RN-* aún no se aplican. xd */
CREATE TABLE Cita (
    IdCita     INT IDENTITY PRIMARY KEY,
    IdPaciente INT NOT NULL,  -- Paciente que agendó la cita. xd
    IdDoctor   INT NOT NULL,  -- Doctor asignado. xd
    FechaHora  DATETIME2 NOT NULL,
    Estado     VARCHAR(20) NOT NULL DEFAULT 'Agendada'  -- El valor de texto queda sin xd. xd
);
```
