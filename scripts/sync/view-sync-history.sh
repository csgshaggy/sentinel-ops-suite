#!/bin/bash

CYAN="\e[36m"; GREEN="\e[32m"; RESET="\e[0m"

LOG="sync.log"

echo -e "${CYAN}==========================================${RESET}"
echo -e "${GREEN}        Sync History Viewer${RESET}"
echo -e "${CYAN}==========================================${RESET}"

if [ ! -f "$LOG" ]; then
    echo "ℹ️ No sync history found. Creating empty log..."
    touch "$LOG"
fi

tail -n 200 "$LOG"

echo
read -p "Press Enter to return..."
