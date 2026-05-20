#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/venv"

echo "[*] Project root: $PROJECT_ROOT"

if [ ! -d "$VENV_DIR" ]; then
  echo "[*] Creating virtualenv at $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

echo "[*] Using Python: $(which python)"
echo "[*] Using pip:    $(which pip)"

if [ -f "$PROJECT_ROOT/requirements.lock" ]; then
  echo "[*] Installing from requirements.lock"
  pip install --upgrade pip
  pip install -r "$PROJECT_ROOT/requirements.lock"
else
  echo "[*] Installing from requirements.txt"
  pip install --upgrade pip
  pip install -r "$PROJECT_ROOT/requirements.txt"
  pip freeze > "$PROJECT_ROOT/requirements.lock"
fi

echo "[+] Environment ready."
