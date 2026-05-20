#!/usr/bin/env bash
set -euo pipefail

# ============================================================
#  ONE‑COMMAND SYNC SCRIPT (authoritative, drift‑proof)
#  Formats → Validates → Stages → Commits → Rebases → Pushes
# ============================================================

REPO_DIR="$(git rev-parse --show-toplevel 2>/dev/null || true)"

if [[ -z "$REPO_DIR" ]]; then
    echo "[ERROR] Not inside a Git repository."
    exit 1
fi

cd "$REPO_DIR"

echo "============================================================"
echo "  SYNC ENGINE STARTED"
echo "  Repo: $REPO_DIR"
echo "  Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "============================================================"

# -------------------------------
# 1. Ensure clean Git environment
# -------------------------------
echo "[1/6] Checking Git status..."
git status --short

# -------------------------------
# 2. Auto-format (if tools exist)
# -------------------------------
echo "[2/6] Running formatters (if available)..."

if command -v black >/dev/null 2>&1; then
    echo " → black ."
    black .
fi

if command -v isort >/dev/null 2>&1; then
    echo " → isort ."
    isort .
fi

if command -v prettier >/dev/null 2>&1; then
    echo " → prettier --write ."
    prettier --write .
fi

# -------------------------------
# 3. Validate (optional)
# -------------------------------
echo "[3/6] Running validators (if available)..."

if command -v flake8 >/dev/null 2>&1; then
    echo " → flake8"
    flake8 || true
fi

if command -v mypy >/dev/null 2>&1; then
    echo " → mypy ."
    mypy . || true
fi

# -------------------------------
# 4. Stage everything
# -------------------------------
echo "[4/6] Staging all changes..."
git add -A

# -------------------------------
# 5. Commit with timestamp
# -------------------------------
echo "[5/6] Committing..."
git commit -m "sync: $(date -u +"%Y-%m-%dT%H:%M:%SZ")" || {
    echo "No changes to commit."
}

# -------------------------------
# 6. Rebase + Push
# -------------------------------
echo "[6/6] Rebasing and pushing..."
git pull --rebase origin main || true
git push origin main

echo "============================================================"
echo "  SYNC COMPLETE ✔"
echo "============================================================"
