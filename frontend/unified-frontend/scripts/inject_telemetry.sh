#!/usr/bin/env bash
set -euo pipefail

ROOT="src"
TELEMETRY_IMPORT='import { Telemetry } from "../telemetry/telemetry";'

# Files requiring telemetry injection
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

# Optional files (only patch if they exist)
OPTIONAL_FILES=(
  "components/Sidebar.jsx"
  "components/TopBar.jsx"
  "App.jsx"
)

echo "=== Sentinel Ops Telemetry Injection Script ==="
echo "Working directory: $(pwd)"
echo

inject_import() {
  local file="$1"

  # Skip if import already exists
  if grep -q "Telemetry" "$file"; then
    echo "[SKIP] Import already present: $file"
    return
  fi

  # Insert import after first existing import
  awk -v import="$TELEMETRY_IMPORT" '
    NR==1 && $0 ~ /^import/ {
      print $0
      print import
      next
    }
    { print }
  ' "$file" > "$file.tmp"

  mv "$file.tmp" "$file"
  echo "[OK] Added telemetry import → $file"
}

inject_call() {
  local file="$1"
  local anchor="$2"
  local call="$3"

  # Skip if call already exists
  if grep -q "$call" "$file"; then
    echo "[SKIP] Telemetry call already present: $file"
    return
  fi

  # Insert call after anchor
  awk -v anchor="$anchor" -v call="$call" '
    index($0, anchor) {
      print $0
      print "    " call
      next
    }
    { print }
  ' "$file" > "$file.tmp"

  mv "$file.tmp" "$file"
  echo "[OK] Inserted telemetry call → $file"
}

echo "=== Injecting telemetry imports ==="
for f in "${FILES[@]}"; do
  full="$ROOT/$f"
  if [[ -f "$full" ]]; then
    inject_import "$full"
  else
    echo "[MISS] File not found: $full"
  fi
done

for f in "${OPTIONAL_FILES[@]}"; do
  full="$ROOT/$f"
  if [[ -f "$full" ]]; then
    inject_import "$full"
  fi
done

echo
echo "=== Injecting telemetry calls ==="

# SessionManager.jsx
inject_call "$ROOT/components/SessionManager.jsx" \
  "catch (err)" \
  'Telemetry.session("restore.failure", { error: err.message }, "SessionManager");'

# useHeartbeat.js
inject_call "$ROOT/hooks/useHeartbeat.js" \
  "catch (err)" \
  'Telemetry.heartbeat("failure", { error: err.message }, "useHeartbeat");'

# useSession.js
inject_call "$ROOT/hooks/useSession.js" \
  "catch (err)" \
  'Telemetry.session("restore.failure", { error: err.message }, "useSession");'

# apiClient.js (request)
inject_call "$ROOT/api/apiClient.js" \
  "axios.interceptors.request.use" \
  'Telemetry.api("request.failure", { error: err?.message }, "apiClient");'

# apiClient.js (response)
inject_call "$ROOT/api/apiClient.js" \
  "axios.interceptors.response.use" \
  'Telemetry.api("response.failure", { status: error?.response?.status }, "apiClient");'

# AuthContext.jsx
inject_call "$ROOT/features/auth/AuthContext.jsx" \
  "catch (err)" \
  'Telemetry.sec("login.failure", { error: err.message }, "AuthContext");'

# Dashboard.jsx
inject_call "$ROOT/pages/Dashboard.jsx" \
  "useEffect" \
  'Telemetry.perf("page_load", {}, "Dashboard");'

# Preferences.jsx
inject_call "$ROOT/pages/Preferences.jsx" \
  "handleSave" \
  'Telemetry.ui("submit", { form: "preferences" }, "Preferences");'

# AvatarTab.jsx
inject_call "$ROOT/pages/Profile/components/tabs/AvatarTab.jsx" \
  "catch (err)" \
  'Telemetry.ui("submit", { action: "avatar_upload" }, "AvatarTab");'

# ApiKeysTab.jsx
inject_call "$ROOT/pages/Profile/components/tabs/ApiKeysTab.jsx" \
  "catch (err)" \
  'Telemetry.ui("click", { action: "copy_api_key" }, "ApiKeysTab");'

# LoginHistoryTab.jsx
inject_call "$ROOT/pages/Profile/components/tabs/LoginHistoryTab.jsx" \
  "catch (err)" \
  'Telemetry.ui("load", { action: "login_history" }, "LoginHistoryTab");'

echo
echo "=== Telemetry injection complete ==="
