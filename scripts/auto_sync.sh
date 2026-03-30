#!/bin/bash
set -e

REPO="/home/kali/ssrf-command-console"
cd "$REPO"

# Ensure venv is active
source "$REPO/.venv/bin/activate"

# Log file
LOG="$REPO/sync.log"

echo "===== SSRF Sync Engine =====" >> "$LOG"
echo "Run: $(date)" >> "$LOG"

# 1. Validate structure
python3 scripts/structure_validator.py >> "$LOG" 2>&1 || true

# 2. Snapshot repo
python3 scripts/snapshot_repo.py >> "$LOG" 2>&1 || true

# 3. Detect drift
python3 scripts/drift_detector.py >> "$LOG" 2>&1 || true

# 4. Auto-pull
git pull --rebase origin main >> "$LOG" 2>&1 || true

# 5. Auto-add
git add -A >> "$LOG" 2>&1 || true

# 6. Auto-commit
git commit -m "Auto-sync: $(date)" >> "$LOG" 2>&1 || true

# 7. Auto-push
git push origin main >> "$LOG" 2>&1 || true

echo "Sync complete." >> "$LOG"
echo "" >> "$LOG"
