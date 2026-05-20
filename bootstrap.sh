#!/usr/bin/env bash
# bootstrap.sh — SSRF Command Console bootstrap
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-venv}"
PYTHON="${PYTHON:-python}"

echo "[bootstrap] Root: ${ROOT_DIR}"
cd "${ROOT_DIR}"

if [ ! -d "${VENV_DIR}" ]; then
  echo "[bootstrap] Creating virtualenv at ${VENV_DIR}"
  "${PYTHON}" -m venv "${VENV_DIR}"
else
  echo "[bootstrap] Using existing virtualenv at ${VENV_DIR}"
fi

# shellcheck disable=SC1090
source "${VENV_DIR}/bin/activate"

echo "[bootstrap] Upgrading pip"
pip install --upgrade pip

echo "[bootstrap] Installing package (editable) with dev extras"
pip install -e ".[dev]"

echo "[bootstrap] Validating structure"
python scripts/structure_validator.py

echo "[bootstrap] Running doctor commands"
ssrf-console doctor env || true
ssrf-console doctor plugins || true
ssrf-console doctor structure || true

echo "[bootstrap] Done."
