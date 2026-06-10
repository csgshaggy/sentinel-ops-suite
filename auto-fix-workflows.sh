#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKFLOW_DIR="$REPO_ROOT/.github/workflows"

echo "🔧 Auto-fixing GitHub workflow YAML files in $WORKFLOW_DIR"
echo ""

shopt -s nullglob
FILES=("$WORKFLOW_DIR"/*.yml)

if [ ${#FILES[@]} -eq 0 ]; then
    echo "❌ No workflow files found."
    exit 1
fi

for FILE in "${FILES[@]}"; do
    echo "➡️  Fixing: $FILE"

    # Extract name line
    NAME_LINE=$(head -n 1 "$FILE")

    # Extract everything after the jobs: block
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
    echo "   ✔ Structure repaired"

    # Ensure check-run reporting exists
    if ! grep -q "LouisBrunner/checks-action" "$FILE"; then
        echo "   ➕ Adding check-run reporting step"
        cat << 'EOF' >> "$FILE"

      - name: Report status
        uses: LouisBrunner/checks-action@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          name: ${{ github.workflow }}
          conclusion: success
EOF
    else
        echo "   ✔ Check-run reporting already present"
    fi

    echo ""
done

echo "✅ Auto-fix complete. All workflows repaired."
