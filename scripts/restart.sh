#!/bin/bash
set -e

echo "============================================================"
echo " Sentinel Ops Suite — Unified Restart Script"
echo "============================================================"

FRONTEND_DIR="$HOME/sentinel-ops-suite/frontend/unified-frontend"
BACKEND_DIR="$HOME/sentinel-ops-suite/backend"

echo ""
echo "------------------------------------------------------------"
echo " 1. Rebuilding Frontend (Vite → dist/)"
echo "------------------------------------------------------------"
cd "$FRONTEND_DIR"
npm run build

echo ""
echo "------------------------------------------------------------"
echo " 2. Reloading NGINX"
echo "------------------------------------------------------------"
sudo nginx -t
sudo systemctl reload nginx

echo ""
echo "------------------------------------------------------------"
echo " 3. Restarting Backend (Uvicorn)"
echo "------------------------------------------------------------"
cd "$BACKEND_DIR"

# Activate virtual environment if present
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Kill any running uvicorn processes
pkill -f uvicorn || true

# Start backend
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &

echo ""
echo "------------------------------------------------------------"
echo " Restart Complete"
echo "------------------------------------------------------------"
echo "Frontend: Rebuilt + NGINX reloaded"
echo "Backend:  Uvicorn restarted (running in background)"
echo "Logs:     $BACKEND_DIR/backend.log"
echo "============================================================"
