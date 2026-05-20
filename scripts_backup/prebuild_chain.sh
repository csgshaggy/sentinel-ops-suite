#!/usr/bin/env bash
set -euo pipefail

# Chain banner
echo -e "\n\033[1;36m[CHAIN] Running: prebuild_chain.sh\033[0m"

echo "=========================================="
echo " SENTINELOPS PREBUILD VALIDATION CHAIN"
echo "=========================================="

# Resolve script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "[1/8] Environment validation..."
"$SCRIPT_DIR/env_check.sh"

echo "[2/8] Dependency validation..."
"$SCRIPT_DIR/validate_deps.sh"

echo "[3/8] Cleaning stray .txt files..."
"$SCRIPT_DIR/cleanup_txt.sh"

echo "[4/8] CI guard checks..."
"$SCRIPT_DIR/ci_guard.sh"

echo "[5/8] Running precommit tests..."
"$SCRIPT_DIR/precommit-tests.sh"

echo "[6/8] Running full test suite..."
"$SCRIPT_DIR/run_tests.sh"

echo "[7/8] Frontend smoke test..."
"$SCRIPT_DIR/frontend_smoke.sh"

echo "[8/8] Linting..."
(
    cd "$PROJECT_ROOT/frontend"
    npm run lint
)

echo "=========================================="
echo " ALL PREBUILD CHECKS PASSED"
echo "=========================================="
