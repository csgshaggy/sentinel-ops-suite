#!/usr/bin/env bash
set -euo pipefail

# -------- CONFIG --------
SOURCE_DIR="/opt/operator_console/backend"
SNAPSHOT_ROOT="/opt/operator_console/backups/backend_snapshots"
LOG_FILE="/var/log/backend_autosync.log"
MAX_SNAPSHOTS=7
HASH_ALGO="sha256sum"
# ------------------------

timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

log() {
  local level="$1"; shift
  echo "$(timestamp) [$level] $*" | tee -a "$LOG_FILE"
}

fail() {
  log "ERROR" "$*"
  exit 1
}

# -------- PRECHECKS --------
[ -d "$SOURCE_DIR" ] || fail "Source directory missing: $SOURCE_DIR"
mkdir -p "$SNAPSHOT_ROOT" || fail "Unable to create snapshot root: $SNAPSHOT_ROOT"
touch "$LOG_FILE" || fail "Unable to touch log file: $LOG_FILE"

log "INFO" "=== Autosync run started ==="
log "INFO" "Source: $SOURCE_DIR"
log "INFO" "Snapshot root: $SNAPSHOT_ROOT"

# -------- SNAPSHOT PREP --------
RUN_ID="$(date +'%Y%m%d_%H%M%S')"
SNAPSHOT_DIR="$SNAPSHOT_ROOT/snapshot_$RUN_ID"
TMP_DIR="$SNAPSHOT_DIR.tmp"

mkdir -p "$TMP_DIR"

log "INFO" "Syncing to temp snapshot: $TMP_DIR"

# Use rsync for efficient, consistent copy
rsync -a --delete \
  --exclude=".git" \
  --exclude="__pycache__" \
  "$SOURCE_DIR"/ "$TMP_DIR"/

log "INFO" "Sync complete. Computing integrity manifest."

# -------- INTEGRITY MANIFEST --------
pushd "$TMP_DIR" >/dev/null

MANIFEST_FILE="MANIFEST.${HASH_ALGO}.txt"
# shellcheck disable=SC2044
for f in $(find . -type f | sed 's|^\./||'); do
  $HASH_ALGO "$f" >> "$MANIFEST_FILE"
done

popd >/dev/null

log "INFO" "Manifest created: $TMP_DIR/$MANIFEST_FILE"

# Atomically move temp dir to final snapshot dir
mv "$TMP_DIR" "$SNAPSHOT_DIR"
log "INFO" "Snapshot finalized: $SNAPSHOT_DIR"

# -------- SNAPSHOT ROTATION --------
log "INFO" "Running snapshot rotation (max $MAX_SNAPSHOTS)."

SNAPSHOTS=($(ls -1 "$SNAPSHOT_ROOT" | sort))
COUNT=${#SNAPSHOTS[@]}

if (( COUNT > MAX_SNAPSHOTS )); then
  TO_DELETE=$(( COUNT - MAX_SNAPSHOTS ))
  for (( i=0; i<TO_DELETE; i++ )); do
    OLD="$SNAPSHOT_ROOT/${SNAPSHOTS[$i]}"
    log "INFO" "Pruning old snapshot: $OLD"
    rm -rf "$OLD"
  done
else
  log "INFO" "No rotation needed. Current snapshots: $COUNT"
fi

log "INFO" "=== Autosync run completed successfully ==="
exit 0
