#!/usr/bin/env bash
set -euo pipefail

echo "============================================================"
echo " SENTINEL OPS — BUILD VALIDATOR"
echo " React 19 / Vite 5+ / Multi‑App"
echo "============================================================"

BASE="/home/ubuntu/sentinel-ops-suite"
LOGIN_DIST="$BASE/frontend/login-app/dist"
DASH_DIST="$BASE/frontend/dashboard-app/dist"

LOGIN_MANIFEST="$LOGIN_DIST/.vite/manifest.json"
DASH_MANIFEST="$DASH_DIST/.vite/manifest.json"

# -------------------------------------------------------------
# Helper: Validate manifest structure
# -------------------------------------------------------------
validate_manifest() {
    local manifest="$1"
    local app="$2"

    echo ""
    echo "Validating manifest for: $app"
    echo "Path: $manifest"

    if [[ ! -f "$manifest" ]]; then
        echo "❌ ERROR: Manifest missing for $app"
        exit 1
    fi

    if ! jq empty "$manifest" >/dev/null 2>&1; then
        echo "❌ ERROR: Manifest for $app is invalid JSON"
        exit 1
    fi

    if ! jq -e 'to_entries | .[0].value.file' "$manifest" >/dev/null 2>&1; then
        echo "❌ ERROR: Manifest for $app missing required 'file' entries"
        exit 1
    fi

    echo "✅ Manifest OK for $app"
}

# -------------------------------------------------------------
# Helper: Validate asset directory
# -------------------------------------------------------------
validate_assets() {
    local dist="$1"
    local app="$2"

    echo ""
    echo "Validating assets for: $app"
    echo "Dist: $dist"

    if [[ ! -d "$dist/assets" ]]; then
        echo "❌ ERROR: Missing assets directory for $app"
        exit 1
    fi

    # Ensure at least one JS bundle exists
    if ! ls "$dist/assets"/*.js >/dev/null 2>&1; then
        echo "❌ ERROR: No JS bundles found for $app"
        exit 1
    fi

    # Ensure at least one CSS bundle exists
    if ! ls "$dist/assets"/*.css >/dev/null 2>&1; then
        echo "❌ ERROR: No CSS bundles found for $app"
        exit 1
    fi

    # Ensure hashed filenames (Vite standard)
    if ls "$dist/assets" | grep -vE '[-_][A-Za-z0-9]{8,}\.(js|css)$' >/dev/null 2>&1; then
        echo "❌ ERROR: Found non‑hashed asset filenames in $app"
        exit 1
    fi

    echo "✅ Asset directory OK for $app"
}

# -------------------------------------------------------------
# Helper: Ensure no source files leaked into dist
# -------------------------------------------------------------
validate_no_source_leak() {
    local dist="$1"
    local app="$2"

    echo ""
    echo "Checking for source leaks in: $app"

    if find "$dist" -type f \( -name "*.jsx" -o -name "*.tsx" -o -name "*.ts" -o -name "*.map" \) | grep .; then
        echo "❌ ERROR: Source files leaked into dist for $app"
        exit 1
    fi

    echo "✅ No source leaks for $app"
}

# -------------------------------------------------------------
# Run validations
# -------------------------------------------------------------
validate_manifest "$LOGIN_MANIFEST" "login-app"
validate_manifest "$DASH_MANIFEST" "dashboard-app"

validate_assets "$LOGIN_DIST" "login-app"
validate_assets "$DASH_DIST" "dashboard-app"

validate_no_source_leak "$LOGIN_DIST" "login-app"
validate_no_source_leak "$DASH_DIST" "dashboard-app"

echo ""
echo "============================================================"
echo " BUILD VALIDATION PASSED — ALL SYSTEMS GREEN"
echo "============================================================"
