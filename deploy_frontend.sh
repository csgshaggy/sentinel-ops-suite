#!/bin/bash
set -e

echo "=== Sentinel Ops Frontend Deployment (unified-frontend) ==="

FRONTEND_DIR="$HOME/sentinel-ops-suite/frontend/unified-frontend"
WEBROOT="/var/www/sentinel-ops-frontend"

echo "[1/6] Navigating to frontend directory..."
cd "$FRONTEND_DIR"

echo "[2/6] Installing dependencies..."
npm install --silent

echo "[3/6] Building production bundle..."
npm run build

echo "[4/6] Syncing dist/ to web root..."
sudo rm -rf "$WEBROOT/assets"
sudo cp -r dist/* "$WEBROOT/"

echo "[5/6] Verifying favicon + manifest..."
for f in favicon.ico favicon.png apple-touch-icon.png site.webmanifest; do
    if [ -f "$WEBROOT/$f" ]; then
        echo "  ✔ $f found"
    else
        echo "  ✘ $f missing"
    fi
done

echo "[6/6] Reloading NGINX..."
sudo nginx -t && sudo systemctl reload nginx

echo "=== Deployment Complete ==="
