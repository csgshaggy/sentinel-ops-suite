#!/usr/bin/env bash
set -euo pipefail

###############################################################
# Sentinel Ops Suite — Unified Deploy Script
# Backend + Frontend + Systemd Install (if missing)
# Deterministic, atomic, zero drift
###############################################################

ROOT="/home/ubuntu/sentinel-ops-suite"
BACKEND_DIR="$ROOT/backend"
FRONTEND_DIR="$ROOT/frontend"
WEBROOT="/var/www/sentinel-frontend"
SERVICE_NAME="uvicorn.service"
SERVICE_PATH="/etc/systemd/system/${SERVICE_NAME}"

banner() {
  echo ""
  echo "============================================================"
  echo "== $1"
  echo "============================================================"
  echo ""
}

###############################################################
# 1. Validate directories
###############################################################
banner "1. Validating directories"

if [[ ! -d "$BACKEND_DIR" ]]; then
  echo "[ERROR] Backend directory not found: $BACKEND_DIR"
  exit 1
fi

if [[ ! -d "$FRONTEND_DIR" ]]; then
  echo "[ERROR] Frontend directory not found: $FRONTEND_DIR"
  exit 1
fi

echo "[OK] Directories validated."


###############################################################
# 2. Install backend systemd service if missing
###############################################################
banner "2. Checking backend systemd service"

if [[ ! -f "$SERVICE_PATH" ]]; then
  echo "[WARN] Backend service not found. Installing..."

  sudo tee "$SERVICE_PATH" >/dev/null <<EOF
[Unit]
Description=Sentinel Ops Backend (Uvicorn)
After=network.target

[Service]
User=ubuntu
WorkingDirectory=$BACKEND_DIR
ExecStart=$BACKEND_DIR/.venv/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

  sudo systemctl daemon-reload
  sudo systemctl enable "$SERVICE_NAME"
  echo "[OK] Backend service installed."
else
  echo "[OK] Backend service already exists."
fi


###############################################################
# 3. Deploy Backend
###############################################################
banner "3. Deploying backend"

cd "$BACKEND_DIR"

# Activate venv
if [[ -f ".venv/bin/activate" ]]; then
  source .venv/bin/activate
else
  echo "[ERROR] Python venv missing at $BACKEND_DIR/.venv"
  exit 1
fi

echo "[OK] Virtual environment activated."

# Pull latest code
git pull

# Install dependencies
pip install -r requirements.txt

# Restart backend service
sudo systemctl restart "$SERVICE_NAME"

# Health check
sleep 2
if curl -s http://localhost:8000/docs >/dev/null; then
  echo "[OK] Backend is responding."
else
  echo "[ERROR] Backend health check failed."
  exit 1
fi


###############################################################
# 4. Deploy Frontend
###############################################################
banner "4. Deploying frontend"

cd "$FRONTEND_DIR"

git pull
npm install
npm run build

# Clean webroot
sudo rm -rf "$WEBROOT"/*
sudo mkdir -p "$WEBROOT"

# Copy new build
sudo cp -r dist/* "$WEBROOT"/

# Reload Nginx
sudo systemctl reload nginx

# Frontend health check
if curl -I http://localhost 2>/dev/null | grep -q "200 OK"; then
  echo "[OK] Frontend is serving new build."
else
  echo "[ERROR] Frontend health check failed."
  exit 1
fi


###############################################################
# 5. Final Summary
###############################################################
banner "5. Deployment Complete"

echo "[SUCCESS] Backend + Frontend deployed cleanly."
echo "[SUCCESS] Backend service: $SERVICE_NAME"
echo "[SUCCESS] Webroot: $WEBROOT"
echo ""
echo "Hard refresh your browser:"
echo "  - Windows/Linux: Ctrl + Shift + R"
echo "  - Mac: Cmd + Shift + R"
echo ""
