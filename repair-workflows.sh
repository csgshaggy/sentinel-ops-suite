#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKFLOW_DIR="$REPO_ROOT/.github/workflows"

echo "🔧 Repairing malformed GitHub workflows in $WORKFLOW_DIR"
echo ""

shopt -s nullglob
FILES=("$WORKFLOW_DIR"/*.yml)

for FILE in "${FILES[@]}"; do
    echo "➡️  Repairing: $FILE"

    # Extract name line
    NAME_LINE=$(head -n 1 "$FILE")

    # Extract everything after the first job definition
    BODY=$(awk '
        /^jobs:/ {flag=1}
        flag {print}
    ' "$FILE")

    # Rebuild file with correct structure
    {
        echo "$NAME_LINE"
        echo ""
        echo "on:"
        echo "  pull_request:"
        echo "  push:"
        echo "    branches:"
        echo "      - main"
        echo ""
        echo "permissions:"
        echo "  contents: read"
        echo "  checks: write"
        echo ""
        echo "$BODY"
    } > "$FILE.tmp"

    mv "$FILE.tmp" "$FILE"
    echo "   ✔ Workflow repaired"
    echo ""
done

echo "✅ All workflows repaired successfully."
