#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"

TARGETS=(
  "scripts/preflight/legacy_preflight.py"
  "scripts/preflight/preflight_old.cjs"
  "scripts/preflight/sync-check.sh"
  "scripts/preflight/preflight-utils.js"
)

for f in "${TARGETS[@]}"; do
  abs="$ROOT/$f"
  if [ -f "$abs" ]; then
    rm -f "$abs"
  fi
done
