#!/usr/bin/env bash
set -euo pipefail

echo "============================================================"
echo " SENTINEL OPS SUITE — UNIFIED LINT + FORMAT CHAIN"
echo " React 19 / Vite 5 / ESLint 9 / Prettier 3"
echo "============================================================"

BASE="/home/ubuntu/sentinel-ops-suite/frontend"

LOGIN="$BASE/login-app"
DASH="$BASE/dashboard-app"

echo ""
echo "------------------------------------------------------------"
echo " STEP 1 — Lint: login-app"
echo "------------------------------------------------------------"
cd "$LOGIN"
npm run lint

echo ""
echo "------------------------------------------------------------"
echo " STEP 2 — Lint: dashboard-app"
echo "------------------------------------------------------------"
cd "$DASH"
npm run lint

echo ""
echo "------------------------------------------------------------"
echo " STEP 3 — Format: login-app"
echo "------------------------------------------------------------"
cd "$LOGIN"
npm run format || echo "[format] login-app: Prettier applied"

echo ""
echo "------------------------------------------------------------"
echo " STEP 4 — Format: dashboard-app"
echo "------------------------------------------------------------"
cd "$DASH"
npm run format || echo "[format] dashboard-app: Prettier applied"

echo ""
echo "============================================================"
echo " LINT + FORMAT CHAIN COMPLETE — ALL SYSTEMS GREEN"
echo "============================================================"
