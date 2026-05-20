#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/ubuntu/sentinel-ops-suite/backend/app"
STALE_DIR="$ROOT/routes"
GOOD_DIR="$ROOT/routers"

echo "=== SentinelOps Router Cleanup ==="
echo

# 1. Check for stale routes directory
if [[ -d "$STALE_DIR" ]]; then
    echo "[!] Stale directory found: $STALE_DIR"
    echo "    Removing..."
    rm -rf "$STALE_DIR"
    echo "    ✔ Removed stale routes directory"
else
    echo "✔ No stale routes directory found"
fi

echo

# 2. Verify correct router directory exists
if [[ -d "$GOOD_DIR" ]]; then
    echo "✔ Valid router directory exists: $GOOD_DIR"
else
    echo "❌ ERROR: Expected router directory missing: $GOOD_DIR"
    echo "Aborting."
    exit 1
fi

echo

# 3. Verify correct auth router file exists
if [[ -f "$GOOD_DIR/auth.py" ]]; then
    echo "✔ Valid auth router found: $GOOD_DIR/auth.py"
else
    echo "❌ ERROR: Missing auth router: $GOOD_DIR/auth.py"
    echo "Aborting."
    exit 1
fi

echo

# 4. Clear all __pycache__ directories
echo "Clearing __pycache__ directories..."
find "$ROOT" -type d -name "__pycache__" -exec rm -rf {} +
echo "✔ Cleared all __pycache__"

echo

# 5. Confirm no stale imports remain
echo "Scanning for stale imports..."
STALE_IMPORTS=$(grep -R "app.routes" -n "$ROOT" || true)

if [[ -n "$STALE_IMPORTS" ]]; then
    echo "❌ Stale imports found:"
    echo "$STALE_IMPORTS"
    echo "You must manually fix these."
else
    echo "✔ No stale imports found"
fi

echo
echo "=== Cleanup Complete ==="
echo "Restart backend with:"
echo "sudo systemctl restart sentinel-backend.service"
