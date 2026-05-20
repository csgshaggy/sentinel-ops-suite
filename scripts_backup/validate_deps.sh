#!/usr/bin/env bash
set -euo pipefail

# Chain banner
echo -e "\n\033[1;36m[CHAIN] Running: $(basename "$0")\033[0m"

echo "[validate_deps] Validating required dependencies..."

# Resolve script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Helper function for dependency checks
check_dep() {
    local dep="$1"
    local name="$2"

    if ! command -v "$dep" >/dev/null 2>&1; then
        echo "[validate_deps] ERROR: Missing dependency: $name ($dep)"
        exit 1
    else
        echo "[validate_deps] OK: $name detected"
    fi
}

echo "[validate_deps] Checking system binaries..."

# Core system tools
check_dep "bash" "Bash"
check_dep "grep" "grep"
check_dep "sed" "sed"
check_dep "awk" "awk"
check_dep "curl" "curl"
check_dep "git" "Git"

echo "[validate_deps] Checking Node.js toolchain..."

# Node.js + npm
check_dep "node" "Node.js"
check_dep "npm" "npm"

# Optional but recommended: npx
if ! command -v npx >/dev/null 2>&1; then
    echo "[validate_deps] WARNING: npx not found — some frontend tasks may fail."
else
    echo "[validate_deps] OK: npx detected"
fi

echo "[validate_deps] Checking Python toolchain..."

# Python + pip
check_dep "python3" "Python3"
check_dep "pip3" "pip3"

echo "[validate_deps] Checking project‑specific directories..."

if [[ ! -d "$PROJECT_ROOT/frontend" ]]; then
    echo "[validate_deps] WARNING: frontend/ directory not found."
else
    echo "[validate_deps] OK: frontend/ directory found"
fi

if [[ ! -d "$PROJECT_ROOT/backend" ]]; then
    echo "[validate_deps] WARNING: backend/ directory not found."
else
    echo "[validate_deps] OK: backend/ directory found"
fi

echo "[validate_deps] Dependency validation complete."
