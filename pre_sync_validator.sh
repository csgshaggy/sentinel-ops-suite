#!/usr/bin/env bash
set -euo pipefail

echo "=== Pre‑Sync Validator ==="

# ------------------------------------------------------------
# AUTO‑REPAIR PERMISSIONS (Item #5)
# ------------------------------------------------------------
if [[ -f "./auto_repair_permissions.sh" ]]; then
    ./auto_repair_permissions.sh
else
    echo "[WARNING] auto_repair_permissions.sh missing — cannot auto‑repair permissions."
fi


# ------------------------------------------------------------
# REQUIRED SCRIPTS (Item #4)
# ------------------------------------------------------------
REQUIRED_SCRIPTS=(
  "sync.sh"
  "pre_sync_validator.sh"
  "view_sync_log.sh"
  "sync_history_dashboard.sh"
  "auto_repair_permissions.sh"
)

echo "[CHECK] Verifying required scripts..."

for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [[ ! -f "./$script" ]]; then
        echo "[ERROR] Missing required script: $script"
        echo "        Restore the file or run: make update-makefile-reference"
        exit 1
    fi

    if [[ ! -x "./$script" ]]; then
        echo "[WARNING] Script not executable: $script"
        echo "         Fixing permissions..."
        chmod +x "./$script"
    fi
done

echo "[OK] All required scripts present."


# ------------------------------------------------------------
# VALIDATE SYNC.SH
# ------------------------------------------------------------
if [[ ! -f "./sync.sh" ]]; then
    echo "[ERROR] sync.sh not found in repo root."
    exit 1
fi

if [[ ! -x "./sync.sh" ]]; then
    echo "[ERROR] sync.sh is not executable. Run: chmod +x sync.sh"
    exit 1
fi


# ------------------------------------------------------------
# GIT STATE VALIDATION
# ------------------------------------------------------------

# 1. Ensure no rebase in progress
if [[ -d ".git/rebase-apply" || -d ".git/rebase-merge" ]]; then
    echo "[ERROR] Rebase in progress. Resolve it before syncing."
    exit 1
fi

# 2. Ensure no merge conflicts
if git ls-files -u | grep -q .; then
    echo "[ERROR] Merge conflicts detected. Resolve them before syncing."
    exit 1
fi

# 3. Warn if working tree has changes
if [[ -n "$(git status --porcelain)" ]]; then
    echo "[WARNING] Working tree has changes."
    echo "This is allowed, but sync.sh will commit them."
fi


# ------------------------------------------------------------
# FINAL PASS
# ------------------------------------------------------------
echo "=== Pre‑Sync Validator Passed ==="
