#!/usr/bin/env bash
set -euo pipefail

echo "=== Sentinel Ops Suite — Final Preferences Cleanup ==="

# Remove leftover PreferencesPage if still present
rm -f src/pages/admin/PreferencesPage.jsx || true

# Remove leftover imports, routes, comments
grep -RIl "Preferences" src | while read -r file; do
  echo "PATCH: $file"
  sed -i.bak '/Preferences/d' "$file"
done

grep -RIl "ThemeManager" src | while read -r file; do
  echo "PATCH: $file"
  sed -i.bak '/ThemeManager/d' "$file"
done

grep -RIl "/preferences" src | while read -r file; do
  echo "PATCH: $file"
  sed -i.bak '/\/preferences/d' "$file"
done

# Remove .bak files
find src -type f -name "*.bak" -delete

echo "=== Final cleanup complete ==="
