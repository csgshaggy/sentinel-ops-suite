#!/usr/bin/env bash
# SentinelOps — Repo Self-Healing Script
# Performs safe, deterministic repairs

set -euo pipefail

REPO_ROOT="/home/ubuntu/sentinel-ops-suite"
cd "$REPO_ROOT"

echo "=== SentinelOps Repo Self-Heal ==="

echo "[1/6] Ensuring git working tree is present..."
if [[ ! -d ".git" ]]; then
  echo "ERROR: .git directory missing. Aborting."
  exit 1
fi

echo "[2/6] Restoring tracked files to HEAD (no untracked removal)..."
git restore .

echo "[3/6] Validating backend virtualenv..."
if [[ ! -d "backend/.venv" ]]; then
  echo "Recreating backend virtualenv..."
  python3 -m venv backend/.venv
  source backend/.venv/bin/activate
  pip install -r backend/requirements.txt
else
  echo "OK: backend/.venv exists"
fi

echo "[4/6] Validating frontend dependencies..."
if [[ ! -d "frontend/node_modules" ]]; then
  echo "Reinstalling frontend dependencies..."
  cd frontend
  npm install
  cd "$REPO_ROOT"
else
  echo "OK: frontend/node_modules exists"
fi

echo "[5/6] Rebuilding frontend dist..."
cd frontend
npm run build
cd "$REPO_ROOT"

echo "[6/6] Validating NGINX + backend service..."
sudo nginx -t || { echo "ERROR: NGINX config invalid"; exit 1; }
sudo systemctl daemon-reload
sudo systemctl restart sentinel-backend.service

echo "=== Self-heal complete ==="
