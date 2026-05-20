#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# SSRF Command Console - Headless Sync Engine Runner
# ------------------------------------------------------------

BASE_DIR="/home/kali/ssrf-command-console"
SCRIPTS_DIR="$BASE_DIR/scripts"
LOG_DIR="$BASE_DIR/runtime/logs"
BACKEND_SCRIPT="$SCRIPTS_DIR/backend.sh"
TUI_SCRIPT="$SCRIPTS_DIR/tui.sh"
SYNC_LOG="$LOG_DIR/sync.log"

mkdir -p "$LOG_DIR"

timestamp() {
    date +"%Y-%m-%d %H:%M:%S"
}

log() {
    echo "$(timestamp) [run_all] $1" | tee -a "$SYNC_LOG"
}

log "------------------------------------------------------------"
log "Starting SSRF Sync Engine"
log "BASE_DIR=$BASE_DIR"
log "SCRIPTS_DIR=$SCRIPTS_DIR"
log "LOG_DIR=$LOG_DIR"
log "------------------------------------------------------------"

# ------------------------------------------------------------
# 1. Start backend (headless)
# ------------------------------------------------------------
if [[ -x "$BACKEND_SCRIPT" ]]; then
    log "Launching backend..."
    "$BACKEND_SCRIPT" >> "$SYNC_LOG" 2>&1 &
    BACKEND_PID=$!
    log "Backend started with PID $BACKEND_PID"
else
    log "ERROR: backend script not found or not executable: $BACKEND_SCRIPT"
    exit 10
fi

# ------------------------------------------------------------
# 2. Start TUI (optional, headless-safe)
# ------------------------------------------------------------
if [[ -x "$TUI_SCRIPT" ]]; then
    log "Launching TUI..."
    "$TUI_SCRIPT" >> "$SYNC_LOG" 2>&1 &
    TUI_PID=$!
    log "TUI started with PID $TUI_PID"
else
    log "TUI script not found or not executable: $TUI_SCRIPT (skipping)"
    TUI_PID=""
fi

# ------------------------------------------------------------
# 3. Wait for components
# ------------------------------------------------------------
log "Waiting for backend (and TUI if present) to finish..."

wait "$BACKEND_PID"
BACKEND_STATUS=$?
log "Backend exited with status $BACKEND_STATUS"

TUI_STATUS=0
if [[ -n "${TUI_PID:-}" ]]; then
    wait "$TUI_PID"
    TUI_STATUS=$?
    log "TUI exited with status $TUI_STATUS"
else
    log "No TUI process to wait for."
fi

# ------------------------------------------------------------
# 4. Final status evaluation
# ------------------------------------------------------------
if [[ $BACKEND_STATUS -ne 0 || $TUI_STATUS -ne 0 ]]; then
    log "One or more components failed. Sync engine exiting with error."
    exit 20
fi

log "Sync engine completed successfully."
exit 0
