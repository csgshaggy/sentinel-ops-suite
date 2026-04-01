#!/usr/bin/env bash
set -euo pipefail

SNAP_DIR=".git-snapshots"
TIMESTAMP="$(date +"%Y-%m-%d_%H-%M-%S")"
OUT="$SNAP_DIR/snapshot_$TIMESTAMP.txt"

mkdir -p "$SNAP_DIR"

{
    echo "=== Git Metadata Snapshot ==="
    echo "Timestamp: $TIMESTAMP"
    echo

    echo "--- HEAD ---"
    git rev-parse HEAD
    git show --no-patch --pretty=fuller HEAD
    echo

    echo "--- Branches ---"
    git branch -vv
    echo

    echo "--- Reflog (HEAD) ---"
    git reflog --date=iso
    echo

    echo "--- Commit Graph Summary ---"
    git log --graph --oneline --decorate --max-count=50
    echo

    echo "--- Object Count ---"
    git count-objects -vH
    echo

    echo "--- Packfiles ---"
    ls -lh .git/objects/pack || true
    echo

    echo "--- FSCK (non-fatal) ---"
    git fsck --no-progress --full || true
    echo

    echo "--- Diffstat (last 24h) ---"
    git log --since="24 hours ago" --stat || true
    echo

} > "$OUT"

echo "[OK] Snapshot written to $OUT"
