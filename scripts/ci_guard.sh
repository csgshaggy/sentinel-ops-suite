#!/usr/bin/env bash
set -euo pipefail

echo "[ci_guard] Starting CI guardrail validation..."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

LOGIN_APP_DIST="$FRONTEND_DIR/login-app/dist"
DASHBOARD_APP_DIST="$FRONTEND_DIR/dashboard-app/dist"

BAD=0

check_dist() {
    local app_name="$1"
    local dist_path="$2"

    echo "[ci_guard] Checking $app_name build artifacts..."

    # 1. Directory must exist
    if [[ ! -d "$dist_path" ]]; then
        echo "  -> ERROR: $app_name dist directory not found: $dist_path"
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

    echo "  -> OK: $app_name build artifacts look valid"
}

# Run checks for both apps
check_dist "login-app" "$LOGIN_APP_DIST"
check_dist "dashboard-app" "$DASHBOARD_APP_DIST"

# Final result
if [[ "$BAD" -eq 1 ]]; then
    echo "[ci_guard] FAIL: One or more frontend builds are invalid or missing."
    exit 1
fi

echo "[ci_guard] SUCCESS: All frontend builds validated successfully."
