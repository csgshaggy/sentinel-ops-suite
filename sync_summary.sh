#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="sync.log"

echo "=== Sync Summary ==="

# Timestamp
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"

# Last commit
LAST_COMMIT=$(git log -1 --pretty=format:"%h %s")
echo "Last Commit: $LAST_COMMIT"

# Files changed
CHANGES=$(git diff --stat HEAD~1 HEAD 2>/dev/null || echo "N/A")
echo "Changes:"
echo "$CHANGES"

# Rebase status
if git rebase --show-current-patch >/dev/null 2>&1; then
    echo "Rebase: IN PROGRESS"
else
    echo "Rebase: Clean"
fi

# Push status (best-effort)
if git status -sb | grep -q "\[ahead"; then
    echo "Push: Pending"
else
    echo "Push: Up to date"
fi

# Drift status
if command -v npx >/dev/null 2>&1; then
    DRIFT_JS=$(npx prettier --check "frontend/src/**/*.{js,jsx,ts,tsx}" >/dev/null 2>&1 && echo "No JS/TS drift" || echo "JS/TS drift detected")
else
    DRIFT_JS="Prettier not installed"
fi

if command -v black >/dev/null 2>&1; then
    DRIFT_PY=$(black --check backend app >/dev/null 2>&1 && echo "No Python drift" || echo "Python drift detected")
else
    DRIFT_PY="Black not installed"
fi

echo "Drift:"
echo "  - $DRIFT_JS"
echo "  - $DRIFT_PY"

echo "=== End Sync Summary ==="
