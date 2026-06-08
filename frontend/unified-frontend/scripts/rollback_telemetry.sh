#!/usr/bin/env bash
set -euo pipefail

ROOT="src"

echo "=== Sentinel Ops Telemetry Rollback Script ==="
echo "Working directory: $(pwd)"
echo

# Files that were patched
FILES=(
  "components/SessionManager.jsx"
  "hooks/useHeartbeat.js"
  "hooks/useSession.js"
  "api/apiClient.js"
  "features/auth/AuthContext.jsx"
  "pages/Dashboard.jsx"
  "pages/Preferences.jsx"
  "pages/Profile/components/tabs/AvatarTab.jsx"
  "pages/Profile/components/tabs/ApiKeysTab.jsx"
  "pages/Profile/components/tabs/LoginHistoryTab.jsx"
)

OPTIONAL_FILES=(
  "components/Sidebar.jsx"
  "components/TopBar.jsx"
  "App.jsx"
)

remove_import() {
  local file="$1"

  if grep -q "import { Telemetry" "$file"; then
    sed -i.bak '/import { Telemetry/d' "$file"
    echo "[OK] Removed telemetry import → $file"
  else
    echo "[SKIP] No telemetry import found: $file"
  fi
}

remove_calls() {
  local file="$1"

  # Remove any line containing Telemetry.<family>(
  if grep -q "Telemetry\." "$file"; then
    sed -i.bak '/Telemetry\./d' "$file"
    echo "[OK] Removed telemetry calls → $file"
  else
    echo "[SKIP] No telemetry calls found: $file"
  fi
}

echo "=== Removing telemetry imports ==="
for f in "${FILES[@]}"; do
  full="$ROOT/$f"
  if [[ -f "$full" ]]; then
    remove_import "$full"
  else
    echo "[MISS] File not found: $full"
  fi
done

for f in "${OPTIONAL_FILES[@]}"; do
  full="$ROOT/$f"
  if [[ -f "$full" ]]; then
    remove_import "$full"
  fi
done

echo
echo "=== Removing telemetry calls ==="
for f in "${FILES[@]}"; do
  full="$ROOT/$f"
  if [[ -f "$full" ]]; then
    remove_calls "$full"
  fi
done

for f in "${OPTIONAL_FILES[@]}"; do
  full="$ROOT/$f"
  if [[ -f "$full" ]]; then
    remove_calls "$full"
  fi
done

echo
echo "=== Rollback complete ==="
echo "Backup copies (*.bak) created for safety."
