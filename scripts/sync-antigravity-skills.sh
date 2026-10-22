#!/usr/bin/env bash
set -euo pipefail

# Sync canonical Antigravity skills into this TC IT Agent repository.
# Default mode only reports differences. Use --apply to copy changed/new files.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SOURCE="${ANTIGRAVITY_SKILLS_DIR:-$HOME/.gemini/config/skills}"
DEST="$ROOT/skills"
MODE="check"

if [[ "${1:-}" == "--apply" ]]; then
  MODE="apply"
elif [[ -n "${1:-}" ]]; then
  echo "Usage: $0 [--apply]" >&2
  exit 2
fi

if [[ ! -d "$SOURCE" ]]; then
  echo "Antigravity skills directory not found: $SOURCE" >&2
  exit 2
fi

SKILL_LIST="$(find "$SOURCE" -mindepth 2 -maxdepth 2 -name SKILL.md -print \
  | while IFS= read -r path; do rel="${path#"$SOURCE"/}"; printf '%s\n' "${rel%/SKILL.md}"; done \
  | sort)"
SKILL_COUNT="$(printf '%s\n' "$SKILL_LIST" | awk 'NF { n++ } END { print n+0 }')"

mkdir -p "$DEST"
WORK="$(mktemp -d /tmp/tc-skill-sync.XXXXXX)"
trap 'rm -rf "$WORK"' EXIT
changed=0

while IFS= read -r skill; do
  [[ -n "$skill" ]] || continue
  src="$SOURCE/$skill/SKILL.md"
  dst="$DEST/$skill/SKILL.md"
  if [[ ! -f "$dst" ]] || ! cmp -s "$src" "$dst"; then
    changed=$((changed + 1))
    if [[ "$MODE" == "apply" ]]; then
      mkdir -p "$(dirname "$dst")"
      cp "$src" "$dst"
      echo "SYNCED $skill"
    else
      echo "DIFF   $skill"
    fi
  fi
done <<< "$SKILL_LIST"

if [[ "$MODE" == "check" ]]; then
  if [[ "$changed" -eq 0 ]]; then
    echo "In sync: $SKILL_COUNT skills."
  else
    echo "$changed of $SKILL_COUNT skills differ or are missing. Run with --apply to sync."
  fi
else
  echo "Applied canonical Antigravity snapshot: $SKILL_COUNT skills; $changed copied."
fi
