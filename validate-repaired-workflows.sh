#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKFLOW_DIR="$REPO_ROOT/.github/workflows"

echo "🔍 Validating repaired GitHub workflows in $WORKFLOW_DIR"
echo ""

shopt -s nullglob
FILES=("$WORKFLOW_DIR"/*.yml)

if [ ${#FILES[@]} -eq 0 ]; then
    echo "❌ No workflow files found."
    exit 1
fi

FAIL=0

for FILE in "${FILES[@]}"; do
    echo "➡️  Checking: $FILE"

    # ---------------------------------------------------------
    # 1. Ensure exactly ONE 'on:' block
    # ---------------------------------------------------------
    ON_COUNT=$(grep -c "^on:" "$FILE" || true)
    if [ "$ON_COUNT" -ne 1 ]; then
        echo "   ❌ Invalid number of 'on:' blocks ($ON_COUNT)"
        FAIL=1
    else
        echo "   ✔ Exactly one 'on:' block"
    fi

    # ---------------------------------------------------------
    # 2. Ensure exactly ONE permissions block
    # ---------------------------------------------------------
    PERM_COUNT=$(grep -c "^permissions:" "$FILE" || true)
    if [ "$PERM_COUNT" -ne 1 ]; then
        echo "   ❌ Invalid number of permissions blocks ($PERM_COUNT)"
        FAIL=1
    else
        echo "   ✔ Exactly one permissions block"
    fi

    # ---------------------------------------------------------
    # 3. Validate required triggers
    # ---------------------------------------------------------
    if ! grep -q "pull_request:" "$FILE"; then
        echo "   ❌ Missing pull_request trigger"
        FAIL=1
    else
        echo "   ✔ pull_request trigger present"
    fi

    if ! grep -q "push:" "$FILE"; then
        echo "   ❌ Missing push trigger"
        FAIL=1
    else
        echo "   ✔ push trigger present"
    fi

    if ! grep -q "branches:" "$FILE"; then
        echo "   ❌ Missing branches block"
        FAIL=1
    else
        echo "   ✔ branches block present"
    fi

    # ---------------------------------------------------------
    # 4. Ensure check-run reporting step exists
    # ---------------------------------------------------------
    if ! grep -q "LouisBrunner/checks-action" "$FILE"; then
        echo "   ❌ Missing check-run reporting step"
        FAIL=1
    else
        echo "   ✔ check-run reporting step present"
    fi

    # ---------------------------------------------------------
    # 5. Validate YAML structure using Python (no external deps)
    # ---------------------------------------------------------
    if ! python3 - <<EOF >/dev/null 2>&1
import yaml, sys
yaml.safe_load(open("$FILE"))
EOF
    then
        echo "   ❌ YAML structure invalid"
        FAIL=1
    else
        echo "   ✔ YAML structure valid"
    fi

    echo ""
done

if [ "$FAIL" -eq 1 ]; then
    echo "❌ Validation failed — one or more workflows still need fixes."
    exit 1
fi

echo "✅ All workflows passed post-repair validation."
