#!/bin/bash
set -e

ROOT="src"

echo "[SCAN] Searching for incorrect avatar/profile routes..."

grep -Rin "/api/auth/profile" $ROOT || true
grep -Rin "/api/auth/profile/avatar" $ROOT || true
grep -Rin "/api/auth/avatar" $ROOT || true

echo "[PATCH] Applying fixes..."

find $ROOT -type f -exec sed -i.bak \
  -e 's|/api/auth/profile/avatar|/api/profile/avatar|g' \
  -e 's|/api/auth/profile|/api/profile|g' \
  -e 's|/api/auth/avatar/upload|/api/profile/avatar|g' \
  {} \;

echo "[DONE] Avatar/profile routes corrected."
echo "Backups created with .bak extension."
