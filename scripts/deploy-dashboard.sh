#!/usr/bin/env bash
###############################################################################
#  deploy-dashboard.sh
#  Builds dashboard-app and deploys to /var/www/sentinel-frontend/admin
#  Usage: bash deploy-dashboard.sh
###############################################################################
set -euo pipefail

# ── Absolute Paths ──────────────────────────────────────────────────────────
APP_DIR="$HOME/sentinel-ops-suite/frontend/dashboard-app"
DEPLOY_DIR="/var/www/sentinel-frontend/admin"
BUILD_DIR="${APP_DIR}/dist"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# ── Banner ──────────────────────────────────────────────────────────────────
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         SENTINEL · Dashboard Deploy Script                 ║"
echo "║         ${TIMESTAMP}                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# ── Step 1: Validate source directory ───────────────────────────────────────
echo "[1/5] Validating source directory..."
if [[ ! -d "${APP_DIR}" ]]; then
  echo "  ✗ FATAL: App directory not found: ${APP_DIR}"
  exit 1
fi
echo "  ✓ Source directory confirmed: ${APP_DIR}"

# ── Step 2: Build ───────────────────────────────────────────────────────────
echo "[2/5] Running npm build..."
cd "${APP_DIR}"
npm run build
echo "  ✓ Build completed."

# ── Step 3: Validate build output ───────────────────────────────────────────
echo "[3/5] Validating build output..."
if [[ ! -f "${BUILD_DIR}/index.html" ]]; then
  echo "  ✗ FATAL: index.html not found in ${BUILD_DIR}"
  exit 1
fi
if [[ ! -d "${BUILD_DIR}/assets" ]]; then
  echo "  ✗ FATAL: assets directory not found in ${BUILD_DIR}"
  exit 1
fi
echo "  ✓ index.html and assets/ verified in build output."

# ── Step 4: Prepare deploy target ───────────────────────────────────────────
echo "[4/5] Preparing deploy target..."
sudo mkdir -p "${DEPLOY_DIR}/assets"
echo "  ✓ Deploy directory ready: ${DEPLOY_DIR}"

# ── Step 5: Copy artifacts (overwrite) ──────────────────────────────────────
echo "[5/5] Deploying artifacts..."
sudo cp --force "${BUILD_DIR}/index.html" "${DEPLOY_DIR}/index.html"
sudo cp --recursive --force "${BUILD_DIR}/assets/." "${DEPLOY_DIR}/assets/"
echo "  ✓ index.html deployed."
echo "  ✓ assets/ deployed (overwrite)."

# ── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════════════════════"
echo "  DEPLOY COMPLETE"
echo "  Target : ${DEPLOY_DIR}"
echo "  Time   : $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "══════════════════════════════════════════════════════════════"
exit 0
