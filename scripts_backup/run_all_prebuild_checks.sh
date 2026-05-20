#!/usr/bin/env bash
set -euo pipefail

echo "[1/4] Running environment validation..."
./scripts/env_check.sh

echo "[2/4] Running dependency validator..."
./scripts/validate_deps.sh

echo "[3/4] Running lint checks..."
npm run lint

echo "[4/4] Running frontend smoke test..."
./scripts/frontend_smoke.sh

echo "All prebuild checks passed."
