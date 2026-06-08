#!/usr/bin/env bash
set -euo pipefail

FRONTEND_DIR="$HOME/sentinel-ops-suite/frontend/unified-frontend"
SRC_DIR="$FRONTEND_DIR/src"

FIX_MODE="${1:-}"

echo "== Frontend validation: 1.3–1.5 =="
echo "Scanning directory: $SRC_DIR"
echo "Fix mode: ${FIX_MODE:-no}"

# ---------------------------------------------------------
# 1.3 — Legacy patterns
# ---------------------------------------------------------
echo "[1.3] Scanning for legacy auth/session symbols..."

LEGACY_PATTERNS=(
  "api/auth.js"
  "restoreSession"
  "pendingLoginToken"
  "mfaPending"
  "hasRestoredOnce"
  "session-status"
)

LEGACY_HITS=0

for pattern in "${LEGACY_PATTERNS[@]}"; do
  if grep -RIn "$pattern" "$SRC_DIR" >/dev/null 2>&1; then
    echo "!! Found legacy pattern: $pattern"
    LEGACY_HITS=1

    if [ "$FIX_MODE" = "--fix" ]; then
      echo "   → Removing pattern '$pattern' from source..."
      grep -RIl "$pattern" "$SRC_DIR" | while read -r file; do
        safe_pattern=$(printf '%s\n' "$pattern" | sed 's/[\/&]/\\&/g')
        sed -i "s|$safe_pattern||g" "$file"
      done
    fi
  fi
done

if [ "$LEGACY_HITS" -ne 0 ] && [ "$FIX_MODE" != "--fix" ]; then
  echo "✖ 1.3 FAILED: legacy references still present."
  echo "Run with:  ./validate_frontend.sh --fix"
  exit 1
fi

echo "✔ 1.3 PASSED: no legacy references found."


# ---------------------------------------------------------
# 1.4 — Legacy files
# ---------------------------------------------------------
echo "[1.4] Checking for legacy files..."

LEGACY_FILES=(
  "$SRC_DIR/api/auth.js"
  "$SRC_DIR/features/auth/legacy"
  "$SRC_DIR/features/auth/RestoreSession.jsx"
  "$SRC_DIR/features/auth/SessionStatusPoller.jsx"
)

LEGACY_FILES_FOUND=0

for f in "${LEGACY_FILES[@]}"; do
  if [ -e "$f" ]; then
    echo "!! Legacy file still exists: $f"
    LEGACY_FILES_FOUND=1

    if [ "$FIX_MODE" = "--fix" ]; then
      echo "   → Removing legacy file: $f"
      rm -rf "$f"
    fi
  fi
done

if [ "$LEGACY_FILES_FOUND" -ne 0 ] && [ "$FIX_MODE" != "--fix" ]; then
  echo "✖ 1.4 FAILED: legacy files still present."
  echo "Run with:  ./validate_frontend.sh --fix"
  exit 1
fi

echo "✔ 1.4 PASSED: no legacy files found."


# ---------------------------------------------------------
# 1.5 — Route drift
# ---------------------------------------------------------
echo "[1.5] Checking for route drift..."

ALLOWED_ROUTES=(
  "/login"
  "/mfa"
  "/dashboard"
  "/security"
  "/admin/users"
  "/admin/audit-logs"
)

ALL_ROUTES_RAW=$(grep -Rho "\"/[a-zA-Z0-9/_-]\+\"" "$SRC_DIR" || true)
ALL_ROUTES=$(printf "%s\n" "$ALL_ROUTES_RAW" | sed 's/"//g' | sort -u)

echo "Detected route-like strings:"
printf "  %s\n" $ALL_ROUTES

ROUTE_DRIFT=0

for r in $ALL_ROUTES; do
  ALLOWED=0
  for ar in "${ALLOWED_ROUTES[@]}"; do
    if [ "$r" = "$ar" ]; then
      ALLOWED=1
      break
    fi
  done

  if [ "$ALLOWED" -eq 0 ]; then
    echo "!! Route not in allowlist: $r"
    ROUTE_DRIFT=1

    if [ "$FIX_MODE" = "--fix" ]; then
      echo "   → Removing drifted route '$r' from source..."
      grep -RIl "$r" "$SRC_DIR" | while read -r file; do
        safe_route=$(printf '%s\n' "$r" | sed 's/[\/&]/\\&/g')
        sed -i "s|$safe_route||g" "$file"
      done
    fi
  fi
done

if [ "$ROUTE_DRIFT" -ne 0 ] && [ "$FIX_MODE" != "--fix" ]; then
  echo "✖ 1.5 FAILED: route drift detected."
  echo "Run with:  ./validate_frontend.sh --fix"
  exit 1
fi

echo "✔ 1.5 PASSED: no route drift."

echo "== Frontend validation 1.3–1.5 COMPLETE =="
