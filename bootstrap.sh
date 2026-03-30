#!/usr/bin/env bash
set -e

echo "=== SSRF Command Console — Bootstrap ==="

# Create venv if missing
if [ ! -d ".venv" ]; then
  echo "[*] Creating virtual environment..."
  python3 -m venv .venv
fi

# Activate venv
echo "[*] Activating virtual environment..."
# shellcheck disable=SC1091
source .venv/bin/activate

# Install project + dev deps
echo "[*] Installing project and development dependencies..."
pip install -e .
if [ -f requirements-dev.txt ]; then
  pip install -r requirements-dev.txt
fi

# Validate structure
echo "[*] Validating project structure..."
make structure

# Smoke test CLI
echo "[*] Running CLI smoke test..."
make smoke

echo "=== Bootstrap complete. Environment ready. ==="
