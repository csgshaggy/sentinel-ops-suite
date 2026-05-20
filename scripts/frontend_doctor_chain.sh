#!/usr/bin/env bash
set -euo pipefail

echo "[CHAIN] Starting frontend doctor chain..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

FRONTEND_DOCTOR="$SCRIPT_DIR/frontend_doctor.sh"
FRONTEND_SMOKE="$SCRIPT_DIR/frontend_smoke.sh"
CI_GUARD="$SCRIPT_DIR/ci_guard.sh"

# -----------------------------
# 1. Frontend Doctor
# -----------------------------
echo "[CHAIN] Running: frontend_doctor.sh"
if ! "$FRONTEND_DOCTOR"; then
    echo "[CHAIN] FAIL: frontend_doctor.sh failed."
    exit 1
fi

# -----------------------------
# 2. Frontend Smoke Tests
# -----------------------------
echo "[CHAIN] Running: frontend_smoke.sh"
if ! "$FRONTEND_SMOKE"; then
    echo "[CHAIN] FAIL: frontend_smoke.sh failed."
    exit 1
fi

# -----------------------------
# 3. CI Guard (frontend portion)
# -----------------------------
echo "[CHAIN] Running: ci_guard.sh"
if ! "$CI_GUARD"; then
    echo "[CHAIN] FAIL: ci_guard.sh failed."
    exit 1
fi

echo "[CHAIN] SUCCESS: Frontend doctor chain completed successfully."

