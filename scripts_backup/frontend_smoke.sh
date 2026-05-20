#!/usr/bin/env bash
set -euo pipefail

# Chain banner
echo -e "\n\033[1;36m[CHAIN] Running: $(basename "$0")\033[0m"

echo "[frontend_smoke] Running frontend smoke tests..."

# Resolve script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
DIST_DIR="$FRONTEND_DIR/dist"

###############################################
# 1. Ensure dist/ exists
###############################################
echo "[frontend_smoke] Checking for dist/ directory..."

if [[ ! -d "$DIST_DIR" ]]; then
    echo "[frontend_smoke] ERROR: dist/ directory not found. Did you run the frontend build?"
    exit 1
fi

echo "[frontend_smoke] OK: dist/ directory found."

###############################################
# 2. Ensure index.html exists and is readable
###############################################
echo "[frontend_smoke] Checking index.html..."

INDEX_FILE="$DIST_DIR/index.html"

if [[ ! -f "$INDEX_FILE" ]]; then
    echo "[frontend_smoke] ERROR: index.html not found in dist/"
    exit 1
fi

if [[ ! -s "$INDEX_FILE" ]]; then
    echo "[frontend_smoke] ERROR: index.html is empty — build may be corrupted."
    exit 1
fi

echo "[frontend_smoke] OK: index.html exists and is non-empty."

###############################################
# 3. Ensure JS bundles exist
###############################################
echo "[frontend_smoke] Checking JS bundles..."

JS_COUNT=$(find "$DIST_DIR" -maxdepth 1 -type f -name "*.js" | wc -l | tr -d ' ')

if [[ "$JS_COUNT" -eq 0 ]]; then
    echo "[frontend_smoke] ERROR: No JavaScript bundles found in dist/"
    exit 1
fi

echo "[frontend_smoke] OK: $JS_COUNT JS bundle(s) found."

###############################################
# 4. Validate index.html contains expected markers
###############################################
echo "[frontend_smoke] Validating index.html content..."

EXPECTED_MARKERS=(
    "<div id=\"root\">"
    "<!DOCTYPE html>"
)

for marker in "${EXPECTED_MARKERS[@]}"; do
    if grep -q "$marker" "$INDEX_FILE"; then
        echo "[frontend_smoke] OK: Found marker '$marker'"
    else
        echo "[frontend_smoke] WARNING: Missing expected marker '$marker'"
    fi
done

###############################################
# 5. Final result
###############################################
echo "[frontend_smoke] Frontend smoke tests complete."
