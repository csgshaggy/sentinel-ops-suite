#!/bin/bash
set -euo pipefail

ROOT="src"

echo "[SCAN] Current bad routes and assets (if any):"
grep -Rin "/api/profile/avatar" "$ROOT" || true
grep -Rin "/api/profile" "$ROOT" || true
grep -Rin "default-avatar.png" "$ROOT" || true

echo
echo "[PATCH] Rewriting profile + avatar routes and default avatar path..."

# Only touch JS/JSX source files
find "$ROOT" \( -name "*.js" -o -name "*.jsx" \) -print0 | while IFS= read -r -d '' FILE; do
  # Create a one-time backup per file
  if [[ ! -f "${FILE}.bak" ]]; then
    cp "$FILE" "${FILE}.bak"
  fi

  # 1) Fix avatar upload route (more specific first)
  sed -i \
    -e 's|/api/profile/avatar|/profile/avatar|g' \
    "$FILE"

  # 2) Fix profile fetch route
  sed -i \
    -e 's|/api/profile|/profile|g' \
    "$FILE"

  # 3) Fix default avatar asset path
  sed -i \
    -e 's|/default-avatar.png|/static/avatars/default-avatar.png|g' \
    -e 's|default-avatar.png|/static/avatars/default-avatar.png|g' \
    "$FILE"
done

echo
echo "[VERIFY] Post-patch occurrences (should be empty or intentional):"
grep -Rin "/api/profile/avatar" "$ROOT" || true
grep -Rin "/api/profile" "$ROOT" || true
grep -Rin "default-avatar.png" "$ROOT" || true

echo
echo "[DONE] Profile + avatar routes and default avatar path patched."
echo "Backups created as *.bak next to each modified file."
