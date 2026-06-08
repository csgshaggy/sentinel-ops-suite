#!/bin/bash

set -e

ROOT="src"

echo "🧹 Starting cleanup of old session system..."
echo ""

# ------------------------------------------------------------
# 1. Remove all .bak files
# ------------------------------------------------------------
echo "🗑  Removing .bak backup files..."
find "$ROOT" -name "*.bak" -print -delete || true
echo "✔ Backup files removed."
echo ""

# ------------------------------------------------------------
# 2. Remove old SessionProvider.jsx if it exists
# ------------------------------------------------------------
SESSION_PROVIDER="$ROOT/context/SessionProvider.jsx"

if [ -f "$SESSION_PROVIDER" ]; then
  echo "🗑  Removing old SessionProvider.jsx..."
  rm "$SESSION_PROVIDER"
  echo "✔ Removed: $SESSION_PROVIDER"
else
  echo "✔ No SessionProvider.jsx found."
fi

# Remove backup if present
if [ -f "$SESSION_PROVIDER.bak" ]; then
  echo "🗑  Removing SessionProvider.jsx.bak..."
  rm "$SESSION_PROVIDER.bak"
  echo "✔ Removed: $SESSION_PROVIDER.bak"
fi

echo ""

# ------------------------------------------------------------
# 3. Locate verification script reliably
# ------------------------------------------------------------
VERIFY_SCRIPT="$(realpath ~/sentinel-ops-suite/scripts/verify-session-context.sh)"

echo "🔍 Looking for verification script at:"
echo "    $VERIFY_SCRIPT"
echo ""

if [ -f "$VERIFY_SCRIPT" ]; then
  echo "🔍 Running verification script..."
  bash "$VERIFY_SCRIPT"
else
  echo "⚠️  Verification script not found."
fi

echo ""
echo "🎉 Cleanup complete!"
