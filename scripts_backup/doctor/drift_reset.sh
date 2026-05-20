#!/usr/bin/env bash
set -e

BASELINE="runtime/structure_baseline.json"

echo ""
echo "==============================================="
echo "        STRUCTURE BASELINE RESET"
echo "==============================================="
echo ""

# Safety confirmation
read -p "This will overwrite the existing baseline. Continue? (y/N): " CONFIRM

if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "[+] Regenerating baseline..."
mkdir -p runtime

python3 scripts/drift_detector.py --generate-baseline

echo "[+] Baseline updated: $BASELINE"
echo ""
