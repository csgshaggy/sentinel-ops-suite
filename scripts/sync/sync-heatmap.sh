#!/bin/bash

CYAN="\e[36m"; GREEN="\e[32m"; YELLOW="\e[33m"; RED="\e[31m"; RESET="\e[0m"

LOG="sync.log"

echo -e "${CYAN}==========================================${RESET}"
echo -e "${GREEN}              Sync Heatmap${RESET}"
echo -e "${CYAN}==========================================${RESET}"

if [ ! -f "$LOG" ]; then
    echo -e "${RED}No sync history found.${RESET}"
    exit 1
fi

echo -e "${YELLOW}Sync Frequency by Day (last 60 days):${RESET}"
echo

for DAY in {0..59}; do
    DATE=$(date -d "$DAY days ago" +%Y-%m-%d)
    COUNT=$(grep "$DATE" "$LOG" | wc -l)

    if [ "$COUNT" -eq 0 ]; then
        COLOR="$RED"
    elif [ "$COUNT" -lt 2 ]; then
        COLOR="$YELLOW"
    else
        COLOR="$GREEN"
    fi

    echo -e "$COLOR$DATE: $COUNT syncs${RESET}"
done

echo
read -p "Press Enter to return..."
