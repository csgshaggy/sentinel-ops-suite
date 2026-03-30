#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/home/kali/ssrf-command-console"
LOG_DIR="$BASE_DIR/runtime/logs"
TUI_LOG="$LOG_DIR/tui.log"

mkdir -p "$LOG_DIR"

timestamp() {
    date +"%Y-%m-%d %H:%M:%S"
}

log() {
    echo "$(timestamp) [tui] $1" | tee -a "$TUI_LOG"
}

log "------------------------------------------------------------"
log "Starting TUI summary run (headless-safe)"
log "BASE_DIR=$BASE_DIR"
log "------------------------------------------------------------"

cd "$BASE_DIR"

# ------------------------------------------------------------
# TUI / SUMMARY PIPELINE
# This should NOT assume an interactive terminal when run under systemd.
# Think of it as a "summary renderer" into logs.
# ------------------------------------------------------------

SYNC_LOG="$LOG_DIR/sync.log"

if [[ -f "$SYNC_LOG" ]]; then
    log "Tail of sync.log (last 50 lines):"
    tail -n 50 "$SYNC_LOG" >> "$TUI_LOG" 2>&1 || true
else
    log "No sync.log found to summarize."
fi

log "TUI summary run completed successfully."
exit 0
