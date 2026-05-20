#!/usr/bin/env bash
set -euo pipefail

echo "[validator] Scanning script integrity..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

BAD=0

for file in "$SCRIPT_DIR"/*.sh; do
    echo "[validator] Checking: $(basename "$file")"

    # 1. Check for Edge metadata contamination
    if grep -q "edge_all_open_tabs" "$file" || \
       grep -q "# User's Edge browser tabs metadata" "$file" || \
       grep -q "<WebsiteContent_" "$file"; then
        echo "  -> ERROR: Contamination detected in $(basename "$file")"
        BAD=1
    fi

    # 2. Check for stray numeric lines
    if grep -qE '^[0-9]+$' "$file"; then
        echo "  -> WARNING: Stray numeric line detected"
        BAD=1
    fi

    # 3. Check executable bit
    if [[ ! -x "$file" ]]; then
        echo "  -> FIXING: Missing executable bit"
        chmod +x "$file"
    fi

    echo "  -> OK"
done

if [[ "$BAD" -eq 1 ]]; then
    echo "[validator] FAIL: One or more scripts contain contamination."
    echo "[validator] Please clean the affected files."
    exit 1
fi

echo "[validator] All scripts passed integrity checks."
