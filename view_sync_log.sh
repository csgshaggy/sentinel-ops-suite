#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="sync.log"

if [[ ! -f "$LOG_FILE" ]]; then
  echo "[sync-log-viewer] No sync.log found in repo root."
  exit 1
fi

echo "=== Sync Log Viewer ==="
echo "File: $LOG_FILE"
echo

if [[ -t 1 ]]; then
  # Interactive terminal: follow with color-friendly paging
  tail -n 100 "$LOG_FILE"
else
  # Non-interactive: just dump last 100 lines
  tail -n 100 "$LOG_FILE"
fi
