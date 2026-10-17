#!/bin/bash
# Create the English and Spanish skeletons of a new feature spec with the next free SPEC number. xd
# Usage: scripts/new_spec.sh <slug> ["English feature name"] ["Nombre en español"] xd
set -euo pipefail
shopt -u patsub_replacement 2>/dev/null || true  # keep "&" literal in replacements on bash 5.2+ xd

root="$(cd "$(dirname "$0")/.." && pwd)"
slug="${1:-}"
name_en="${2:-}"
name_es="${3:-}"
slug_re='^[a-z][a-z0-9]*(-[a-z0-9]+)*$'

if [[ -z "$slug" ]]; then
  echo "usage: scripts/new_spec.sh <slug> [\"English feature name\"] [\"Nombre en español\"]" >&2
  exit 2
fi
if [[ ! "$slug" =~ $slug_re ]]; then
  echo "error: slug must be lowercase letters, digits, and single hyphens (example: cancel-appointment)" >&2
  exit 2
fi
for template in "$root/specs/template.md" "$root/espanol/specs/template.md"; do
  [[ -f "$template" ]] || { echo "error: missing template $template" >&2; exit 1; }
done

# Next free number across both language trees, so a mirror never collides with a source. xd
max=0
for f in "$root"/specs/[0-9][0-9][0-9]-*.md "$root"/espanol/specs/[0-9][0-9][0-9]-*.md; do
  [[ -e "$f" ]] || continue
  base="${f##*/}"
  n=$((10#${base:0:3}))
  (( n > max )) && max=$n
done
num="$(printf '%03d' $((max + 1)))"
en="$root/specs/$num-$slug.md"
es="$root/espanol/specs/$num-$slug.md"
for target in "$en" "$es"; do
  [[ -e "$target" ]] && { echo "error: $target already exists" >&2; exit 1; }
done

# $1 template, $2 target, $3 title placeholder, $4 title (optional). xd
render() {
  local content
  content="$(<"$1")"
  content="${content//SPEC-XXX/SPEC-$num}"
  if [[ -n "$4" ]]; then
    content="${content//"$3"/$4}"
  fi
  printf '%s\n' "$content" > "$2"
}
render "$root/specs/template.md" "$en" "Feature name" "$name_en"
render "$root/espanol/specs/template.md" "$es" "Nombre de la funcionalidad" "${name_es:-$name_en}"

echo "created specs/$num-$slug.md"
echo "created espanol/specs/$num-$slug.md"
if [[ -n "$name_en" && -z "$name_es" ]]; then
  echo "note: the Spanish title was copied from English; translate it in espanol/specs/$num-$slug.md"
fi
echo "next: fill the English spec citing IDs from their owner documents, keep status draft, update the mirror (spanish-sync), then run python3 scripts/trace_check.py"
