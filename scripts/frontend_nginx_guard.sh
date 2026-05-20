
#!/usr/bin/env bash
set -euo pipefail

echo "[frontend_nginx_guard] Starting NGINX deployment validation..."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

LOGIN_APP_DIST="$FRONTEND_DIR/login-app/dist"
DASHBOARD_APP_DIST="$FRONTEND_DIR/dashboard-app/dist"

BAD=0

validate_nginx_ready() {
    local app_name="$1"
    local dist_path="$2"

    echo "[frontend_nginx_guard] Checking NGINX readiness for $app_name..."

    # 1. dist directory must exist
    if [[ ! -d "$dist_path" ]]; then
        echo "  -> ERROR: dist/ missing for $app_name: $dist_path"
        BAD=1
        return
    fi

    # 2. index.html must exist
    if [[ ! -f "$dist_path/index.html" ]]; then
        echo "  -> ERROR: $app_name missing index.html (NGINX cannot serve SPA)"
        BAD=1
    fi

    # 3. index.html must not be empty
    if [[ ! -s "$dist_path/index.html" ]]; then
        echo "  -> ERROR: $app_name index.html is empty"
        BAD=1
    fi

    # 4. assets directory must exist
    if [[ ! -d "$dist_path/assets" ]]; then
        echo "  -> ERROR: $app_name missing assets/ directory"
        BAD=1
    fi

    # 5. Ensure assets directory is not empty
    if [[ -z "$(ls -A "$dist_path/assets")" ]]; then
        echo "  -> ERROR: $app_name assets/ directory is empty"
        BAD=1
    fi

    # 6. Ensure NGINX-readable permissions
    while IFS= read -r file; do
        if [[ ! -r "$file" ]]; then
            echo "  -> ERROR: $file is not readable (NGINX will fail)"
            BAD=1
        fi
    done < <(find "$dist_path" -type f)

    # 7. Ensure no forbidden file types (security hardening)
    if find "$dist_path" -type f -name "*.map" | grep -q .; then
        echo "  -> WARNING: Source maps detected in $app_name (not recommended for production)"
    fi

    echo "  -> OK: $app_name is NGINX-ready"
}

validate_nginx_ready "login-app" "$LOGIN_APP_DIST"
validate_nginx_ready "dashboard-app" "$DASHBOARD_APP_DIST"

if [[ "$BAD" -eq 1 ]]; then
    echo "[frontend_nginx_guard] FAIL: One or more apps are not NGINX-ready."
    exit 1
fi

echo "[frontend_nginx_guard] SUCCESS: All frontend apps are NGINX-ready for deployment."

