#!/usr/bin/env bash
set -euo pipefail

###############################################
# Sentinel Ops Suite — Backend Deploy
# Clean, deterministic, operator‑grade
###############################################

BACKEND_DIR="/home/ubuntu/sentinel-ops-suite/backend"
VENV_DIR="$BACKEND_DIR/.venv"
SERVICE_NAME="sentinel-backend"

banner() {
  echo ""
  echo "============================================================"
  echo "== $1"
  echo "============================================================"
  echo ""
}

# --- 1. Validate backend directory ---------------------------------
banner "1. Validating backend directory"

if [[ ! -d "$BACKEND_DIR" ]]; then
  echo "[ERROR] Backend directory not found: $BACKEND_DIR"
  exit 1
fi

if [[ ! -d "$VENV_DIR" ]]; then
  echo "[ERROR] Backend venv not found: $VENV_DIR"
  exit 1
fi

echo "[OK] Backend directory + venv validated."


# --- 2. Stop backend service ---------------------------------------
banner "2. Stopping backend service"

sudo systemctl stop "$SERVICE_NAME" || true
echo "[OK] Backend service stopped."


# --- 3. Install dependencies inside venv ----------------------------
banner "3. Installing backend dependencies (venv)"

cd "$BACKEND_DIR"
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install -r requirements.txt

echo "[OK] Dependencies installed inside venv."


# --- 4. Start backend service --------------------------------------
banner "4. Starting backend service"

sudo systemctl start "$SERVICE_NAME"
echo "[OK] Backend service started."


# --- 5. Verify backend health --------------------------------------
banner "5. Verifying backend health"

sleep 2

if curl -s https://crcybercop.dpdns.org/api/auth/session/restore >/dev/null; then
  echo "[OK] Backend is responding."
else
  echo "[ERROR] Backend health check failed."
  exit 1
fi


# --- 6. Complete ----------------------------------------------------
banner "6. Backend deployment complete"

echo "[SUCCESS] Backend deployed cleanly."
echo ""
