#!/usr/bin/env bash
set -euo pipefail

echo "============================================================"
echo " SENTINEL OPS SUITE — FULL DEPLOYMENT PIPELINE"
echo " React 19 / Vite 5+ / Multi‑App / FastAPI / NGINX"
echo "============================================================"

BASE="/home/ubuntu/sentinel-ops-suite"

LOGIN="$BASE/frontend/login-app"
DASH="$BASE/frontend/dashboard-app"
BACKEND="$BASE/backend"

VALIDATOR="$BASE/scripts/validators/validate_build.sh"
GUARDRAIL="$BASE/scripts/guardrails/guard_manifest.sh"

SYSTEMD_SERVICE="sentinel-backend.service"

echo ""
echo "------------------------------------------------------------"
echo " STEP 1 — Environment Validation"
echo "------------------------------------------------------------"

[[ -d "$LOGIN" ]] || { echo "❌ Missing login-app directory"; exit 1; }
[[ -d "$DASH" ]]  || { echo "❌ Missing dashboard-app directory"; exit 1; }
[[ -d "$BACKEND" ]] || { echo "❌ Missing backend directory"; exit 1; }

echo "✓ Environment OK"

echo ""
echo "------------------------------------------------------------"
echo " STEP 2 — Build Login App"
echo "------------------------------------------------------------"
cd "$LOGIN"
rm -rf dist
npm install --silent
npm run build

echo ""
echo "------------------------------------------------------------"
echo " STEP 3 — Build Dashboard App"
echo "------------------------------------------------------------"
cd "$DASH"
rm -rf dist
npm install --silent
npm run build

echo ""
echo "------------------------------------------------------------"
echo " STEP 4 — Build Validation"
echo "------------------------------------------------------------"
bash "$VALIDATOR"

echo ""
echo "------------------------------------------------------------"
echo " STEP 5 — Manifest Guardrail"
echo "------------------------------------------------------------"
bash "$GUARDRAIL"

echo ""
echo "------------------------------------------------------------"
echo " STEP 6 — Restart Backend"
echo "------------------------------------------------------------"
sudo systemctl restart "$SYSTEMD_SERVICE"

echo ""
echo "------------------------------------------------------------"
echo " STEP 7 — Reload NGINX"
echo "------------------------------------------------------------"
sudo nginx -t
sudo systemctl reload nginx

echo ""
echo "============================================================"
echo " FULL DEPLOYMENT COMPLETE — ALL SYSTEMS GREEN"
echo "============================================================"
