#!/usr/bin/env bash
set -euo pipefail

# Chain banner
echo -e "\n\033[1;36m[CHAIN] Running: $(basename "$0")\033[0m"

echo "[precommit-tests] Running pre-commit validation checks..."

# Resolve script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

###############################################
# 1. Shell script linting
###############################################
echo "[precommit-tests] Linting shell scripts..."

if command -v shellcheck >/dev/null 2>&1; then
    find "$PROJECT_ROOT" -type f -name "*.sh" | while read -r file; do
        echo "[precommit-tests] shellcheck: $file"
        shellcheck "$file"
    done
else
    echo "[precommit-tests] WARNING: shellcheck not installed — skipping shell linting."
fi

###############################################
# 2. Python linting
###############################################
echo "[precommit-tests] Linting Python files..."

if command -v flake8 >/dev/null 2>&1; then
    if find "$PROJECT_ROOT/backend" -type f -name "*.py" | grep -q .; then
        flake8 "$PROJECT_ROOT/backend"
    else
        echo "[precommit-tests] No Python files found."
    fi
else
    echo "[precommit-tests] WARNING: flake8 not installed — skipping Python linting."
fi

###############################################
# 3. JavaScript/TypeScript linting
###############################################
echo "[precommit-tests] Linting JS/TS files..."

if command -v npx >/dev/null 2>&1; then
    if [[ -f "$PROJECT_ROOT/frontend/package.json" ]]; then
        (cd "$PROJECT_ROOT/frontend" && npx eslint . || true)
    else
        echo "[precommit-tests] No frontend package.json found — skipping JS linting."
    fi
else
    echo "[precommit-tests] WARNING: npx not installed — skipping JS linting."
fi

###############################################
# 4. Markdown formatting check
###############################################
echo "[precommit-tests] Checking Markdown formatting..."

if command -v markdownlint >/dev/null 2>&1; then
    find "$PROJECT_ROOT" -type f -name "*.md" | while read -r file; do
        markdownlint "$file" || true
    done
else
    echo "[precommit-tests] WARNING: markdownlint not installed — skipping MD checks."
fi

###############################################
# 5. Final result
###############################################
echo "[precommit-tests] Pre-commit validation complete."

