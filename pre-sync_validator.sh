#!/usr/bin/env bash
set -euo pipefail

echo "=== Pre‑Sync Validator ==="

# ------------------------------------------------------------
# REQUIRED SCRIPTS
# ------------------------------------------------------------
REQUIRED_SCRIPTS=(
  "sync.sh"
  "pre_sync_validator.sh"
  "view_sync_log.sh"
  "sync_history_dashboard.sh"
)

echo "[CHECK] Verifying required scripts..."

for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [[ ! -f "./$script" ]]; then
        echo "[ERROR] Missing required script: $script"
        echo "        Run: make update-makefile-reference or restore the file."
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
# EXISTING VALIDATION LOGIC
# ------------------------------------------------------------

# 1. Ensure sync.sh exists
if [[ ! -f "./sync.sh" ]]; then
    echo "[ERROR] sync.sh not found in repo root."
    exit 1
fi

# 2. Ensure sync.sh is executable
if [[ ! -x "./sync.sh" ]]; then
    echo "[ERROR] sync.sh is not executable. Run: chmod +x sync.sh"
    exit 1
fi

# 3. Ensure no ongoing rebase
if [[ -d ".git/rebase-apply" || -d ".git/rebase-merge" ]]; then
    echo "[ERROR] Rebase in progress. Resolve it before syncing."
    exit 1
fi

# 4. Ensure no merge conflicts
if git ls-files -u | grep -q .; then
    echo "[ERROR] Merge conflicts detected. Resolve them before syncing."
    exit 1
fi

# 5. Ensure working tree is clean-ish
if [[ -n "$(git status --porcelain)" ]]; then
    echo "[WARNING] Working tree has changes."
    echo "This is allowed, but sync.sh will commit them."
fi

echo "=== Pre‑Sync Validator Passed ==="
