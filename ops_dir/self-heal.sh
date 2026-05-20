#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🩺 Sentinel Ops Suite — Self-Heal Run"
date +"📅 %Y-%m-%dT%H:%M:%S%z"

cd "$REPO_ROOT"

echo "🔍 Checking git status..."
git status --short || true

echo "🔎 Running Makefile validator..."
if ! node scripts/ops/validate-makefile.mjs; then
    echo "❌ Makefile validation failed."
    exit 1
fi

echo "🔎 Running structure validator..."
if [ -f scripts/ops/validate-structure.mjs ]; then
    if ! node scripts/ops/validate-structure.mjs; then
        echo "❌ Structure validation failed."
        exit 1
    fi
else
    echo "ℹ️ No structure validator found — skipping."
fi

echo "✅ Self-heal checks complete."
