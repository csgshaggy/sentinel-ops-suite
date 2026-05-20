#!/usr/bin/env bash
set -euo pipefail

###############################################
# Sentinel Ops Suite — Unified Frontend Deploy
# Clean, deterministic, operator‑grade
###############################################

FRONTEND_SRC="/home/ubuntu/sentinel-ops-suite/frontend/unified-frontend"
DIST_DIR="$FRONTEND_SRC/dist"
NGINX_ROOT="/var/www/sentinel-ops-frontend"

banner() {
  echo ""
  echo "============================================================"
  echo "== $1"
  echo "============================================================"
  echo ""
}

# --- 1. Validate directories ---------------------------------
banner "1. Validating directories"

if [[ ! -d "$FRONTEND_SRC" ]]; then
  echo "[ERROR] Frontend source directory not found: $FRONTEND_SRC"
  exit 1
fi

if [[ ! -d "$NGINX_ROOT" ]]; then
  echo "[ERROR] NGINX root directory not found: $NGINX_ROOT"
  exit 1
fi

echo "[OK] Directories validated."


# --- 2. Build unified frontend -------------------------------
banner "2. Building unified frontend"

cd "$FRONTEND_SRC"
npm run build

if [[ ! -d "$DIST_DIR" ]]; then
  echo "[ERROR] Build failed — dist/ directory not found."
  exit 1
fi

echo "[OK] Build completed."


# --- 3. Clean NGINX web root --------------------------------
banner "3. Cleaning NGINX web root"

sudo rm -rf "$NGINX_ROOT"/*
echo "[OK] NGINX root cleaned."


# --- 4. Deploy new build -------------------------------------
banner "4. Deploying new build to NGINX root"

sudo cp -r "$DIST_DIR"/* "$NGINX_ROOT"/
sudo chown -R www-data:www-data "$NGINX_ROOT"
sudo chmod -R 755 "$NGINX_ROOT"

echo "[OK] New build deployed."


# --- 5. Validate NGINX config --------------------------------
banner "5. Testing NGINX configuration"

if sudo nginx -t; then
  echo "[OK] NGINX config is valid."
else
  echo "[ERROR] NGINX config test failed. Deployment aborted."
  exit 1
fi


# --- 6. Reload NGINX -----------------------------------------
banner "6. Reloading NGINX"

sudo systemctl reload nginx
echo "[OK] NGINX reloaded."


# --- 7. Complete ---------------------------------------------
banner "7. Deployment complete"

echo "[SUCCESS] Unified frontend deployed cleanly."
echo ""

