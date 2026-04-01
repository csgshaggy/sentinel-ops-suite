#!/usr/bin/env bash
set -euo pipefail

SNAP_DIR=".git-snapshots"

if [[ ! -d "$SNAP_DIR" ]]; then
    echo "[ERROR] Snapshot directory '$SNAP_DIR' does not exist."
    exit 1
fi

LATEST="$(ls -1 "$SNAP_DIR" | sort | tail -n 1 || true)"
PREV="$(ls -1 "$SNAP_DIR" | sort | tail -n 2 | head -n 1 || true)"

if [[ -z "$LATEST" || -z "$PREV" || "$LATEST" == "$PREV" ]]; then
    echo "[ERROR] Not enough snapshots to diff (need at least 2)."
    exit 1
fi

LATEST_PATH="$SNAP_DIR/$LATEST"
PREV_PATH="$SNAP_DIR/$PREV"

echo "[GIT-SNAPSHOT-DIFF] Comparing:"
echo "  PREV:   $PREV_PATH"
echo "  LATEST: $LATEST_PATH"
echo

diff -u "$PREV_PATH" "$LATEST_PATH" || true
