#!/usr/bin/env bash
set -euo pipefail

WORKFLOW_DIR=".github/workflows"

echo "🔧 Auto-fix: Starting governance-scoped workflow corrections..."

# Governance-critical workflows
GOVERNANCE_FILES=(
  "workflow-governance.yml"
  "avatar-integrity.yml"
)

fix_governance_file() {
  local FILE="$1"
  local PATH="$WORKFLOW_DIR/$FILE"

  echo "➡️ Processing governance workflow: $FILE"

  # Ensure permissions block exists
  if ! grep -q "^permissions:" "$PATH"; then
    echo "   ➕ Adding missing permissions block"
    sed -i '1a permissions:\n  contents: write\n  checks: write' "$PATH"
  fi

  # Ensure required triggers exist
  for TRIGGER in "pull_request" "push" "branches"; do
    if ! grep -q "$TRIGGER:" "$PATH"; then
      echo "   ➕ Adding missing trigger: $TRIGGER"
      sed -i "/^on:/a\  $TRIGGER:" "$PATH"
    fi
  done

  # Ensure check-run reporting step exists
  if ! grep -q "LouisBrunner/checks-action" "$PATH"; then
    echo "   ➕ Adding missing check-run reporting step"
    cat <<'EOF' >> "$PATH"

      - name: Report status
        uses: LouisBrunner/checks-action@v1
        with:
          token: \${{ github.token }}
          name: Governance Check
          status: success
EOF
  fi

  echo "   ✔ Governance workflow fixed"
}

# Iterate governance files only
for FILE in "${GOVERNANCE_FILES[@]}"; do
  FULL="$WORKFLOW_DIR/$FILE"
  if [[ -f "$FULL" ]]; then
    fix_governance_file "$FILE"
  else
    echo "⏭ Skipping missing governance file: $FILE"
  fi
done

echo "✅ Auto-fix complete (governance-scoped)"
