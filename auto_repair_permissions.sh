#!/usr/bin/env bash
set -euo pipefail

echo "[permissions] Auto‑repairing script permissions..."

REQUIRED_SCRIPTS=(
  "sync.sh"
  "pre_sync_validator.sh"
  "view_sync_log.sh"
  "sync_history_dashboard.sh"
  "auto_repair_permissions.sh"
)

for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [[ -f "$script" ]]; then
        if [[ ! -x "$script" ]]; then
            echo "[permissions] Fixing: $script"
            chmod +x "$script"
        fi
    fi
done

echo "[permissions] Permission repair complete."
