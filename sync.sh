#!/usr/bin/env bash
set -euo pipefail

echo "=== One‑Command Sync ==="

# 1. Show repo status
echo "[1/5] Checking repo status..."
git status

# 2. Stage everything
echo "[2/5] Staging changes..."
git add -A

# 3. Commit if needed
echo "[3/5] Committing (if needed)..."
git commit -m "sync: local changes before rebase" || echo "No changes to commit."

# 4. Pull with rebase
echo "[4/5] Rebasing onto origin/main..."
git pull --rebase origin main

# 5. Push final clean state
echo "[5/5] Pushing..."
git push origin main

echo "=== Sync Complete ==="
