#!/usr/bin/env bash
set -e

echo "📁 Moving to repo root..."
cd "$(dirname "$0")"

echo "🧹 Staging all changes..."
git add -A

if ! git diff --cached --quiet; then
    echo "📝 Committing staged changes..."
    git commit -m "sync: local changes before pull"
else
    echo "ℹ️ No local changes to commit."
fi

echo "🔍 Running MFA structure validator (pre‑commit)..."
if ! make validate-mfa; then
    echo ""
    echo "❌ Commit blocked: MFA structure validation failed."
    echo "   Fix the issues above and try committing again."
    exit 1
fi

echo "🔄 Pulling latest changes with rebase..."
git pull --rebase origin main || {
    echo "❗ Rebase failed. Resolve conflicts and run sync again."
    exit 1
}

echo "🧪 Running repo-health..."
if ! make repo-health; then
    echo ""
    echo "❌ Repo-health failed. Fix issues and run sync again."
    exit 1
fi

echo "🚀 Pushing clean, validated state..."
git push origin main

echo "📄 Generating sync summary..."
if [ -f sync_summary.sh ]; then
    ./sync_summary.sh
else
    echo "ℹ️ No sync_summary.sh found. Skipping summary."
fi

echo "✅ Repository sync complete."
