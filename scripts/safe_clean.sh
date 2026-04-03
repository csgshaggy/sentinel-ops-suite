#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" != "--force-clean" ]]; then
    echo "[SAFE CLEAN] Refusing to run."
    echo "Usage: ./scripts/safe_clean.sh --force-clean"
    exit 1
fi

echo "[SAFE CLEAN] Running preflight structure validation..."
make validate || {
    echo "[SAFE CLEAN] Structure invalid. Aborting."
    exit 1
}

echo "[SAFE CLEAN] Performing dry-run..."
git rm -r --cached . --dry-run

read -p "Proceed with cleanup? (yes/no): " ans
if [[ "$ans" != "yes" ]]; then
    echo "[SAFE CLEAN] Aborted."
    exit 0
fi

echo "[SAFE CLEAN] Executing cleanup..."
git rm -r --cached .
git add .
echo "[SAFE CLEAN] Cleanup complete. Commit manually."
