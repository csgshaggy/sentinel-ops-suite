#!/bin/bash

RED="\e[31m"; GREEN="\e[32m"; YELLOW="\e[33m"; BLUE="\e[34m"; CYAN="\e[36m"; RESET="\e[0m"

BASELINE=".meta/makefile/Makefile.baseline"
HISTORY_DIR=".meta/makefile/history"

echo -e "${CYAN}==========================================${RESET}"
echo -e "${GREEN}        Baseline Dashboard${RESET}"
echo -e "${CYAN}==========================================${RESET}"

if [ ! -f "$BASELINE" ]; then
    echo -e "${RED}❌ No baseline found.${RESET}"
    exit 1
fi

LAST_UPDATE=$(stat -c %y "$BASELINE" | cut -d'.' -f1)
HISTORY_COUNT=$(ls "$HISTORY_DIR" | wc -l)

# Drift status
node scripts/make/makefile-drift-check.cjs --status-only
DRIFT=$?

if [ "$DRIFT" -eq 0 ]; then
    DRIFT_STATUS="${GREEN}No Drift Detected${RESET}"
else
    DRIFT_STATUS="${YELLOW}Drift Present${RESET}"
fi

echo -e "${BLUE}Baseline Last Updated:${RESET} $LAST_UPDATE"
echo -e "${BLUE}History Snapshots:${RESET} $HISTORY_COUNT"
echo -e "${BLUE}Drift Status:${RESET} $DRIFT_STATUS"

echo
read -p "Press Enter to return..."
