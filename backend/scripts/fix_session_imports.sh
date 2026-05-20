#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/ubuntu/sentinel-ops-suite/backend"

echo "=== SentinelOps Import Fixer ==="
echo "Scanning for 'app.models.session' imports..."
echo

# Find all real source files that import the old model
mapfile -t FILES < <(
    grep -R "from src.session_models import" -n "$ROOT" \
        | grep -v "\.bak" \
        | grep -v "__pycache__" \
        | grep -v "code_health_report.json" \
        | awk -F: '{print $1}' \
        | sort -u
)

if [[ ${#FILES[@]} -eq 0 ]]; then
    echo "No files found with the old import. Nothing to do."
    exit 0
fi

echo "Found ${#FILES[@]} file(s) to patch:"
printf ' - %s\n' "${FILES[@]}"
echo

for FILE in "${FILES[@]}"; do
    echo "Patching: $FILE"

    # Backup
    cp "$FILE" "$FILE.bak"

    # Replace import
    sed -i "s|from src.session_models import|from src.session_models import|g" "$FILE"

    echo "  ✔ Updated and backed up to $FILE.bak"
done

echo
echo "=== Clearing __pycache__ directories ==="
find "$ROOT" -type d -name "__pycache__" -exec rm -rf {} +
echo "  ✔ Cleared"

echo
echo "=== Done. Restart backend ==="
echo "sudo systemctl restart sentinel-backend.service"
