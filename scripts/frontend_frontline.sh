#!/usr/bin/env bash
set -euo pipefail

echo "[frontend_frontline] Starting unified frontend validation pipeline..."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

LOGIN_APP_DIR="$FRONTEND_DIR/login-app"
DASHBOARD_APP_DIR="$FRONTEND_DIR/dashboard-app"

LOGIN_APP_DIST="$LOGIN_APP_DIR/dist"
DASHBOARD_APP_DIST="$DASHBOARD_APP_DIR/dist"

BAD=0

# -----------------------------
# 1. VALIDATION (structure)
# -----------------------------
validate_structure() {
    local app_name="$1"
    local app_dir="$2"

    echo "[frontend_frontline] Validating structure for $app_name..."

    if [[ ! -d "$app_dir" ]]; then
        echo "  -> ERROR: $app_name directory missing: $app_dir"
        BAD=1
        return
    fi

    if [[ ! -f "$app_dir/package.json" ]]; then
        echo "  -> ERROR: $app_name missing package.json"
        BAD=1
    fi

    echo "  -> OK: $app_name structure valid"
}

validate_structure "login-app" "$LOGIN_APP_DIR"
validate_structure "dashboard-app" "$DASHBOARD_APP_DIR"

# -----------------------------
# 2. BUILD (npm install + build)
# -----------------------------
build_app() {
    local app_name="$1"
    local app_dir="$2"

    echo "[frontend_frontline] Building $app_name..."

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
# 3. SMOKE TEST (dist sanity)
# -----------------------------
smoke_test() {
    local app_name="$1"
    local dist_path="$2"

    echo "[frontend_frontline] Smoke testing $app_name..."

    if [[ ! -d "$dist_path" ]]; then
        echo "  -> ERROR: dist/ missing for $app_name: $dist_path"
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

smoke_test "login-app" "$LOGIN_APP_DIST"
smoke_test "dashboard-app" "$DASHBOARD_APP_DIST"

# -----------------------------
# 4. CI GUARD (artifact integrity)
# -----------------------------
ci_guard() {
    local app_name="$1"
    local dist_path="$2"

    echo "[frontend_frontline] CI guard: validating $app_name artifacts..."

    if [[ ! -d "$dist_path" ]]; then
        echo "  -> ERROR: dist/ not found for $app_name"
        BAD=1
        return
    fi

    if [[ ! -f "$dist_path/index.html" ]]; then
        echo "  -> ERROR: $app_name missing index.html"
        BAD=1
    fi

    if [[ ! -d "$dist_path/assets" ]]; then
        echo "  -> ERROR: $app_name missing assets/"
        BAD=1
    fi

    echo "  -> OK: $app_name artifacts validated"
}

ci_guard "login-app" "$LOGIN_APP_DIST"
ci_guard "dashboard-app" "$DASHBOARD_APP_DIST"

# -----------------------------
# FINAL RESULT
# -----------------------------
if [[ "$BAD" -eq 1 ]]; then
    echo "[frontend_frontline] FAIL: One or more checks failed."
    exit 1
fi

echo "[frontend_frontline] SUCCESS: All frontend apps validated, built, and passed CI guard."

