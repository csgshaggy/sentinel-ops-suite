#!/usr/bin/env bash
set -euo pipefail

echo "[frontend_manifest_guard] Starting Vite manifest validation..."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

LOGIN_APP_DIST="$FRONTEND_DIR/login-app/dist"
DASHBOARD_APP_DIST="$FRONTEND_DIR/dashboard-app/dist"

BAD=0

validate_manifest() {
    local app_name="$1"
    local dist_path="$2"
    local manifest="$dist_path/.vite/manifest.json"

    echo "[frontend_manifest_guard] Checking $app_name manifest..."

    # 1. manifest.json must exist (Vite 5: dist/.vite/manifest.json)
    if [[ ! -f "$manifest" ]]; then
        echo "  -> ERROR: manifest.json missing for $app_name (expected: $manifest)"
        BAD=1
        return
    fi

    # 2. Validate JSON syntax
    if ! jq empty "$manifest" >/dev/null 2>&1; then
        echo "  -> ERROR: manifest.json for $app_name is not valid JSON"
        BAD=1
        return
    fi

    # 3. Ensure required Vite keys exist
    local required_keys=("file" "isEntry")
    for key in "${required_keys[@]}"; do
        if ! jq -e ".[].$key" "$manifest" >/dev/null 2>&1; then
            echo "  -> ERROR: manifest.json missing required key '$key' for $app_name"
            BAD=1
        fi
    done

    # 4. Ensure all referenced files exist
    local missing_assets=0
    while IFS= read -r asset; do
        if [[ -n "$asset" && ! -f "$dist_path/$asset" ]]; then
            echo "  -> ERROR: Referenced asset missing for $app_name: $asset"
            missing_assets=1
        fi
    done < <(jq -r '.[] | .file, (.css[]? // empty), (.assets[]? // empty)' "$manifest")

    if [[ "$missing_assets" -eq 1 ]]; then
        BAD=1
    else
        echo "  -> OK: All manifest assets exist for $app_name"
    fi

    echo "  -> OK: $app_name manifest validated"
}

validate_manifest "login-app" "$LOGIN_APP_DIST"
validate_manifest "dashboard-app" "$DASHBOARD_APP_DIST"

if [[ "$BAD" -eq 1 ]]; then
    echo "[frontend_manifest_guard] FAIL: One or more manifest validations failed."
    exit 1
fi

echo "[frontend_manifest_guard] SUCCESS: All Vite manifests validated successfully."
