#!/usr/bin/env bash
set -euo pipefail

echo -e "\n\033[1;36m[CHAIN] Running: $(basename "$0")\033[0m"
echo "[ci_guard] Starting CI guardrail validation..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "[ci_guard] Checking frontend build artifacts..."
FRONTEND_BUILD_DIR="$PROJECT_ROOT/frontend/dist"

if [[ ! -d "$FRONTEND_BUILD_DIR" ]]; then
    echo "[ci_guard] ERROR: Frontend build directory not found: $FRONTEND_BUILD_DIR"
    exit 1
fi

if ! find "$FRONTEND_BUILD_DIR" -type f -name "*.js" | grep -q .; then
    echo "[ci_guard] ERROR: No JavaScript build artifacts found in dist/"
    exit 1
fi

echo "[ci_guard] OK: Frontend build artifacts detected."

echo "[ci_guard] Checking backend dependencies..."
BACKEND_DIR="$PROJECT_ROOT/backend"

if [[ ! -f "$BACKEND_DIR/requirements.txt" ]]; then
    echo "[ci_guard] ERROR: Missing backend requirements.txt"
    exit 1
fi

if [[ ! -d "$BACKEND_DIR/.venv" ]]; then
    echo "[ci_guard] WARNING: Backend virtual environment not found."
else
    echo "[ci_guard] OK: Backend virtual environment detected."
fi

echo "[ci_guard] Validating Content-Security-Policy headers..."
CSP_FILE="$PROJECT_ROOT/frontend/dist/index.html"

if [[ ! -f "$CSP_FILE" ]]; then
    echo "[ci_guard] WARNING: index.html not found — skipping CSP validation."
else
    if grep -i "content-security-policy" "$CSP_FILE" >/dev/null 2>&1; then
        echo "[ci_guard] OK: CSP header found in index.html"
    else
        echo "[ci_guard] WARNING: No CSP header found in index.html"
    fi
fi

echo "[ci_guard] Checking for header folding (CRLF patterns)..."
if grep -R $'\r' "$PROJECT_ROOT" >/dev/null 2>&1; then
    echo "[ci_guard] ERROR: CRLF line endings detected — header folding risk."
    exit 1
else
    echo "[ci_guard] OK: No CRLF folding detected."
fi

echo "[ci_guard] Checking for required security headers..."
REQUIRED_HEADERS=(
    "X-Frame-Options"
    "X-Content-Type-Options"
    "Referrer-Policy"
    "Strict-Transport-Security"
)

for header in "${REQUIRED_HEADERS[@]}"; do
    if grep -R "$header" "$PROJECT_ROOT/frontend/dist" >/dev/null 2>&1; then
        echo "[ci_guard] OK: $header found"
    else
        echo "[ci_guard] WARNING: $header missing"
    fi
done

echo "[ci_guard] CI guardrail validation complete."
