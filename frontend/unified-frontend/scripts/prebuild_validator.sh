#!/usr/bin/env bash
set -e

echo "[VALIDATOR] Starting prebuild validation..."

###############################################
# CONFIG
###############################################
ALLOWED_EXTERNAL_DEPS=(
  react
  react-dom
  react-router-dom
  zustand
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

AUTO_FIX=${AUTO_FIX:-false}
DEBUG_RESOLUTION=${DEBUG_RESOLUTION:-false}

###############################################
# 1. Lockfile integrity check
###############################################
echo "[VALIDATOR] Checking lockfile integrity..."
npm ci --dry-run >/dev/null 2>&1
if [ $? -ne 0 ]; then
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

IMPORTS=$(grep -RhoP "(?<=from \")[^\"]+" src | sort -u)

if [ "$DEBUG_RESOLUTION" = "true" ]; then
  echo "[DEBUG] Module resolution logging enabled."
  echo "[DEBUG] Scanning imports..."
fi

for IMP in $IMPORTS; do

  ###############################################
  # DEBUG: Module resolution logging
  ###############################################
  if [ "$DEBUG_RESOLUTION" = "true" ]; then
    echo ""
    echo "[DEBUG] Import: $IMP"

    if [[ "$IMP" == .* ]]; then
      echo "[DEBUG] → Relative import (skipped resolution)"
    else
      RESOLVED_PATH=$(node -e "try { console.log(require.resolve('$IMP')); } catch (e) { process.exit(1); }" 2>/dev/null || echo "NOT_FOUND")

      if [ "$RESOLVED_PATH" = "NOT_FOUND" ]; then
        echo "[DEBUG] → Resolution FAILED"
      else
        echo "[DEBUG] → Resolved to: $RESOLVED_PATH"
      fi
    fi
  fi

  ###############################################
  # Normal dependency validation logic
  ###############################################
  if [[ "$IMP" == .* ]]; then continue; fi
  if printf '%s\n' "${ALLOWED_EXTERNAL_DEPS[@]}" | grep -qx "$IMP"; then continue; fi
  if printf '%s\n' "${VIRTUAL_MODULES[@]}" | grep -qx "$IMP"; then continue; fi
  if [[ "$IMP" == react-dom/* ]]; then continue; fi
  if [[ "$IMP" == react/jsx-runtime ]]; then continue; fi

  if [ ! -d "node_modules/$IMP" ] && [ ! -f "node_modules/$IMP" ]; then
    MISSING+=("$IMP")
  fi
done

if [ "$DEBUG_RESOLUTION" = "true" ]; then
  echo ""
  echo "[DEBUG] Module resolution logging complete."
fi

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "[VALIDATOR] Missing dependencies detected:"
  for dep in "${MISSING[@]}"; do
    echo "  - $dep"
  done

  if [ "$AUTO_FIX" = "true" ]; then
    echo "[VALIDATOR] AUTO-FIX ENABLED — installing missing dependencies..."
    for dep in "${MISSING[@]}"; do
      npm install "$dep" || true
    done
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
  PATHS=$(grep -oP "(?<=from \")[^\"]+" "$FILE" | grep "^\." || true)

  for P in $PATHS; do
    BASE="$(dirname "$FILE")/$P"

    if [ ! -e "$BASE" ] &&
       [ ! -e "$BASE.js" ] &&
       [ ! -e "$BASE.jsx" ] &&
       [ ! -e "$BASE.ts" ] &&
       [ ! -e "$BASE.tsx" ] &&
       [ ! -e "$BASE.css" ]; then
      BROKEN_IMPORTS+=("$FILE → $P")
    fi
  done
done < <(find src \( -name "*.jsx" -o -name "*.js" \) -type f)

if [ ${#BROKEN_IMPORTS[@]} -gt 0 ]; then
  echo "[VALIDATOR] ERROR: Broken relative imports detected:"
  for b in "${BROKEN_IMPORTS[@]}"; do
    echo "  - $b"
  done

  if [ "$AUTO_FIX" = "true" ]; then
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

if [ ! -f vite.config.js ] && [ ! -f vite.config.ts ]; then
  echo "[VALIDATOR] ERROR: Missing Vite config file."
  exit 1
fi

echo "[VALIDATOR] Vite config OK."


###############################################
# 5. React Router sanity check
###############################################
echo "[VALIDATOR] Checking React Router routes..."

if ! grep -R "createBrowserRouter" -n src >/dev/null 2>&1; then
  echo "[VALIDATOR] ERROR: No router definition found."
  exit 1
fi

echo "[VALIDATOR] Router OK."


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
  if [ ! -f "$COMP" ]; then
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
