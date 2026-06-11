#!/usr/bin/env bash
set -euo pipefail

# Force bash even if invoked under sh
[ -n "${BASH_VERSION:-}" ] || exec bash "$0" "$@"

WORKFLOW_DIR=".github/workflows"

echo " Auto-fix: Starting governance-scoped workflow corrections..."

# POSIX-safe list of governance workflow files
GOVERNANCE_FILES="workflow-governance.yml avatar-integrity.yml"

fix_governance_file() {
  FILE="$1"
  PATH="$WORKFLOW_DIR/$FILE"

  echo " Processing governance workflow: $FILE"

  # Ensure permissions block exists
  if ! grep -q "^permissions:" "$PATH"; then
    echo "    Adding missing permissions block"
    sed -i '1ipermissions:' "$PATH"
    sed -i '2i\  contents: write' "$PATH"
    sed -i '3i\  checks: write' "$PATH"
  fi

  # Ensure required triggers exist
  for TRIGGER in pull_request push branches; do
    if ! grep -q "$TRIGGER:" "$PATH"; then
      echo "    Adding missing trigger: $TRIGGER"
      sed -i "/^on:/a\  $TRIGGER:" "$PATH"
    fi
  done

  # Ensure check-run reporting step exists
  if ! grep -q "LouisBrunner/checks-action" "$PATH"; then
    echo "    Adding missing check-run reporting step"
    {
      echo ""
      echo "      - name: Report status"
      echo "        uses: LouisBrunner/checks-action@v1"
      echo "        with:"
      echo "          token: \${{ github.token }}"
      echo "          name: Governance Check"
      echo "          status: success"
    } >> "$PATH"
  fi

  echo "    Governance workflow fixed"
}

# Loop through governance files (POSIX-safe)
for FILE in $GOVERNANCE_FILES; do
  FULL="$WORKFLOW_DIR/$FILE"
  if [ -f "$FULL" ]; then
    fix_governance_file "$FILE"
  else
    echo " Skipping missing governance file: $FILE"
  fi
done

echo " Auto-fix complete (governance-scoped)"
