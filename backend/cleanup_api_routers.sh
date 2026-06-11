#!/bin/bash
set -e

echo "=== SentinelOps API Router Cleanup ==="

# Ensure legacy folder exists
mkdir -p app/api_legacy

echo "Moving dead API routers to app/api_legacy ..."

# Loop through actual directory entries
for item in $(ls -1 app/api); do
    # Skip __pycache__
    if [[ "$item" == "__pycache__" ]]; then
        continue
    fi

    echo "Moving: $item"
    mv "app/api/$item" app/api_legacy/
done

echo "Cleanup complete."
