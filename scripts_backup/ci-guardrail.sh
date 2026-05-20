#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/ubuntu/sentinel-ops-suite"
SCRIPTS="$ROOT/scripts"

echo "=== SENTINEL CI GUARDRAIL START ==="

echo "[STEP 1] Validating NGINX configuration..."
"$SCRIPTS/validate-nginx.sh"

echo "[STEP 2] Validating CSP formatting..."
"$SCRIPTS/validate-csp.sh"

echo "[STEP 3] Checking for header folding..."
"$SCRIPTS/detect-header-folding.sh"

echo "[STEP 4] Validating dashboard build output..."
"$SCRIPTS/check-dashboard-build.sh"

echo "[STEP 5] Optional: probing live dashboard asset..."
if [ -f "$SCRIPTS/probe-dashboard-asset.sh" ]; then
    "$SCRIPTS/probe-dashboard-asset.sh" || {
        echo "[WARNING] Live asset probe failed."
        exit 1
    }
else
    echo "[INFO] probe-dashboard-asset.sh not found — skipping."
fi

echo "=== SENTINEL CI GUARDRAIL PASSED ==="
