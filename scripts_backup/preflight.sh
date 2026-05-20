#!/usr/bin/env bash
set -e

echo "=== Sentinel-Ops-Suite: Preflight Drift & Integrity Scan ==="

# 1. Ensure inside a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "[FATAL] Not inside a Git repository."
    exit 1
fi

# 2. Capture current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "[INFO] Branch: $BRANCH"

# 3. Ensure branch has upstream
if ! git rev-parse --abbrev-ref @{u} >/dev/null 2>&1; then
    echo "[WARN] No upstream branch configured."
else
    echo "[OK] Upstream detected: $(git rev-parse --abbrev-ref @{u})"
fi

# 4. Fetch latest remote state
git fetch --quiet origin

# 5. Detect drift (ahead/behind/diverged)
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u} 2>/dev/null || echo "none")
BASE=$(git merge-base @ @{u} 2>/dev/null || echo "none")

if [[ "$REMOTE" == "none" ]]; then
    echo "[WARN] No remote branch to compare."
elif [[ "$LOCAL" == "$REMOTE" ]]; then
    echo "[OK] No Git drift (local == remote)."
elif [[ "$LOCAL" == "$BASE" ]]; then
    echo "[WARN] Local is BEHIND remote."
elif [[ "$REMOTE" == "$BASE" ]]; then
    echo "[WARN] Local is AHEAD of remote."
else
    echo "[FATAL] Local and remote have DIVERGED."
fi

# 6. Detect untracked files
UNTRACKED=$(git ls-files --others --exclude-standard)
if [ -n "$UNTRACKED" ]; then
    echo "[WARN] Untracked files:"
    echo "$UNTRACKED"
fi

# 7. Detect unstaged or staged changes
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "[WARN] Working tree has modifications."
fi

# 8. Structural anomaly detection
echo "[INFO] Checking directory structure..."

REQUIRED_DIRS=(
    "backend"
    "dashboard-app"
    "login-app"
    "scripts"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "[FATAL] Missing required directory: $dir"
    else
        echo "[OK] $dir exists."
    fi
done

# 9. Detect unexpected top-level directories
echo "[INFO] Scanning for unexpected directories..."
EXPECTED=$(printf "%s\n" "${REQUIRED_DIRS[@]}" ".git" ".github")
for d in */; do
    d=${d%/}
    if ! printf "%s\n" "$EXPECTED" | grep -qx "$d"; then
        echo "[WARN] Unexpected directory detected: $d"
    fi
done

# 10. Permission drift detection
echo "[INFO] Checking for permission drift..."
find . -type f -perm /111 | grep -v "\.sh$" && echo "[WARN] Non-script files are executable."

# 11. Symlink anomaly detection
echo "[INFO] Checking for symlink anomalies..."
find . -type l -exec ls -l {} \; | grep -v "" || echo "[OK] No symlinks detected."

# 12. Line-ending drift
echo "[INFO] Checking for CRLF drift..."
CRLF=$(grep -rl $'\r' . | grep -v ".git")
if [ -n "$CRLF" ]; then
    echo "[WARN] Files with CRLF line endings:"
    echo "$CRLF"
fi

# 13. Timestamp anomaly detection
echo "[INFO] Checking for timestamp anomalies..."
find . -type f -newer .git/HEAD && echo "[WARN] Files modified after last commit."

# 14. Git index integrity
git fsck --no-progress --no-reflogs >/dev/null 2>&1 || {
    echo "[FATAL] Git index corruption detected."
    exit 1
}

echo "=== Preflight Scan Complete ==="
