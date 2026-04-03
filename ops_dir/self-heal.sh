#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "🩺 Sentinel Ops Suite — Self-Heal Run"
echo "📅 $(date -Iseconds)"

# 1. Git integrity
echo "🔍 Checking git status..."
if ! git status >/dev/null 2>&1; then
  echo "❌ Git repository appears broken."
  exit 1
fi

# 2. Ensure core directories exist
for d in backend frontend scripts scripts/sync scripts/ops; do
  if [ ! -d "$d" ]; then
    echo "⚠️ Missing directory: $d"
  fi
done

# 3. Run Makefile validator (if present)
if [ -f "scripts/ops/validate-makefile.cjs" ]; then
  echo "🔎 Running Makefile validator..."
  if ! node scripts/ops/validate-makefile.cjs; then
    echo "❌ Makefile validation failed."
    exit 1
  fi
fi

# 4. Run repo structure checksum
if [ -f "scripts/ops/repo-structure-checksum.cjs" ]; then
  echo "🔐 Updating repo structure checksum..."
  node scripts/ops/repo-structure-checksum.cjs
fi

echo "✅ Self-heal run complete."
