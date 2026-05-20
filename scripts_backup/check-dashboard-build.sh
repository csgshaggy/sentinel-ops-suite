#!/usr/bin/env bash
set -euo pipefail

DASHBOARD_DIST="/home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/dist"
ASSETS_DIR="$DASHBOARD_DIST/assets"

echo "[BUILD] Checking dashboard dist directory..."
if [ ! -d "$DASHBOARD_DIST" ]; then
  echo "[ERROR] Dashboard dist missing: $DASHBOARD_DIST"
  exit 1
fi

echo "[BUILD] Checking assets directory..."
if [ ! -d "$ASSETS_DIR" ]; then
  echo "[ERROR] Assets directory missing: $ASSETS_DIR"
  exit 1
fi

JS_COUNT=$(find "$ASSETS_DIR" -maxdepth 1 -type f -name "index-*.js" | wc -l)
CSS_COUNT=$(find "$ASSETS_DIR" -maxdepth 1 -type f -name "index-*.css" | wc -l)

echo "[BUILD] index-*.js files:  $JS_COUNT"
echo "[BUILD] index-*.css files: $CSS_COUNT"

if [ "$JS_COUNT" -eq 0 ]; then
  echo "[ERROR] No index-*.js bundle found in $ASSETS_DIR"
  exit 1
fi

if [ "$CSS_COUNT" -eq 0 ]; then
  echo "[ERROR] No index-*.css bundle found in $ASSETS_DIR"
  exit 1
fi

echo "[BUILD] Dashboard build output looks valid."
