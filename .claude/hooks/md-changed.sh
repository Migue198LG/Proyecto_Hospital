#!/bin/bash
# PostToolUse: when an English .md changes, ask the agent to sync its Spanish mirror (SKILLS.md → spanish-sync). xd
input=$(cat)
file=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')
# Repo root is two levels above this script, so it works whatever folder the session was opened in. xd
root="$(cd "$(dirname "$0")/../.." && pwd)"
case "$file" in
  "$root"/*.md) rel="${file#"$root"/}" ;;
  *) exit 0 ;;
esac
case "$rel" in
  espanol/*|.claude/*|contexto/*) exit 0 ;;
esac
jq -n --arg rel "$rel" '{hookSpecificOutput: {hookEventName: "PostToolUse",
  additionalContext: ("\($rel) changed. Apply the spanish-sync skill from SKILLS.md: update espanol/\($rel) with the Spanish translation before finishing.")}}'
