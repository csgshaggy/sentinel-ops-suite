#!/usr/bin/env bash
# SentinelOps — Repo Integrity Audit
# Read-only, deterministic, operator-grade

set -euo pipefail

REPO_ROOT="/home/ubuntu/sentinel-ops-suite"
cd "$REPO_ROOT"

echo "=== SentinelOps Repo Integrity Audit ==="

echo "[1/7] Git status (cleanliness)..."
git status --short

echo "[2/7] Untracked files..."
git ls-files --others --exclude-standard

echo "[3/7] Modified tracked files..."
git diff --name-status

echo "[4/7] Checking for missing critical paths..."
critical_paths=(
  "backend/app/main.py"
  "backend/app/core/settings.py"
  "frontend/vite.config.js"
  "frontend/src/main.jsx"
  "deploy.sh"
)

missing=0
for path in "${critical_paths[@]}"; do
  if [[ ! -e "$path" ]]; then
    echo "MISSING: $path"
    missing=1
  else
    echo "OK: $path"
  fi
done

echo "[5/7] Validating Python environment..."
if [[ -d "backend/.venv" ]]; then
  echo "OK: backend/.venv exists"
else
  echo "WARN: backend/.venv missing"
fi

echo "[6/7] Validating Node modules (frontend)..."
if [[ -d "frontend/node_modules" ]]; then
  echo "OK: frontend/node_modules exists"
else
  echo "WARN: frontend/node_modules missing"
fi

echo "[7/7] NGINX + systemd references..."
if [[ -f "/etc/nginx/sites-enabled/sentinel" ]]; then
  echo "OK: /etc/nginx/sites-enabled/sentinel present"
else
  echo "WARN: NGINX sentinel config missing"
fi

if systemctl list-units --type=service | grep -q "sentinel-backend.service"; then
  echo "OK: sentinel-backend.service registered"
else
  echo "WARN: sentinel-backend.service not registered"
fi

echo "=== Audit complete ==="

