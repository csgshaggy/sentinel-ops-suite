#!/bin/bash
set -e

ROOT="src"
TARGET_HOOK="useSession"
AUTH_IMPORT='import { useAuth } from "../features/auth/AuthContext.jsx";'

echo "[CLEANUP] Searching for files using $TARGET_HOOK..."

FILES=$(grep -Ril "$TARGET_HOOK" "$ROOT" || true)

if [ -z "$FILES" ]; then
  echo "[OK] No files found using $TARGET_HOOK. Nothing to patch."
  exit 0
fi

echo "[FOUND] The following files use $TARGET_HOOK:"
echo "$FILES"
echo

for f in $FILES; do
  echo "[PATCH] Processing $f"

  # Backup original
  cp "$f" "$f.bak"

  # Remove the old import
  sed -i '/useSession/d' "$f"

  # Insert the new import at the top (only if not already present)
  if ! grep -q "useAuth" "$f"; then
    sed -i "1s|^|$AUTH_IMPORT\n|" "$f"
  fi

  # Replace useSession() with useAuth()
  sed -i 's/useSession()/useAuth()/g' "$f"

  echo "[OK] Patched $f"
done

echo
echo "[DONE] All useSession references removed and migrated to useAuth."
echo "Backups created with .bak extension."
