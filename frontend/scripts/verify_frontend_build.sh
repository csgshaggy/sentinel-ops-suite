#!/usr/bin/env bash
set -euo pipefail

FRONTEND_ROOT="/home/ubuntu/sentinel-ops-suite/frontend/unified-frontend/dist"
NGINX_ROOT="/home/ubuntu/sentinel-ops-suite/frontend/unified-frontend/dist"

echo "=== SentinelOps Frontend Build Verification ==="
echo

# 1. Check build directory
echo "[1] Checking build directory..."
if [[ ! -d "$FRONTEND_ROOT" ]]; then
    echo "❌ Build directory not found: $FRONTEND_ROOT"
    exit 1
fi
echo "✔ Build directory exists"
echo

# 2. Check index.html
echo "[2] Checking index.html..."
INDEX="$FRONTEND_ROOT/index.html"
if [[ ! -f "$INDEX" ]]; then
    echo "❌ index.html missing"
    exit 1
fi
echo "✔ index.html exists"
echo

# 3. Extract JS + CSS bundle references
echo "[3] Extracting bundle references..."
JS=$(grep -o 'assets/.*\.js' "$INDEX" | head -n 1)
CSS=$(grep -o 'assets/.*\.css' "$INDEX" | head -n 1)

echo "JS bundle:  $JS"
echo "CSS bundle: $CSS"
echo

# 4. Validate bundle files exist
echo "[4] Validating bundle files..."
if [[ ! -f "$FRONTEND_ROOT/$JS" ]]; then
    echo "❌ JS bundle missing: $JS"
    exit 1
fi
if [[ ! -f "$FRONTEND_ROOT/$CSS" ]]; then
    echo "❌ CSS bundle missing: $CSS"
    exit 1
fi
echo "✔ Bundles exist"
echo

# 5. Check for stale bundles
echo "[5] Checking for stale bundles..."
STALE=$(find "$FRONTEND_ROOT/assets" -type f ! -name "$(basename "$JS")" ! -name "$(basename "$CSS")")
if [[ -n "$STALE" ]]; then
    echo "⚠️ Stale bundles detected:"
    echo "$STALE"
else
    echo "✔ No stale bundles"
fi
echo

# 6. Check NGINX root alignment
echo "[6] Checking NGINX root alignment..."
if [[ "$FRONTEND_ROOT" == "$NGINX_ROOT" ]]; then
    echo "✔ NGINX root matches build directory"
else
    echo "❌ NGINX root mismatch"
    echo "Frontend: $FRONTEND_ROOT"
    echo "NGINX:    $NGINX_ROOT"
    exit 1
fi
echo

# 7. Permissions
echo "[7] Checking permissions..."
find "$FRONTEND_ROOT" -type f -exec chmod 644 {} \;
find "$FRONTEND_ROOT" -type d -exec chmod 755 {} \;
echo "✔ Permissions normalized"
echo

echo "=== Frontend Build Verification Complete ==="
