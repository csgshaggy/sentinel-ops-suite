#!/usr/bin/env bash
set -euo pipefail

echo "[frontend_doctor] Starting full frontend validation, build, and smoke test..."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

LOGIN_APP_DIR="$FRONTEND_DIR/login-app"
DASHBOARD_APP_DIR="$FRONTEND_DIR/dashboard-app"

LOGIN_APP_DIST="$LOGIN_APP_DIR/dist"
DASHBOARD_APP_DIST="$DASHBOARD_APP_DIR/dist"

BAD=0

# -----------------------------
# 1. VALIDATION
# -----------------------------
validate_app() {
    local app_name="$1"
    local app_dir="$2"

    echo "[frontend_doctor] Validating $app_name directory..."

    if [[ ! -d "$app_dir" ]]; then
        echo "  -> ERROR: $app_name directory missing: $app_dir"
        BAD=1
        return
    fi

    if [[ ! -f "$app_dir/package.json" ]]; then
        echo "  -> ERROR: $app_name missing package.json"
        BAD=1
    fi

    echo "  -> OK: $app_name structure looks valid"
}

validate_app "login-app" "$LOGIN_APP_DIR"
validate_app "dashboard-app" "$DASHBOARD_APP_DIR"

# -----------------------------
# 2. BUILD
# -----------------------------
build_app() {
    local app_name="$1"
    local app_dir="$2"

    echo "[frontend_doctor] Building $app_name..."

    cd "$app_dir"

    if [[ ! -d node_modules ]]; then
        echo "  -> Installing dependencies for $app_name..."
        npm install --silent
    fi

    echo "  -> Running build for $app_name..."
    npm run build --silent || {
        echo "  -> ERROR: Build failed for $app_name"
        BAD=1
        return
    }

    echo "  -> OK: $app_name build completed"
}

build_app "login-app" "$LOGIN_APP_DIR"
build_app "dashboard-app" "$DASHBOARD_APP_DIR"

# -----------------------------
# 3. SMOKE TEST
# -----------------------------
smoke_check() {
    local app_name="$1"
    local dist_path="$2"

    echo "[frontend_doctor] Smoke testing $app_name..."

    if [[ ! -d "$dist_path" ]]; then
        echo "  -> ERROR: dist/ directory missing for $app_name: $dist_path"
        BAD=1
        return
    fi

    if [[ ! -f "$dist_path/index.html" ]]; then
        echo "  -> ERROR: $app_name missing index.html"
        BAD=1
    fi

    if [[ ! -d "$dist_path/assets" ]]; then
        echo "  -> ERROR: $app_name missing assets/ directory"
        BAD=1
    fi

    if [[ ! -s "$dist_path/index.html" ]]; then
        echo "  -> ERROR: $app_name index.html is empty"
        BAD=1
    fi

    echo "  -> OK: $app_name smoke test passed"
}

smoke_check "login-app" "$LOGIN_APP_DIST"
smoke_check "dashboard-app" "$DASHBOARD_APP_DIST"

# -----------------------------
# FINAL RESULT
# -----------------------------
if [[ "$BAD" -eq 1 ]]; then
    echo "[frontend_doctor] FAIL: One or more frontend checks failed."
    exit 1
fi

echo "[frontend_doctor] SUCCESS: All frontend apps validated, built, and passed smoke tests."

