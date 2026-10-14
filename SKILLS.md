# Project skills

Reusable procedures for agents (Claude Code and Codex). Each skill states when it applies, the steps, and the rules that must hold.

## spanish-sync — keep `espanol/` in sync with the English documents

**When:** every time a `.md` file outside `espanol/` is created, edited, renamed, or deleted. Excluded: `.claude/` and anything inside `espanol/`. The PDFs in `contexto/` are never touched.

In Claude Code this runs automatically: the `PostToolUse` hook in `.claude/settings.json` (`.claude/hooks/md-changed.sh`) detects the change and asks the agent to apply this skill. It can also be run manually with `/spanish-sync <path>`. Codex and human edits do not trigger the hook; in that case apply the skill by hand.

### Steps

1. Identify the English source `<path>.md` and its mirror `espanol/<path>.md` (same relative path and same file name; file names are not translated).
2. Read the source and, if it exists, the current mirror.
3. Check that the mirror was not edited directly. If it contains content with no equivalent in the English version, do not overwrite it: report the difference and ask which version prevails.
4. Translate only what changed when the change is local; retranslate the whole file when the structure changed. Keep the rest of the mirror as it is so wording does not drift between syncs.
5. Write `espanol/<path>.md`. If the source was deleted or renamed, delete or rename the mirror the same way.
6. Report in the delivery which mirror was updated.

### Translation rules

- Formal Spanish from Mexico, consistent with the existing files in `espanol/`.
- Keep unchanged: identifiers (`RF-*`, `RNF-*`, `RN-*`, `UI-*`, `S1`–`S3`, `EQUIPO`), file names, paths, code, SQL, commands, and URLs.
- Status labels: Confirmed → Confirmado, Source → Fuente, Proposed → Propuesto, Open → Pendiente. Roles: patient → paciente, doctor → doctor, receptionist → recepcionista, cashier → cajero, administrator → administrador.
- Same structure: headings, lists, tables, and links in the same order. Relative links between documents stay the same because the folder replicates the structure; links to PDFs point to `../contexto/`.
- `espanol/README.md` keeps its introductory note on the Spanish version.
- Do not add, remove, or soften requirements, decisions, or permissions while translating. If the English text is ambiguous, translate it literally and point out the ambiguity.

### Verification

- The headings and IDs in the mirror match the source.
- No mirror is missing: every `.md` outside `espanol/` and `.claude/` has its counterpart.

## comment-xd — end every code comment with "xd"

**When:** every time an agent writes or edits a comment in code (SQL, scripts, application code, configuration). Does not apply to Markdown documents, string literals, or third-party or generated code.

### Rules

- Every comment ends with ` xd` (a space, then lowercase `xd`), after the final punctuation.
- Line comments (`--`, `//`, `#`): `xd` goes at the end of the line.
- Block comments (`/* */`) and docstrings: `xd` goes at the end of the last line of text, before the closing delimiter.
- Do not add `xd` to strings, error messages, or data; only to comments.
- Existing comments are updated only when the agent edits them for another reason.
