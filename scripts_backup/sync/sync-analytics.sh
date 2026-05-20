#!/bin/bash

RED="\e[31m"; GREEN="\e[32m"; YELLOW="\e[33m"; BLUE="\e[34m"; CYAN="\e[36m"; RESET="\e[0m"

LOG="sync.log"

echo -e "${CYAN}==========================================${RESET}"
echo -e "${GREEN}        Sync Analytics${RESET}"
echo -e "${CYAN}==========================================${RESET}"

if [ ! -f "$LOG" ]; then
    echo -e "${RED}No sync history found.${RESET}"
    exit 1
fi

TOTAL=$(cat "$LOG" | wc -l)
LAST=$(tail -n 1 "$LOG" | cut -d'|' -f1)
MONTH=$(grep "$(date +%Y-%m)" "$LOG" | wc -l)
WEEK=$(grep "$(date +%Y-%m-%d -d 'last 7 days')" "$LOG" | wc -l)

echo -e "${BLUE}Total Syncs:${RESET} $TOTAL"
echo -e "${BLUE}Last Sync:${RESET} $LAST"
echo -e "${BLUE}Syncs This Month:${RESET} $MONTH"
echo -e "${BLUE}Syncs Last 7 Days:${RESET} $WEEK"

echo
read -p "Press Enter to return..."
