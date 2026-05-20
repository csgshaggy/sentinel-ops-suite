#!/usr/bin/env bash
set -e

echo "=== Sentinel-Ops-Suite: Repo Health Validator ==="

# 1. Ensure we are inside a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "[FATAL] Not inside a Git repository."
    exit 1
fi

# 2. Detect untracked files
UNTRACKED=$(git ls-files --others --exclude-standard)
if [ -n "$UNTRACKED" ]; then
    echo "[WARN] Untracked files detected:"
    echo "$UNTRACKED"
else
    echo "[OK] No untracked files."
fi

# 3. Detect unstaged or staged changes
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "[WARN] Working tree has modifications."
else
    echo "[OK] Working tree clean."
fi

# 4. Ensure branch is valid
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "[INFO] Current branch: $BRANCH"

if [[ "$BRANCH" == "main" ]]; then
    echo "[WARN] You are on MAIN. Direct commits are forbidden."
fi

# 5. Check for divergence from origin
git fetch --quiet origin

LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u} 2>/dev/null || echo "none")
BASE=$(git merge-base @ @{u} 2>/dev/null || echo "none")

if [[ "$REMOTE" == "none" ]]; then
    echo "[WARN] No upstream branch configured."
elif [[ "$LOCAL" == "$REMOTE" ]]; then
    echo "[OK] Branch is up to date with origin."
elif [[ "$LOCAL" == "$BASE" ]]; then
    echo "[WARN] Local branch is BEHIND origin."
elif [[ "$REMOTE" == "$BASE" ]]; then
    echo "[WARN] Local branch is AHEAD of origin."
else
    echo "[FATAL] Local and remote branches have DIVERGED."
fi

# 6. Node dependency drift
if [ -f package.json ]; then
    echo "[INFO] Checking Node dependency drift..."
    npm ls >/dev/null 2>&1 || echo "[WARN] Node dependency issues detected."
fi

# 7. Python dependency drift
if [ -f requirements.txt ]; then
    echo "[INFO] Checking Python dependency drift..."
    pip check >/dev/null 2>&1 || echo "[WARN] Python dependency issues detected."
fi

# 8. Git index integrity
git fsck --no-progress --no-reflogs >/dev/null 2>&1 || {
    echo "[FATAL] Git index corruption detected."
    exit 1
}

echo "=== Repo Health Check Complete ==="

