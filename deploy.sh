#!/usr/bin/env bash
# SentinelOps Deployment Script
# Deterministic, idempotent, operator‑grade

set -e

REPO_ROOT="/home/ubuntu/sentinel-ops-suite"
BACKEND_DIR="$REPO_ROOT/backend"
FRONTEND_DIR="$REPO_ROOT/frontend"
SERVICE_NAME="sentinel-backend.service"

echo "=== SentinelOps Deployment Started ==="

###############################################
# 1. Pull latest code
###############################################
echo "[1/6] Pulling latest code..."
cd "$REPO_ROOT"
git pull --rebase

###############################################
# 2. Backend: Install dependencies
###############################################
echo "[2/6] Updating backend dependencies..."
cd "$BACKEND_DIR"
source .venv/bin/activate
pip install -r requirements.txt

###############################################
# 3. Frontend: Build Vite SPA
###############################################
echo "[3/6] Building frontend..."
cd "$FRONTEND_DIR"
npm install
npm run build

###############################################
# 4. Restart backend service
###############################################
echo "[4/6] Restarting backend service..."
sudo systemctl daemon-reload
sudo systemctl restart "$SERVICE_NAME"

###############################################
# 5. Validate backend health
###############################################
echo "[5/6] Checking backend health..."
sleep 2
curl -sf http://127.0.0.1:8000/health || {
    echo "Backend health check failed."
    exit 1
}

###############################################
# 6. Reload NGINX
###############################################
echo "[6/6] Reloading NGINX..."
sudo nginx -t
sudo systemctl reload nginx

echo "=== SentinelOps Deployment Complete ==="
