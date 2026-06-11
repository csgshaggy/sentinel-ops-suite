#!/bin/bash
set -e

echo "=== SentinelOps Model Cleanup ==="

# Ensure legacy folder exists
mkdir -p app/models_legacy

echo "Moving dead models to app/models_legacy ..."

# ACTIVE MODELS (DO NOT MOVE)
ACTIVE=(
  "user.py"
  "session.py"
  "api_keys.py"
  "governance.py"
)

# Convert active list to lookup
ACTIVE_LOOKUP=$(printf "|%s" "${ACTIVE[@]}")
ACTIVE_LOOKUP=${ACTIVE_LOOKUP:1}

# Move *.bak models
for bak in app/models/*.bak; do
    if [[ -e "$bak" ]]; then
        echo "Moving backup model: $(basename "$bak")"
        mv "$bak" app/models_legacy/
    fi
done

# Move all non-active models
for file in app/models/*.py; do
    base=$(basename "$file")
    if [[ ! "$base" =~ ^($ACTIVE_LOOKUP)$ ]]; then
        echo "Moving dead model: $base"
        mv "$file" app/models_legacy/
    fi
done

echo "Cleanup complete."
