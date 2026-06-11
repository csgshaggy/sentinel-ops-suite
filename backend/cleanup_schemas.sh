#!/bin/bash
set -e

echo "=== SentinelOps Schema Cleanup ==="

# Ensure legacy folder exists
mkdir -p app/schemas_legacy

echo "Moving dead schemas to app/schemas_legacy ..."

# ACTIVE SCHEMAS (DO NOT MOVE)
ACTIVE=(
  "auth.py"
  "user.py"
  "api_keys.py"
  "sessions.py"
  "settings.py"
  "governance.py"
)

# Convert active list to lookup
ACTIVE_LOOKUP=$(printf "|%s" "${ACTIVE[@]}")
ACTIVE_LOOKUP=${ACTIVE_LOOKUP:1}

# Move *.bak schemas
for bak in app/schemas/*.bak; do
    if [[ -e "$bak" ]]; then
        echo "Moving backup schema: $(basename "$bak")"
        mv "$bak" app/schemas_legacy/
    fi
done

# Move all non-active schemas
for file in app/schemas/*.py; do
    base=$(basename "$file")
    if [[ ! "$base" =~ ^($ACTIVE_LOOKUP)$ ]]; then
        echo "Moving dead schema: $base"
        mv "$file" app/schemas_legacy/
    fi
done

echo "Cleanup complete."
