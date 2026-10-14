# Sistema hospitalario — documentación inicial

> Versión en español para el equipo. Las versiones en inglés permanecen fuera de esta carpeta. Los enlaces a los PDFs apuntan a `../contexto/`; las rutas de archivos en las instrucciones y los prompts se refieren a la raíz del proyecto. Esta copia se actualiza con la skill `spanish-sync` de `SKILLS.md`, automática en Claude Code.

Estado: borrador v0.1. Fecha: 2026-10-12.

Proyecto académico para gestionar citas, consultas, recetas, medicamentos, servicios y pagos con Microsoft SQL Server. Las cinco experiencias serán web: paciente, doctor, recepcionista, cajero y administrador. Recepcionista, cajero y administrador accederán por VPN.

## Empezar aquí

1. [Contexto, acuerdos y pendientes](docs/00-contexto.md).
2. [Problemática y objetivos](docs/01-problematica.md).
3. [Requerimientos funcionales y no funcionales](docs/02-requerimientos.md).
4. [Reglas de negocio](docs/03-reglas-negocio.md).
5. [Mapa de vistas y brief para Claude Design](docs/04-diseno-vistas.md).
6. [Guía práctica para desarrollar con especificaciones](docs/05-guia-sdd.md) y [primer ejemplo de funcionalidad](specs/001-agendar-cita.md).

Los PDFs originales se conservan en `contexto/`. Los documentos redactados aquí son una base para revisión del equipo, no una aprobación automática de las propuestas.

## Flujo de spec driven development

Trabajar por funcionalidades pequeñas. Para cada una: **necesidad → especificación → boceto → ajustes → plan técnico → implementación → verificación**. Los bocetos pueden empezar ahora y servir para descubrir requisitos. La documentación se actualiza cuando cambia una decisión.

| Etapa | Resultado | Situación |
| --- | --- | --- |
| Contexto y alcance | Acuerdos, responsables y dudas registradas | Base creada; falta revisar |
| Documentación básica | Problemática, RF, RNF y reglas de negocio | Borradores creados |
| Exploración de interfaz | Mapa general de cinco roles y bocetos | Brief preparado; bocetos pendientes |
| Primera entrega académica | Diagramas de contexto 0/1/2, entidad-relación y diccionario de datos, además de la documentación básica | Pendiente |
| Diseño funcional y de datos | Casos de uso, secuencias y modelo relacional normalizado | Pendiente |
| Diseño técnico | Arquitectura, autenticación, VPN, contratos y scripts SQL | Pendiente; stack sin elegir |
| Implementación por flujo | Primero login y agendamiento con validaciones | Pendiente |
| Segunda entrega académica | Scripts, conexión, datos de prueba, cuatro vistas, cuatro funciones y agendamiento desde aplicación | Pendiente |

Las entregas académicas se obtuvieron de las rúbricas originales; no basta con preparar los bocetos para cubrirlas.

## Contexto para agentes

- `AGENTS.md`: instrucciones comunes del proyecto y entrada para Codex.
- `CLAUDE.md`: importa las mismas instrucciones para Claude Code.
- `docs/`: contexto funcional compartido; leer solo los documentos relevantes para la tarea.
- `specs/plantilla.md`: formato ligero para especificar una funcionalidad cuando se empiece a trabajar en ella.
- `specs/001-agendar-cita.md`: ejemplo en borrador para aprender el ciclo antes de implementar.

Un encargo a un agente debe incluir: objetivo, RF/RN implicados, archivos a modificar, alcance, pendientes relevantes y cómo verificar el resultado. Ambos agentes pueden implementar o revisar; el equipo asigna responsabilidades por tarea.

## Primer paso en Claude Design

Adjuntar el PDF original `contexto/ESPECIFICACIONES PROYECTO FINAL BASES DE DATOS 26-2.pdf` junto con `docs/00-contexto.md`, `docs/02-requerimientos.md`, `docs/03-reglas-negocio.md` y `docs/04-diseno-vistas.md`. Copiar el prompt del último documento. El PDF conserva las exigencias académicas; los Markdown distinguen las decisiones posteriores del equipo y las propuestas. Si aparece una discrepancia, registrarla para revisión. El encargo inicial es **mapa general de los cinco roles**, no el desarrollo del sistema.

Después, incorporar al proyecto la exportación del diseño, las decisiones tomadas y sus pendientes. Vincular los nombres de pantallas con sus identificadores `UI-*` antes de encargar su implementación.

## 20 de octubre

- Problemática
- Requisitos funcionales
- Requisitos no funcionales
- Diagrama de contexto
- Modelo entidad-relación
- Diccionario de datos

## Referencias

- [Especificaciones académicas](../contexto/ESPECIFICACIONES%20PROYECTO%20FINAL%20BASES%20DE%20DATOS%2026-2.pdf).
- [Primera rúbrica](../contexto/Ru%CC%81brica_Eval_Proyecto_1P.pdf).
- [Segunda rúbrica](../contexto/Ru%CC%81brica_Eval_Proyecto_2P.pdf).
- [Instrucciones de Codex con AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
- [Contexto de Claude Code e importaciones](https://code.claude.com/docs/en/memory).
- [Prototipos y entrega de Claude Design](https://academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux).
