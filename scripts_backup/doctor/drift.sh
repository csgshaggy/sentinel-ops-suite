#!/usr/bin/env bash
set -e

echo ""
echo "==============================================="
echo "        STRUCTURE DRIFT DETECTOR"
echo "==============================================="
echo ""

# Ensure runtime directory exists
mkdir -p runtime

# Execute drift detector
python3 scripts/drift_detector.py

echo ""
echo "-----------------------------------------------"
echo " Drift detection complete"
echo "-----------------------------------------------"
echo ""
