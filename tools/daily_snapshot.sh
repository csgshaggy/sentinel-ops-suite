#!/usr/bin/env bash
set -euo pipefail

# Run from repo root
cd "$(dirname "$0")/.."

echo "[DAILY-SNAPSHOT] Running git-snapshot via Makefile..."
make git-snapshot
