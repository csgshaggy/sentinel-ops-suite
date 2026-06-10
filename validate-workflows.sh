#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKFLOW_DIR="$REPO_ROOT/.github/workflows"

echo "🔍 Validating GitHub workflows in $WORKFLOW_DIR"
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
    # 1. YAML syntax check
    # ---------------------------------------------------------
    if ! yamllint -d "{extends: relaxed, rules: {line-length: disable}}" "$FILE" >/dev/null 2>&1; then
        echo "   ❌ Invalid YAML syntax"
        FAIL=1
    else
        echo "   ✔ YAML syntax valid"
    fi

    # ---------------------------------------------------------
    # 2. Check for valid 'on:' block
    # ---------------------------------------------------------
    if ! grep -q "^on:" "$FILE"; then
        echo "   ❌ Missing 'on:' block"
        FAIL=1
    else
        echo "   ✔ 'on:' block present"
    fi

    # ---------------------------------------------------------
    # 3. Check for required triggers
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

    # ---------------------------------------------------------
    # 4. Check for permissions block
    # ---------------------------------------------------------
    if ! grep -q "^permissions:" "$FILE"; then
        echo "   ❌ Missing permissions block"
        FAIL=1
    else
        echo "   ✔ permissions block present"
    fi

    # ---------------------------------------------------------
    # 5. Check for check-run reporting step
    # ---------------------------------------------------------
    if ! grep -q "LouisBrunner/checks-action" "$FILE"; then
        echo "   ❌ Missing check-run reporting step"
        FAIL=1
    else
        echo "   ✔ check-run reporting step present"
    fi

    echo ""
done

if [ "$FAIL" -eq 1 ]; then
    echo "❌ Validation failed — one or more workflows need fixes."
    exit 1
fi

echo "✅ All workflows passed validation."
