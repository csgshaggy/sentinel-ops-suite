#!/usr/bin/env bash

set -e

echo "[PATCH] Fixing incorrect 'from auth.models' imports..."

FILES=(
  "app/auth/router.py"
  "app/dependencies/auth.py"
  "app/routers/admin.py"
  "app/routers/users.py"
  "app/routers/session_status.py"
  "app/utils/sessions.py"
)

for f in "${FILES[@]}"; do
  if grep -q "from auth.models" "$f"; then
    echo "[PATCH] Updating $f"
    sed -i 's/from auth.models/from app.auth.models/g' "$f"
  else
    echo "[SKIP] $f already correct"
  fi
done

echo "[DONE] Import paths corrected."
