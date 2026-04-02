#!/usr/bin/env bash
set -euo pipefail

echo "🔄 Starting repository sync..."

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_ROOT"

echo "🔍 Running pre-sync validator..."
node scripts/sync/pre-sync-validate.cjs

echo "📦 Staging tracked changes..."
git add -A

echo "📦 Auto-adding untracked files..."
# This ensures all untracked files are included in the sync
git add .

if git diff --cached --quiet; then
    echo "ℹ️ No changes to commit."
else
    COMMIT_MSG="sync: automated repository sync on $(date '+%Y-%m-%d %H:%M:%S')"
    echo "📝 Committing changes: $COMMIT_MSG"
    git commit -m "$COMMIT_MSG"
fi

echo "📥 Fetching latest from origin..."
git fetch origin main

echo "🔁 Rebasing onto origin/main..."
git rebase origin/main

echo "📤 Pushing to origin..."
git push origin HEAD

echo "📊 Running post-sync health snapshot..."
node scripts/sync/post-sync-health-snapshot.cjs

echo "🔍 Running post-sync governance checks..."
make governance

echo "✅ Sync complete, untracked files added, snapshot captured, governance validated."
