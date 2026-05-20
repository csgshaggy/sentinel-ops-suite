#!/bin/bash

echo "=== SentinelOps Logo Integrity Verification ==="
echo

SRC_LOGO="$HOME/sentinel-ops-suite/frontend/unified-frontend/src/assets/SentinelOps.jpg"
DIST_DIR="$HOME/sentinel-ops-suite/frontend/unified-frontend/dist/assets"
NGINX_DIR="/var/www/sentinel-ops-frontend/assets"

# --- Helper function ---
check_file() {
    local label="$1"
    local file="$2"

    if [ -f "$file" ]; then
        echo "[✔] $label FOUND:"
        echo "     Path: $file"
        echo "     Size: $(stat -c%s "$file") bytes"
        echo "     SHA256: $(sha256sum "$file" | awk '{print $1}')"
        echo
    else
        echo "[✘] $label NOT FOUND at:"
        echo "     $file"
        echo
    fi
}

echo "1) Checking SOURCE logo (React import)..."
check_file "Source Logo" "$SRC_LOGO"

echo "2) Checking BUILT Vite assets..."
DIST_LOGO=$(ls $DIST_DIR/SentinelOps-*.jpg 2>/dev/null | head -n 1)
check_file "Built Logo" "$DIST_LOGO"

echo "3) Checking DEPLOYED NGINX assets..."
NGINX_LOGO=$(ls $NGINX_DIR/SentinelOps-*.jpg 2>/dev/null | head -n 1)
check_file "Deployed Logo" "$NGINX_LOGO"

# --- Compare hashes ---
echo "4) Comparing hashes..."
if [ -f "$SRC_LOGO" ] && [ -f "$DIST_LOGO" ] && [ -f "$NGINX_LOGO" ]; then
    SRC_HASH=$(sha256sum "$SRC_LOGO" | awk '{print $1}')
    DIST_HASH=$(sha256sum "$DIST_LOGO" | awk '{print $1}')
    NGINX_HASH=$(sha256sum "$NGINX_LOGO" | awk '{print $1}')

    echo "Source Hash:   $SRC_HASH"
    echo "Built Hash:    $DIST_HASH"
    echo "Deployed Hash: $NGINX_HASH"
    echo

    if [[ "$SRC_HASH" == "$DIST_HASH" && "$DIST_HASH" == "$NGINX_HASH" ]]; then
        echo "=== RESULT: ✔ PASS — All logo files match exactly ==="
    else
        echo "=== RESULT: ✘ FAIL — Logo files DO NOT match ==="
        echo "    → This means the deployed logo is outdated or the build didn't include the new file."
    fi
else
    echo "=== RESULT: ✘ FAIL — One or more logo files missing ==="
fi

echo
echo "=== Verification Complete ==="
