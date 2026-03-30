#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="sync.log"

if [[ ! -f "$LOG_FILE" ]]; then
  echo "[sync-history] No sync.log found."
  exit 1
fi

echo "=== Sync History Dashboard (CLI) ==="
echo

# Extract last 10 sync blocks
grep -E "=== One‑Command Sync ===|=== Sync Complete ===|^\[.*\]" "$LOG_FILE" \
  | tail -n 200 \
  | sed 's/^/  /'
