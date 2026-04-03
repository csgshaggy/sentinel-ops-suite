#!/usr/bin/env bash
set -euo pipefail

echo "🔄 Running sync.sh..."

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$REPO_ROOT"

# ----------------------------------------
# 1. Pre-sync validator (correct path)
# ----------------------------------------
echo "🔍 Running pre-sync validator (sync.sh)..."
node "$SCRIPT_DIR/pre-sync-validate.mjs"

# ----------------------------------------
# 2. Git pull (if repo exists)
# ----------------------------------------
if [ -d "$REPO_ROOT/.git" ]; then
    echo "📥 Pulling latest changes..."
    git pull --rebase
else
    echo "⚠️ No .git directory found — skipping git pull."
fi

# ----------------------------------------
# 3. Submodules (if present)
# ----------------------------------------
if [ -f "$REPO_ROOT/.gitmodules" ]; then
    echo "📦 Updating submodules..."
    git submodule update --init --recursive
else
    echo "ℹ️ No submodules detected — skipping."
fi

# ----------------------------------------
# 4. Optional: dependency refresh hooks
# ----------------------------------------
if [ -f "$REPO_ROOT/scripts/sync/post-sync.sh" ]; then
    echo "🔧 Running post-sync hook..."
    bash "$REPO_ROOT/scripts/sync/post-sync.sh"
else
    echo "ℹ️ No post-sync hook found — skipping."
fi

echo "✅ sync.sh complete."
