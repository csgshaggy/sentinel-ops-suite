#!/usr/bin/env bash
set -euo pipefail

echo "[frontend_hash_guard] Starting hash-based drift detection..."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

LOGIN_APP_DIST="$FRONTEND_DIR/login-app/dist"
DASHBOARD_APP_DIST="$FRONTEND_DIR/dashboard-app/dist"

HASH_DIR="$ROOT_DIR/.hashes"
mkdir -p "$HASH_DIR"

BAD=0

compute_hash() {
    local app_name="$1"
    local dist_path="$2"
    local hash_file="$HASH_DIR/${app_name}.sha256"

    echo "[frontend_hash_guard] Checking $app_name..."

    if [[ ! -d "$dist_path" ]]; then
        echo "  -> ERROR: dist directory missing for $app_name: $dist_path"
        BAD=1
        return
    fi

    # Compute current hash
    local current_hash
    current_hash="$(find "$dist_path" -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum | awk '{print $1}')"

    # If no baseline exists, create one
    if [[ ! -f "$hash_file" ]]; then
        echo "  -> Baseline hash missing. Creating new baseline for $app_name."
        echo "$current_hash" > "$hash_file"
        echo "  -> OK: Baseline established."
        return
    fi

    # Read stored baseline
    local baseline_hash
    baseline_hash="$(cat "$hash_file")"

    # Compare
    if [[ "$current_hash" != "$baseline_hash" ]]; then
        echo "  -> ERROR: Drift detected in $app_name dist folder!"
        echo "     Baseline: $baseline_hash"
        echo "     Current : $current_hash"
        BAD=1
    else
        echo "  -> OK: No drift detected for $app_name."
    fi
}

compute_hash "login-app" "$LOGIN_APP_DIST"
compute_hash "dashboard-app" "$DASHBOARD_APP_DIST"

if [[ "$BAD" -eq 1 ]]; then
    echo "[frontend_hash_guard] FAIL: Drift detected."
    exit 1
fi

echo "[frontend_hash_guard] SUCCESS: No drift detected in any frontend app."

