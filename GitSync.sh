#!/usr/bin/env bash
set -euo pipefail

REMOTE="${1:-origin}"
BRANCH="${2:-main}"

git rev-parse --is-inside-work-tree >/dev/null

git checkout "$BRANCH"
git fetch "$REMOTE"

# overwrite remote branch with local branch (safer force)
git push --force-with-lease "$REMOTE" "$BRANCH"
echo "Done: $REMOTE/$BRANCH now matches local $BRANCH"
