#!/usr/bin/env bash
set -euo pipefail

WORKFLOW_DIR=".github/workflows"

echo "🔧 Fixing incorrect tokens in GitHub workflows..."
echo ""

shopt -s nullglob
FILES=("$WORKFLOW_DIR"/*.yml)

if [ ${#FILES[@]} -eq 0 ]; then
    echo "❌ No workflow files found."
    exit 1
fi

for FILE in "${FILES[@]}"; do
    echo "➡️  Checking: $FILE"

    # Replace secrets.GITHUB_TOKEN with github.token ONLY for checks-action
    if grep -q "LouisBrunner/checks-action" "$FILE"; then
        if grep -q "token: \${{ secrets.GITHUB_TOKEN }}" "$FILE"; then
            echo "   🔄 Fixing token..."
            sed -i 's/token: \${{ secrets.GITHUB_TOKEN }}/token: ${{ github.token }}/g' "$FILE"
            echo "   ✔ Token fixed"
        else
            echo "   ✔ Token already correct"
        fi
    else
        echo "   ⏭ No checks-action usage, skipping"
    fi

    echo ""
done

echo "✅ All tokens fixed."
