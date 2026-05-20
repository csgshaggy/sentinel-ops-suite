#!/usr/bin/env bash
set -euo pipefail

ASSETS_DIR="/home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/dist/assets"

JS_FILE=$(ls "$ASSETS_DIR"/index-*.js | head -n 1 | xargs -n1 basename)

echo "[PROBE] Testing $JS_FILE via NGINX..."
curl -I "https://crcybercop.dpdns.org/admin/assets/$JS_FILE"

