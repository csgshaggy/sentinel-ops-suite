#!/usr/bin/env bash
set -e

# Sentinel Ops Suite — Sync Summary Generator
# Produces a timestamped summary of the last sync event.

ROOT_DIR="$(dirname "$0")"
SUMMARY_FILE="$ROOT_DIR/sync_summary.log"

TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
LAST_COMMIT="$(git log -1 --pretty=format:'%h - %s (%an)')"

echo "📝 Generating sync summary..."

{
    echo "------------------------------------------------------------"
    echo "Sync completed: $TIMESTAMP"
    echo "Branch: $BRANCH"
    echo "Last commit: $LAST_COMMIT"
    echo "------------------------------------------------------------"
    echo ""
} >> "$SUMMARY_FILE"

echo "✅ Sync summary written to: $SUMMARY_FILE"
