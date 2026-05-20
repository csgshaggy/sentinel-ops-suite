#!/usr/bin/env bash
set -euo pipefail

echo "============================================================"
echo " SENTINEL OPS — FULL DEPLOY PIPELINE"
echo " React 19 / Vite 5+ / Multi‑App"
echo "============================================================"

BASE="/home/ubuntu/sentinel-ops-suite"
LOGIN="$BASE/frontend/login-app"
DASH="$BASE/frontend/dashboard-app"
BACKEND="$BASE/backend"
GUARD="$BASE/scripts/guardrails/guard_manifest.sh"

echo ""
echo "------------------------------------------------------------"
echo " STEP 1 — Build Login App"
echo "------------------------------------------------------------"
cd "$LOGIN"
rm -rf dist
npm install --silent
npm run build

echo ""
echo "------------------------------------------------------------"
echo " STEP 2 — Build Dashboard App"
echo "------------------------------------------------------------"
cd "$DASH"
rm -rf dist
npm install --silent
npm run build

echo ""
echo "------------------------------------------------------------"
echo " STEP 3 — Run Manifest Guardrail"
echo "------------------------------------------------------------"
bash "$GUARD"

echo ""
echo "------------------------------------------------------------"
echo " STEP 4 — Restart Backend (Uvicorn / Gunicorn / Systemd)"
echo "------------------------------------------------------------"
sudo systemctl restart sentinel-backend.service

echo ""
echo "------------------------------------------------------------"
echo " STEP 5 — Reload NGINX"
echo "------------------------------------------------------------"
sudo nginx -t
sudo systemctl reload nginx

echo ""
echo "============================================================"
echo " DEPLOY COMPLETE — ALL SYSTEMS GREEN"
echo "============================================================"
