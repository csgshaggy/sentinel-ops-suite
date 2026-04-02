#!/bin/bash

# Sentinel Ops Suite — Sync Menu (TUI)

while true; do
    clear
    echo "=========================================="
    echo "        Sentinel Ops Sync Menu"
    echo "=========================================="
    echo "1) Full Sync"
    echo "2) Dev Sync (governance only)"
    echo "3) Quick Sync (fastest)"
    echo "4) View Sync History"
    echo "5) Governance Summary"
    echo "6) Update Makefile Baseline"
    echo "7) Exit"
    echo "------------------------------------------"
    read -p "Select an option: " choice

    case $choice in
        1) make sync ;;
        2) make dev-sync ;;
        3) make quick-sync ;;
        4) scripts/sync/view-sync-history.sh ;;
        5) scripts/sync/governance-summary.sh ;;
        6) make update-makefile-baseline ;;
        7) exit 0 ;;
        *) echo "Invalid option"; sleep 1 ;;
    esac
done
