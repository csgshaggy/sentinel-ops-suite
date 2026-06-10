#!/usr/bin/env bash
set -euo pipefail

WORKFLOW_DIR=".github/workflows"

echo "🔧 Patching GitHub workflows in $WORKFLOW_DIR ..."
echo ""

for FILE in $WORKFLOW_DIR/*.yml; do
    echo "➡️  Processing: $FILE"

    # ---------------------------------------------------------
    # 1. Ensure permissions block exists
    # ---------------------------------------------------------
    if ! grep -q "permissions:" "$FILE"; then
        echo "   ➕ Adding permissions block"
        # Insert after the 'on:' block
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
          token: \${{ secrets.GITHUB_TOKEN }}
          name: \${{ github.workflow }}
          conclusion: success
EOF
    else
        echo "   ✔ check-run reporting already exists"
    fi

    echo ""
done

echo "✅ All workflows patched successfully."
