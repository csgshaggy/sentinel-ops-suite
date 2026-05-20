#!/usr/bin/env bash
set -euo pipefail

###############################################################
# Sentinel Ops Suite — Rollback Script
# Restores previous backend commit + previous frontend build
###############################################################

ROOT="/home/ubuntu/sentinel-ops-suite"
BACKEND_DIR="$ROOT/backend"
FRONTEND_DIR="$ROOT/frontend"
WEBROOT="/var/www/sentinel-frontend"
BACKUP_DIR="$ROOT/backups"

banner() {
  echo ""
  echo "============================================================"
  echo "== $1"
  echo "============================================================"
  echo ""
}

banner "1. Validating backup directory"

if [[ ! -d "$BACKUP_DIR" ]]; then
  echo "[ERROR] No backups directory found at $BACKUP_DIR"
  exit 1
fi

###############################################
# 2. Rollback Backend
###############################################
banner "2. Rolling back backend"

cd "$BACKEND_DIR"

if git rev-parse --verify HEAD~1 >/dev/null 2>&1; then
  git reset --hard HEAD~1
  echo "[OK] Backend rolled back to previous commit."
else
  echo "[ERROR] No previous commit to roll back to."
  exit 1
fi

sudo systemctl restart uvicorn.service
sleep 2

if curl -s http://localhost:8000/docs >/dev/null; then
  echo "[OK] Backend healthy after rollback."
else
  echo "[ERROR] Backend failed after rollback."
  exit 1
fi

###############################################
# 3. Rollback Frontend
###############################################
banner "3. Rolling back frontend"

LATEST_BACKUP=$(ls -t "$BACKUP_DIR" | head -n 1)

if [[ -z "$LATEST_BACKUP" ]]; then
  echo "[ERROR] No frontend backups found."
  exit 1
fi

sudo rm -rf "$WEBROOT"/*
sudo cp -r "$BACKUP_DIR/$LATEST_BACKUP"/* "$WEBROOT"/

sudo systemctl reload nginx

if curl -I http://localhost 2>/dev/null | grep -q "200 OK"; then
  echo "[OK] Frontend healthy after rollback."
else
  echo "[ERROR] Frontend failed after rollback."
  exit 1
fi

banner "Rollback Complete"
echo "[SUCCESS] System restored to previous known-good state."
