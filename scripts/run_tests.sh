#!/usr/bin/env bash
set -euo pipefail

# Chain banner
echo -e "\n\033[1;36m[CHAIN] Running: $(basename "$0")\033[0m"

echo "[run_tests] Running full project test suite..."

# Resolve script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

###############################################
# 1. Frontend tests
###############################################
echo "[run_tests] Checking for frontend test suite..."

FRONTEND_DIR="$PROJECT_ROOT/frontend"

if [[ -f "$FRONTEND_DIR/package.json" ]]; then
    echo "[run_tests] Running frontend tests via npm..."
    (
        cd "$FRONTEND_DIR"
        if npm test --silent; then
            echo "[run_tests] OK: Frontend tests passed."
        else
            echo "[run_tests] ERROR: Frontend tests failed."
            exit 1
        fi
    )
else
    echo "[run_tests] WARNING: No package.json found — skipping frontend tests."
fi

###############################################
# 2. Backend tests
###############################################
echo "[run_tests] Checking for backend test suite..."

BACKEND_DIR="$PROJECT_ROOT/backend"

if [[ -d "$BACKEND_DIR" ]]; then
    if command -v pytest >/dev/null 2>&1; then
        if find "$BACKEND_DIR" -type f -name "test_*.py" | grep -q .; then
            echo "[run_tests] Running backend tests via pytest..."
            (
                cd "$BACKEND_DIR"
                if pytest -q; then
                    echo "[run_tests] OK: Backend tests passed."
                else
                    echo "[run_tests] ERROR: Backend tests failed."
                    exit 1
                fi
            )
        else
            echo "[run_tests] WARNING: No backend test files found."
        fi
    else
        echo "[run_tests] WARNING: pytest not installed — skipping backend tests."
    fi
else
    echo "[run_tests] WARNING: backend/ directory not found — skipping backend tests."
fi

###############################################
# 3. Final result
###############################################
echo "[run_tests] All test phases complete."

