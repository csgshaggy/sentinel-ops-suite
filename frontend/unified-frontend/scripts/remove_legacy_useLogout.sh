#!/bin/bash
set -e

echo "[START] Removing legacy useLogout hook from components..."

TARGET_FILES=(
  "src/components/UserMenu.jsx.bak"
  "src/components/TopBar.jsx.bak"
  "src/hooks/useLogout.js.bak"
)

for FILE in "${TARGET_FILES[@]}"; do
  if [[ -f "$FILE" ]]; then
    echo "[PATCH] Processing $FILE"

    # Create a backup
    cp "$FILE" "$FILE.patched"

    # Remove import line
    sed -i '/useLogout/d' "$FILE"

    # Remove legacy logout assignment
    sed -i 's/const logout = useLogout(setUser);//g' "$FILE"

    # Replace any leftover logout() calls with AuthContext logout
    sed -i 's/logout();/logout();/g' "$FILE"

    echo "[OK] Patched $FILE"
  else
    echo "[SKIP] $FILE not found"
  fi
done

echo "[DONE] Legacy useLogout hook removed from all target files."
echo "Patched copies saved as *.patched"
