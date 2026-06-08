#!/usr/bin/env bash
set -euo pipefail

echo "[VALIDATOR] Starting prebuild validation..."

###############################################
# CONFIG
###############################################
ALLOWED_EXTERNAL_DEPS=(
  react
  react-dom
  react-router-dom
  zustand
  framer-motion
)

VIRTUAL_MODULES=(
  vitest
  vitest/config
  vite
  vite/client
  @vitejs/plugin-react
  @testing-library/react
  @testing-library/jest-dom
  @testing-library/user-event
)

NODE_BUILTINS=(
  assert
  buffer
  child_process
  crypto
  events
  fs
  http
  https
  os
  path
  stream
  url
  util
  zlib
)

AUTO_FIX="${AUTO_FIX:-false}"
DEBUG_RESOLUTION="${DEBUG_RESOLUTION:-false}"

###############################################
# HELPERS
###############################################
log_debug() {
  if [[ "$DEBUG_RESOLUTION" == "true" ]]; then
    echo "$@"
  fi
}

array_contains() {
  local needle="$1"
  shift
  local item
  for item in "$@"; do
    if [[ "$item" == "$needle" ]]; then
      return 0
    fi
  done
  return 1
}

file_or_module_exists() {
  local base="$1"

  [[ -e "$base" ]] && return 0
  [[ -f "${base}.js" ]] && return 0
  [[ -f "${base}.jsx" ]] && return 0
  [[ -f "${base}.ts" ]] && return 0
  [[ -f "${base}.tsx" ]] && return 0
  [[ -f "${base}.css" ]] && return 0

  [[ -f "${base}/index.js" ]] && return 0
  [[ -f "${base}/index.jsx" ]] && return 0
  [[ -f "${base}/index.ts" ]] && return 0
  [[ -f "${base}/index.tsx" ]] && return 0

  return 1
}

