#!/usr/bin/env bash

source "$(dirname "$0")/banner.sh"

PORTS=${@:-"8000 8080 5000 3000"}

echo -e "[KILL] Attempting to free ports: $PORTS"
echo ""

for PORT in $PORTS; do
    PIDS=$(lsof -t -i :$PORT)
    if [ -n "$PIDS" ]; then
        echo -e "[KILL] Killing processes on port $PORT"
        kill -9 $PIDS
    else
        echo -e "[OK] Port $PORT already free"
    fi
done
