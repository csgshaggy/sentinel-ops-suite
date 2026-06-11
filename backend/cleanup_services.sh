#!/bin/bash
set -e

echo "=== SentinelOps Service Cleanup ==="

# Ensure legacy folder exists
mkdir -p app/services_legacy

echo "Moving dead services to app/services_legacy ..."

# ACTIVE SERVICES (DO NOT MOVE)
ACTIVE=(
  "governance_service.py"
  "session_service.py"
)

# Convert active list to lookup
ACTIVE_LOOKUP=$(printf "|%s" "${ACTIVE[@]}")
ACTIVE_LOOKUP=${ACTIVE_LOOKUP:1}

# Move *.bak services
for bak in app/services/*.bak; do
    if [[ -e "$bak" ]]; then
        echo "Moving backup service: $(basename "$bak")"
        mv "$bak" app/services_legacy/
    fi
done

# Move all non-active services
for file in app/services/*.py; do
    base=$(basename "$file")
    if [[ ! "$base" =~ ^($ACTIVE_LOOKUP)$ ]]; then
        echo "Moving dead service: $base"
        mv "$file" app/services_legacy/
    fi
done

echo "Cleanup complete."
