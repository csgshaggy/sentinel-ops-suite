#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/home/kali/ssrf-command-console"
LOG_DIR="$BASE_DIR/runtime/logs"
BACKEND_LOG="$LOG_DIR/backend.log"

mkdir -p "$LOG_DIR"

timestamp() {
    date +"%Y-%m-%d %H:%M:%S"
}

log() {
    echo "$(timestamp) [backend] $1" | tee -a "$BACKEND_LOG"
}

log "------------------------------------------------------------"
log "Starting backend sync pipeline"
log "BASE_DIR=$BASE_DIR"
log "------------------------------------------------------------"

cd "$BASE_DIR"

# ------------------------------------------------------------
# BACKEND PIPELINE
# Replace this block with your real backend/sync steps.
# Keep it non-interactive and headless-safe.
# ------------------------------------------------------------

# Example skeleton (safe to keep as-is until you customize):
if command -v git >/dev/null 2>&1; then
    log "Running git status (dry check)..."
    git status -sb >> "$BACKEND_LOG" 2>&1 || log "git status reported non-zero exit (continuing)."
else
    log "git not found in PATH (skipping git checks)."
fi

# Example placeholder for tests / sync:
# log "Running backend tests..."
# ./scripts/run_tests.sh >> "$BACKEND_LOG" 2>&1

# log "Running sync job..."
# ./scripts/sync_job.sh >> "$BACKEND_LOG" 2>&1

log "Backend sync pipeline completed successfully."
exit 0
