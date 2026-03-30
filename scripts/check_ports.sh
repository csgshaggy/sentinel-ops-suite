#!/usr/bin/env bash

source "$(dirname "$0")/banner.sh"

PORTS=${@:-"8000 8080 5000 3000"}

echo -e "[PORTS] Checking ports: $PORTS"
echo ""

for PORT in $PORTS; do
    if lsof -i :$PORT >/dev/null 2>&1; then
        echo -e "[BUSY] Port $PORT is in use:"
        lsof -i :$PORT | sed 's/^/    /'
    else
        echo -e "[FREE] Port $PORT is available"
    fi
done
