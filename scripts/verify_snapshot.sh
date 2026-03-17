#!/usr/bin/env bash
set -euo pipefail

SNAPSHOT_DIR="${1:-}"
HASH_ALGO="sha256sum"

if [ -z "$SNAPSHOT_DIR" ] || [ ! -d "$SNAPSHOT_DIR" ]; then
  echo "Usage: $0 /path/to/snapshot_dir"
  exit 1
fi

MANIFEST_FILE="$SNAPSHOT_DIR/MANIFEST.${HASH_ALGO}.txt"

if [ ! -f "$MANIFEST_FILE" ]; then
  echo "Manifest not found: $MANIFEST_FILE"
  exit 1
fi

pushd "$SNAPSHOT_DIR" >/dev/null

echo "Verifying snapshot: $SNAPSHOT_DIR"
$HASH_ALGO -c "$(basename "$MANIFEST_FILE")"

popd >/dev/null
