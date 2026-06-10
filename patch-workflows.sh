#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKFLOW_DIR="$REPO_ROOT/.github/workflows"

echo "🔧 Patching GitHub workflows in $WORKFLOW_DIR ..."
echo ""

shopt -s nullglob
FILES=("$WORKFLOW_DIR"/*.yml)

if [ ${#FILES[@]} -eq 0 ]; then
    echo "❌ No workflow files found in $WORKFLOW_DIR"
    exit 1
fi

for FILE in "${FILES[@]}"; do
    echo "➡️  Processing: $FILE"

    # ---------------------------------------------------------
    # 1. Ensure permissions block exists
    # ---------------------------------------------------------
    if ! grep -q "^permissions:" "$FILE"; then
        echo "   ➕ Adding permissions block"
        awk '
            /on:/ && !x {print; print "permissions:\n  contents: read\n  checks: write"; x=1; next}
            1
        ' "$FILE" > "$FILE.tmp" && mv "$FILE.tmp" "$FILE"
    else
        echo "   ✔ permissions block already exists"
    fi

    # ---------------------------------------------------------
    # 2. Ensure final check-run reporting step exists
    # ---------------------------------------------------------
    if ! grep -q "LouisBrunner/checks-action" "$FILE"; then
        echo "   ➕ Adding final check-run reporting step"
        cat << 'EOF' >> "$FILE"

      - name: Report status
        uses: LouisBrunner/checks-action@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          name: ${{ github.workflow }}
          conclusion: success
EOF
    else
        echo "   ✔ check-run reporting already exists"
    fi

    echo ""
done

echo "✅ All workflows patched successfully."
