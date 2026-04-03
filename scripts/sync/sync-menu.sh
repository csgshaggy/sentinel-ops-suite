#!/bin/bash

# Color palette
RED="\e[31m"; GREEN="\e[32m"; YELLOW="\e[33m"; BLUE="\e[34m"; CYAN="\e[36m"; RESET="\e[0m"

while true; do
    clear
    echo -e "${CYAN}==========================================${RESET}"
    echo -e "${GREEN}        Sentinel Ops Sync Menu${RESET}"
    echo -e "${CYAN}==========================================${RESET}"
    echo -e "${YELLOW}1) Full Sync${RESET}"
    echo -e "${YELLOW}2) Dev Sync (governance only)${RESET}"
    echo -e "${YELLOW}3) Quick Sync (fastest)${RESET}"
    echo -e "${YELLOW}4) View Sync History${RESET}"
    echo -e "${YELLOW}5) Governance Summary${RESET}"
    echo -e "${YELLOW}6) Baseline Diff${RESET}"
    echo -e "${YELLOW}7) Baseline Rollback${RESET}"
    echo -e "${YELLOW}8) Baseline History Compare${RESET}"
    echo -e "${YELLOW}9) Baseline Dashboard${RESET}"
    echo -e "${YELLOW}10) Sync Analytics${RESET}"
    echo -e "${YELLOW}11) Exit${RESET}"
    echo -e "${CYAN}------------------------------------------${RESET}"
    read -p "Select an option: " choice

    case $choice in
        1) make sync ;;
        2) make dev-sync ;;
        3) make quick-sync ;;
        4) bash scripts/sync/view-sync-history.sh ;;
        5) bash scripts/sync/governance-summary.sh ;;
        6) make baseline-diff ;;
        7) make baseline-rollback ;;
        8) make baseline-history-compare ;;
        9) bash scripts/sync/baseline-dashboard.sh ;;
        10) bash scripts/sync/sync-analytics.sh ;;
        11) exit 0 ;;
        *) echo -e "${RED}Invalid option${RESET}"; sleep 1 ;;
    esac
done
