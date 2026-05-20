#!/usr/bin/env bash
set -euo pipefail

echo "[frontend_smoke] Running frontend smoke tests..."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

LOGIN_APP_DIST="$FRONTEND_DIR/login-app/dist"
DASHBOARD_APP_DIST="$FRONTEND_DIR/dashboard-app/dist"

BAD=0

smoke_check() {
    local app_name="$1"
    local dist_path="$2"

    echo "[frontend_smoke] Checking $app_name..."

    # 1. dist directory must exist
    if [[ ! -d "$dist_path" ]]; then
        echo "  -> ERROR: dist/ directory not found for $app_name: $dist_path"
        BAD=1
        return
    fi

    # 2. index.html must exist
    if [[ ! -f "$dist_path/index.html" ]]; then
        echo "  -> ERROR: $app_name missing index.html"
        BAD=1
    fi

    # 3. assets directory must exist
    if [[ ! -d "$dist_path/assets" ]]; then
        echo "  -> ERROR: $app_name missing assets/ directory"
        BAD=1
    fi

    # 4. Basic smoke test: ensure index.html is not empty
    if [[ ! -s "$dist_path/index.html" ]]; then
        echo "  -> ERROR: $app_name index.html is empty"
        BAD=1
    fi

    echo "  -> OK: $app_name smoke test passed"
}

# Run smoke tests for both apps
smoke_check "login-app" "$LOGIN_APP_DIST"
smoke_check "dashboard-app" "$DASHBOARD_APP_DIST"

# Final result
if [[ "$BAD" -eq 1 ]]; then
    echo "[frontend_smoke] FAIL: One or more smoke tests failed."
    exit 1
fi

echo "[frontend_smoke] SUCCESS: All frontend smoke tests passed."

