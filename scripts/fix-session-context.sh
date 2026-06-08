#!/bin/bash

set -e

ROOT="src"

echo "🔍 Searching for useSessionContext imports..."

# Find all files that import useSessionContext
FILES=$(grep -rl "useSessionContext" "$ROOT")

if [ -z "$FILES" ]; then
  echo "✅ No files found using useSessionContext. Nothing to change."
  exit 0
fi

echo "📄 Files to patch:"
echo "$FILES"
echo ""

for FILE in $FILES; do
  echo "✏️  Patching $FILE"

  # Backup original
  cp "$FILE" "$FILE.bak"

  # Replace import line
  sed -i \
    's|import { useSessionContext } from "../context/SessionProvider.jsx";|import { useAuth } from "../features/auth/AuthContext.jsx";|' \
    "$FILE"

  # Replace usage
  sed -i \
    's/useSessionContext()/useAuth()/g' \
    "$FILE"

  echo "   ✔ Updated"
done

echo ""
echo "🎉 All done!"
echo "Backups created with .bak extension."
