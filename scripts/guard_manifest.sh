#!/usr/bin/env bash
set -euo pipefail

echo "============================================================"
echo " SENTINEL OPS — MANIFEST GUARDRAIL (React 19 / Vite 5+)"
echo "============================================================"

LOGIN_MANIFEST="/home/ubuntu/sentinel-ops-suite/frontend/login-app/dist/.vite/manifest.json"
DASH_MANIFEST="/home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/dist/.vite/manifest.json"

# --- Helper ---------------------------------------------------
check_manifest() {
    local manifest_path="$1"
    local app_name="$2"

    echo ""
    echo "Checking manifest for: $app_name"
    echo "Path: $manifest_path"

    # 1. File must exist
    if [[ ! -f "$manifest_path" ]]; then
        echo "❌ ERROR: Manifest missing for $app_name"
        echo "Expected at: $manifest_path"
        exit 1
    fi

    # 2. File must be valid JSON
    if ! jq empty "$manifest_path" >/dev/null 2>&1; then
        echo "❌ ERROR: Manifest for $app_name is not valid JSON"
        exit 1
    fi

    # 3. Must contain at least one entry with a 'file' key
    if ! jq -e 'to_entries | .[0].value.file' "$manifest_path" >/dev/null 2>&1; then
        echo "❌ ERROR: Manifest for $app_name missing required 'file' entries"
        exit 1
    fi

    echo "✅ $app_name manifest OK"
}

# --- Run checks ----------------------------------------------
check_manifest "$LOGIN_MANIFEST" "login-app"
check_manifest "$DASH_MANIFEST" "dashboard-app"

echo ""
echo "============================================================"
echo " ALL MANIFESTS VALID — GUARDRAIL PASSED"
echo "============================================================"
