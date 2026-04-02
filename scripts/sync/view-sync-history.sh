#!/bin/bash

LOG_FILE="sync.log"

if [ ! -f "$LOG_FILE" ]; then
    echo "ℹ️ No sync history found. Creating empty log..."
    touch "$LOG_FILE"
fi

echo "=========================================="
echo "        Sync History Viewer"
echo "=========================================="
echo

tail -n 200 "$LOG_FILE"
echo
read -p "Press Enter to return to menu..."
