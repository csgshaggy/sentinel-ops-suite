#!/usr/bin/env bash
set -euo pipefail

# Chain banner
echo -e "\n\033[1;36m[CHAIN] Running: $(basename "$0")\033[0m"

echo "[env_check] Validating environment..."

# Resolve script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Ensure script is run from project root or scripts directory
if [[ ! -d "$PROJECT_ROOT/frontend" && ! -d "$PROJECT_ROOT/backend" ]]; then
  echo "[env_check] ERROR: This script must be run from the project root or scripts directory."
  echo "[env_check] PROJECT_ROOT resolved to: $PROJECT_ROOT"
  exit 1
fi

# Check Node
if ! command -v node >/dev/null 2>&1; then
  echo "[env_check] ERROR: Node.js is not installed."
  exit 1
fi

# Check npm
if ! command -v npm >/dev/null 2>&1; then
  echo "[env_check] ERROR: npm is not installed."
  exit 1
fi

# Check Python
if ! command -v python3 >/dev/null 2>&1; then
  echo "[env_check] ERROR: Python3 is not installed."
  exit 1
fi

# Check virtual environment (supports root or backend venv)
if [[ ! -d "$PROJECT_ROOT/.venv" && ! -d "$PROJECT_ROOT/backend/.venv" ]]; then
  echo "[env_check] WARNING: No Python virtual environment found."
else
  echo "[env_check] Python virtual environment detected."
fi

# Check permissions
if [[ ! -x "$SCRIPT_DIR/env_check.sh" ]]; then
  echo "[env_check] WARNING: env_check.sh is not executable. Fixing..."
  chmod +x "$SCRIPT_DIR/env_check.sh"
fi

echo "[env_check] Environment OK."

