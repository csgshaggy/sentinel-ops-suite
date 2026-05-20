#!/usr/bin/env bash
set -euo pipefail

echo "============================================================"
echo " SENTINEL OPS — UNIFIED CI PIPELINE"
echo " React 19 / Vite 5+ / Multi‑App"
echo "============================================================"

BASE="/home/ubuntu/sentinel-ops-suite"

LOGIN="$BASE/frontend/login-app"
DASH="$BASE/frontend/dashboard-app"

DEPLOY_SCRIPT="$BASE/scripts/deploy/deploy.sh"
VALIDATOR="$BASE/scripts/validators/validate_build.sh"
GUARDRAIL="$BASE/scripts/guardrails/guard_manifest.sh"

echo ""
echo "------------------------------------------------------------"
echo " STEP 1 — Frontend Builds (Login + Dashboard)"
echo "------------------------------------------------------------"
bash "$DEPLOY_SCRIPT" || {
  echo "❌ Deploy script failed during build or reload."
  exit 1
}

echo ""
echo "------------------------------------------------------------"
echo " STEP 2 — Build Validation"
echo "------------------------------------------------------------"
bash "$VALIDATOR" || {
  echo "❌ Build validation failed."
  exit 1
}

echo ""
echo "------------------------------------------------------------"
echo " STEP 3 — Manifest Guardrail"
echo "------------------------------------------------------------"
bash "$GUARDRAIL" || {
  echo "❌ Manifest guardrail failed."
  exit 1
}

echo ""
echo "============================================================"
echo " CI PIPELINE COMPLETE — ALL CHECKS PASSED"
echo "============================================================"
