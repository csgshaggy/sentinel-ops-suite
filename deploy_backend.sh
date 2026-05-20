#!/bin/bash
set -e

echo "=== Sentinel Ops Backend Deployment ==="

BACKEND_DIR="/home/ubuntu/sentinel-ops-suite/backend"

echo "[1/3] Navigating to backend directory..."
cd "$BACKEND_DIR"

echo "[2/3] Activating virtual environment..."
source .venv/bin/activate

echo "[3/3] Restarting backend service..."
sudo systemctl restart sentinel-backend

echo "=== Backend deployment complete ==="
