#!/usr/bin/env bash
set -euo pipefail

echo "=== One‑Command Sync ==="

# ------------------------------------------------------------
# AUTO‑REPAIR PERMISSIONS (Item #5)
# ------------------------------------------------------------
if [[ -f "./auto_repair_permissions.sh" ]]; then
    ./auto_repair_permissions.sh
else
    echo "[WARNING] auto_repair_permissions.sh missing — cannot auto‑repair permissions."
fi


# ------------------------------------------------------------
# PRE‑SYNC VALIDATION
# ------------------------------------------------------------
if [[ -f "./pre_sync_validator.sh" ]]; then
    ./pre_sync_validator.sh
else
    echo "[ERROR] pre_sync_validator.sh missing — cannot validate sync."
    exit 1
fi


# ------------------------------------------------------------
# 1. CHECK REPO STATUS
# ------------------------------------------------------------
echo "[1/5] Checking repo status..."
git status


# ------------------------------------------------------------
# 2. STAGE CHANGES
# ------------------------------------------------------------
echo "[2/5] Staging changes..."
git add -A || true


# ------------------------------------------------------------
# 3. COMMIT (IF NEEDED)
# ------------------------------------------------------------
echo "[3/5] Committing (if needed)..."

if ! git diff --cached --quiet; then
    echo "[PRE-COMMIT] Running format + lint..."
    make format || true
    make lint || true

    # Stage any formatter/linter changes
    git add -A

    git commit -m "sync: local changes before rebase"
else
    echo "[INFO] No changes to commit."
fi


# ------------------------------------------------------------
# 4. REBASE ONTO ORIGIN/MAIN
# ------------------------------------------------------------
echo "[4/5] Rebasing onto origin/main..."

# Stage any changes created by format/lint
git add -A

git pull --rebase origin main || {
    echo "[ERROR] Rebase failed — resolve conflicts and re-run sync."
    exit 1
}


# ------------------------------------------------------------
# 5. PUSH
# ------------------------------------------------------------
echo "[5/5] Pushing..."

echo "[PRE-PUSH] Running Makefile self-check + CI-fast gate..."
make self-check
make ci-fast

git push origin main


# ------------------------------------------------------------
# SYNC SUMMARY
# ------------------------------------------------------------
if [[ -f "./sync_summary.sh" ]]; then
    ./sync_summary.sh | tee -a sync.log
else
    echo "[WARNING] sync_summary.sh missing — cannot generate summary."
fi


# ------------------------------------------------------------
# FINAL: REATTACH HEAD TO MAIN
# ------------------------------------------------------------
echo "[FINAL] Ensuring HEAD is attached to main..."
git checkout main >/dev/null 2>&1 || true

echo "=== Sync Complete ==="
