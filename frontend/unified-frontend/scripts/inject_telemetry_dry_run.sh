#!/usr/bin/env bash
set -euo pipefail

ROOT="src"
TELEMETRY_IMPORT='import { Telemetry } from "../telemetry/telemetry";'

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

echo "=== DRY RUN: Telemetry Injection ==="
echo "No files will be modified."
echo

dry_import_check() {
  local file="$1"

  if grep -q "Telemetry" "$file"; then
    echo "[SKIP] Import already present: $file"
  else
    echo "[ADD] Would insert telemetry import → $file"
  fi
}

dry_call_check() {
  local file="$1"
  local call="$2"

  if grep -q "$call" "$file"; then
    echo "[SKIP] Telemetry call already present: $file"
  else
    echo "[ADD] Would insert telemetry call → $file"
  fi
}

echo "=== Checking telemetry imports ==="
for f in "${FILES[@]}"; do
  full="$ROOT/$f"
  if [[ -f "$full" ]]; then
    dry_import_check "$full"
  else
    echo "[MISS] File not found: $full"
  fi
done

for f in "${OPTIONAL_FILES[@]}"; do
  full="$ROOT/$f"
  if [[ -f "$full" ]]; then
    dry_import_check "$full"
  fi
done

echo
echo "=== Checking telemetry call insertion points ==="

dry_call_check "$ROOT/components/SessionManager.jsx" \
  'Telemetry.session("restore.failure"'

dry_call_check "$ROOT/hooks/useHeartbeat.js" \
  'Telemetry.heartbeat("failure"'

dry_call_check "$ROOT/hooks/useSession.js" \
  'Telemetry.session("restore.failure"'

dry_call_check "$ROOT/api/apiClient.js" \
  'Telemetry.api("request.failure"'

dry_call_check "$ROOT/api/apiClient.js" \
  'Telemetry.api("response.failure"'

dry_call_check "$ROOT/features/auth/AuthContext.jsx" \
  'Telemetry.sec("login.failure"'

dry_call_check "$ROOT/pages/Dashboard.jsx" \
  'Telemetry.perf("page_load"'

dry_call_check "$ROOT/pages/Preferences.jsx" \
  'Telemetry.ui("submit"'

dry_call_check "$ROOT/pages/Profile/components/tabs/AvatarTab.jsx" \
  'Telemetry.ui("submit", { action: "avatar_upload"'

dry_call_check "$ROOT/pages/Profile/components/tabs/ApiKeysTab.jsx" \
  'Telemetry.ui("click", { action: "copy_api_key"'

dry_call_check "$ROOT/pages/Profile/components/tabs/LoginHistoryTab.jsx" \
  'Telemetry.ui("load", { action: "login_history"'

echo
echo "=== DRY RUN COMPLETE ==="
