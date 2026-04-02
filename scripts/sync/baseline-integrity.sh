#!/bin/bash

GREEN="\e[32m"; RED="\e[31m"; CYAN="\e[36m"; RESET="\e[0m"

BASELINE=".meta/makefile/Makefile.baseline"
HISTORY_DIR=".meta/makefile/history"

echo -e "${CYAN}==========================================${RESET}"
echo -e "${GREEN}        Baseline Integrity Checker${RESET}"
echo -e "${CYAN}==========================================${RESET}"

if [ ! -f "$BASELINE" ]; then
    echo -e "${RED}❌ No baseline found.${RESET}"
    exit 1
fi

if [ ! -d "$HISTORY_DIR" ]; then
    echo -e "${RED}❌ No baseline history directory found.${RESET}"
    exit 1
fi

LATEST=$(ls -t "$HISTORY_DIR" | head -n 1)

if [ -z "$LATEST" ]; then
    echo -e "${RED}❌ No baseline history snapshots found.${RESET}"
    exit 1
fi

echo -e "${CYAN}Comparing current baseline to last snapshot:${RESET}"
echo -e "Snapshot: $LATEST"
echo

diff -u "$HISTORY_DIR/$LATEST" "$BASELINE" || true

echo
echo -e "${GREEN}✔ Integrity check complete${RESET}"
echo
read -p "Press Enter to return..."