resolve_alias() {
  local imp="$1"

  # Vite-style alias: @/foo -> src/foo
  if [[ "$imp" == @/* ]]; then
    echo "src/${imp#@/}"
    return 0
  fi

  echo "$imp"
}

should_skip_import() {
  local imp="$1"

  # Skip relative imports here; they are validated later
  [[ "$imp" == .* ]] && return 0

  # Skip absolute/internal paths if you ever add them later
  [[ "$imp" == /* ]] && return 0

  # Skip node:* built-ins
  [[ "$imp" == node:* ]] && return 0

  # Skip built-in modules
  if array_contains "$imp" "${NODE_BUILTINS[@]}"; then
    return 0
  fi

  # Skip approved external deps
  if array_contains "$imp" "${ALLOWED_EXTERNAL_DEPS[@]}"; then
    return 0
  fi

  # Skip Vite/Vitest/runtime virtual modules
  if array_contains "$imp" "${VIRTUAL_MODULES[@]}"; then
    return 0
  fi

  # Common React runtime patterns
  [[ "$imp" == react-dom/* ]] && return 0
  [[ "$imp" == react/jsx-runtime ]] && return 0

  return 1
}

extract_imports() {
  # Extract import targets from:
  #   import x from "module"
  #   import x from 'module'
  #   import "module"
  #   import 'module'
  #
  # We intentionally keep this grep-based approach lightweight.
  grep -RhoP \
    "(?<=from[[:space:]]\")[^\"]+|(?<=from[[:space:]]')[^']+|(?<=import[[:space:]]\")[^\"]+|(?<=import[[:space:]]')[^']+" \
    src 2>/dev/null | sort -u
}

###############################################
# 1. Lockfile integrity check
###############################################
echo "[VALIDATOR] Checking lockfile integrity..."
if ! npm ci --dry-run >/dev/null 2>&1; then
  echo "[VALIDATOR] ERROR: Lockfile integrity check failed."
  echo "[VALIDATOR] Run: npm install"
  exit 1
fi
echo "[VALIDATOR] Lockfile OK."

###############################################
# 2. Check for missing dependencies
###############################################
echo "[VALIDATOR] Checking for missing dependencies..."

MISSING=()
mapfile -t IMPORTS < <(extract_imports)

log_debug "[DEBUG] Module resolution logging enabled."
log_debug "[DEBUG] Total unique imports found: ${#IMPORTS[@]}"

for IMP in "${IMPORTS[@]}"; do
  [[ -z "$IMP" ]] && continue

  log_debug ""
  log_debug "[DEBUG] Import: $IMP"

  if should_skip_import "$IMP"; then
    log_debug "[DEBUG] → Skipped by validator rules"
    continue
  fi

  ###############################################
  # Alias-aware dependency resolution
  ###############################################
  if [[ "$IMP" == @/* ]]; then
    RESOLVED="$(resolve_alias "$IMP")"
    log_debug "[DEBUG] → Alias resolved to: $RESOLVED"

    if ! file_or_module_exists "$RESOLVED"; then
      log_debug "[DEBUG] → Alias resolution FAILED"
      MISSING+=("$IMP")
    else
      log_debug "[DEBUG] → Alias resolution OK"
    fi

    continue
  fi

  ###############################################
  # Normal node_modules resolution
  ###############################################
  if [[ -d "node_modules/$IMP" || -f "node_modules/$IMP" ]]; then
    log_debug "[DEBUG] → Found directly in node_modules"
    continue
  fi

  # Fallback to Node's resolver for packages/subpaths
  if node -e "try { require.resolve('$IMP'); process.exit(0); } catch (e) { process.exit(1); }" >/dev/null 2>&1; then
    log_debug "[DEBUG] → Resolved via require.resolve"
    continue
  fi

  log_debug "[DEBUG] → Resolution FAILED"
  MISSING+=("$IMP")
done

if [[ "$DEBUG_RESOLUTION" == "true" ]]; then
  echo ""
  echo "[DEBUG] Module resolution logging complete."
fi

if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo "[VALIDATOR] Missing dependencies detected:"
  printf '%s\n' "${MISSING[@]}" | sort -u | while read -r dep; do
    echo "  - $dep"
  done

  if [[ "$AUTO_FIX" == "true" ]]; then
    echo "[VALIDATOR] AUTO-FIX ENABLED — installing missing dependencies..."
    while read -r dep; do
      [[ -z "$dep" ]] && continue

      # Never try to npm install aliases, relative paths, or built-ins
      if [[ "$dep" == @/* || "$dep" == .* || "$dep" == node:* ]]; then
        continue
      fi
      if array_contains "$dep" "${NODE_BUILTINS[@]}"; then
        continue
      fi

      npm install "$dep" || true
    done < <(printf '%s\n' "${MISSING[@]}" | sort -u)

    echo "[VALIDATOR] Dependencies installed. Re-running validator..."
    AUTO_FIX=false exec "$0"
  fi

  echo "[VALIDATOR] Install them before building."
  exit 1
fi

echo "[VALIDATOR] All dependencies accounted for."

###############################################
# 3. Check for broken relative imports
###############################################
echo "[VALIDATOR] Checking for broken relative imports..."

BROKEN_IMPORTS=()

while IFS= read -r FILE; do
  [[ -z "$FILE" ]] && continue

  mapfile -t PATHS < <(
    grep -oP \
      "(?<=from[[:space:]]\")[^\"]+|(?<=from[[:space:]]')[^']+" \
      "$FILE" 2>/dev/null | grep "^\." || true
  )

  for P in "${PATHS[@]}"; do
    BASE="$(dirname "$FILE")/$P"

    if ! file_or_module_exists "$BASE"; then
      BROKEN_IMPORTS+=("$FILE → $P")
    fi
  done
done < <(find src \( -name "*.jsx" -o -name "*.js" -o -name "*.ts" -o -name "*.tsx" \) -type f)

if [[ ${#BROKEN_IMPORTS[@]} -gt 0 ]]; then
  echo "[VALIDATOR] ERROR: Broken relative imports detected:"
  printf '%s\n' "${BROKEN_IMPORTS[@]}" | sort -u | while read -r b; do
    echo "  - $b"
  done

  if [[ "$AUTO_FIX" == "true" ]]; then
    echo "[VALIDATOR] AUTO-FIX ENABLED — running unified import fixer..."
    ../../scripts/fix_imports_unified.sh || true
    echo "[VALIDATOR] Re-running validator..."
    AUTO_FIX=false exec "$0"
  fi

  exit 1
fi

echo "[VALIDATOR] All relative imports valid."

###############################################
# 4. Vite config sanity check
###############################################
echo "[VALIDATOR] Checking Vite config..."

if [[ ! -f vite.config.js && ! -f vite.config.ts && ! -f vitest.config.js && ! -f vitest.config.ts ]]; then
  echo "[VALIDATOR] ERROR: Missing Vite/Vitest config file."
  echo "[VALIDATOR] Expected one of:"
  echo "  - vite.config.js"
  echo "  - vite.config.ts"
  echo "  - vitest.config.js"
  echo "  - vitest.config.ts"
  exit 1
fi

echo "[VALIDATOR] Vite config OK."

###############################################
# 5. React Router sanity check
###############################################
echo "[VALIDATOR] Checking React Router routes..."

ROUTER_OK=false

if grep -R "createBrowserRouter" -n src >/dev/null 2>&1; then
  echo "[VALIDATOR] Router OK (createBrowserRouter detected)"
  ROUTER_OK=true
fi

if [[ -f src/App.jsx ]] && grep -R "<Routes>" -n src/App.jsx >/dev/null 2>&1; then
  echo "[VALIDATOR] Router OK (App.jsx <Routes> detected)"
  ROUTER_OK=true
fi

if [[ -f src/main.jsx ]] && grep -R "BrowserRouter" -n src/main.jsx >/dev/null 2>&1; then
  echo "[VALIDATOR] Router OK (BrowserRouter detected)"
  ROUTER_OK=true
fi

if [[ "$ROUTER_OK" != "true" ]]; then
  echo "[VALIDATOR] ERROR: No valid router definition found."
  echo "[VALIDATOR] Expected either:"
  echo "  - createBrowserRouter (legacy router.jsx)"
  echo "  - <Routes> inside App.jsx (modern routing)"
  echo "  - <BrowserRouter> inside main.jsx"
  exit 1
fi

###############################################
# 6. Layout + component integrity
###############################################
echo "[VALIDATOR] Checking layout/component structure..."

REQUIRED_COMPONENTS=(
  "src/components/Sidebar.jsx"
  "src/components/Layout.jsx"
  "src/components/DashboardGrid.jsx"
  "src/components/Panel.jsx"
)

for COMP in "${REQUIRED_COMPONENTS[@]}"; do
  if [[ ! -f "$COMP" ]]; then
    echo "[VALIDATOR] ERROR: Missing required component: $COMP"
    exit 1
  fi
done

echo "[VALIDATOR] Component structure OK."

###############################################
# DONE
###############################################
echo "[VALIDATOR] Prebuild validation complete. All checks passed."
exit 0
