#!/bin/bash

set -e

echo "=== SentinelOps Router Cleanup ==="

# Create legacy folder
mkdir -p app/routers/legacy

echo "Moving dead routers to app/routers/legacy ..."

# ACTIVE ROUTERS (DO NOT MOVE)
ACTIVE=(
  "auth.py"
  "users.py"
  "admin.py"
  "health.py"
  "profile_avatar.py"
  "settings_router.py"
  "governance.py"
)

# Convert active list to a lookup string
ACTIVE_LOOKUP=$(printf "|%s" "${ACTIVE[@]}")
ACTIVE_LOOKUP=${ACTIVE_LOOKUP:1}

# Move *.bak routers
find app/routers -maxdepth 1 -name "*.bak" -exec mv {} app/routers/legacy/ \;

# Move all non-active routers
for file in app/routers/*.py; do
    base=$(basename "$file")
    if [[ ! "$base" =~ ^($ACTIVE_LOOKUP)$ ]]; then
        echo "Moving dead router: $base"
        mv "$file" app/routers/legacy/
    fi
done

echo "Cleanup complete."
