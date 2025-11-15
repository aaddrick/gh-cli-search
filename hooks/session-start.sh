#!/usr/bin/env bash
# Session-start hook for gh-cli-search plugin
# Loads the using-gh-cli-search skill at session start to introduce available skills

set -euo pipefail

# Find the plugin directory (go up from hooks/ to plugin root)
PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Load the intro skill content
SKILL_FILE="${PLUGIN_DIR}/skills/using-gh-cli-search/SKILL.md"

if [ ! -f "$SKILL_FILE" ]; then
    echo "Error: Skill file not found at $SKILL_FILE" >&2
    exit 1
fi

# Read the skill content
SKILL_CONTENT=$(cat "$SKILL_FILE")

# Escape for JSON
SKILL_CONTENT_ESCAPED=$(echo "$SKILL_CONTENT" | jq -Rs .)

# Output JSON context injection
cat <<EOF
{
  "hook": "SessionStart",
  "additional_context": "# gh-cli-search Skills Available\n\n${SKILL_CONTENT_ESCAPED}"
}
EOF
