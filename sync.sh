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
    echo "[PRE-COMMIT] Running format + lint + ci-precommit..."
    make format || true
    make lint || true
    make ci-precommit || true

    git commit -m "sync: local changes before rebase"
else
    echo "[INFO] No changes to commit."
fi


# ------------------------------------------------------------
# 4. REBASE ONTO ORIGIN/MAIN
# ------------------------------------------------------------
echo "[4/5] Rebasing onto origin/main..."
git pull --rebase origin main || {
    echo "[ERROR] Rebase failed — resolve conflicts and re-run sync."
    exit 1
}


# ------------------------------------------------------------
# 5. PUSH
# ------------------------------------------------------------
echo "[5/5] Pushing..."

# Pre-push CI gates
echo "[PRE-PUSH] Running Makefile self-check + CI-fast gate..."
make self-check || {
    echo "[ERROR] Makefile self-check failed."
    exit 1
}

make ci-fast || {
    echo "[ERROR] CI-fast gate failed."
    exit 1
}

git push origin main


# ------------------------------------------------------------
# SYNC SUMMARY (Item #6)
# ------------------------------------------------------------
if [[ -f "./sync_summary.sh" ]]; then
    ./sync_summary.sh | tee -a sync.log
else
    echo "[WARNING] sync_summary.sh missing — cannot generate summary."
fi


echo "=== Sync Complete ==="
