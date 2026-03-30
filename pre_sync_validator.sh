#!/usr/bin/env bash
set -euo pipefail

echo "=== Pre‑Sync Validator ==="

# 1. Ensure sync.sh exists
if [[ ! -f "./sync.sh" ]]; then
    echo "[ERROR] sync.sh not found in repo root."
    exit 1
fi

# 2. Ensure sync.sh is executable
if [[ ! -x "./sync.sh" ]]; then
    echo "[ERROR] sync.sh is not executable. Run: chmod +x sync.sh"
    exit 1
fi

# 3. Ensure no ongoing rebase
if [[ -d ".git/rebase-apply" || -d ".git/rebase-merge" ]]; then
    echo "[ERROR] Rebase in progress. Resolve it before syncing."
    exit 1
fi

# 4. Ensure no merge conflicts
if git ls-files -u | grep -q .; then
    echo "[ERROR] Merge conflicts detected. Resolve them before syncing."
    exit 1
fi

# 5. Ensure working tree is clean
if [[ -n "$(git status --porcelain)" ]]; then
    echo "[WARNING] Working tree has changes."
    echo "This is allowed, but sync.sh will commit them."
fi

echo "=== Pre‑Sync Validator Passed ==="
