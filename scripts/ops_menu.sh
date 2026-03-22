#!/usr/bin/env bash

source "$(dirname "$0")/banner.sh"

while true; do
    echo ""
    echo -e "Select an operation:"
    echo -e "  1) Environment Info"
    echo -e "  2) Project Tree"
    echo -e "  3) Check Ports"
    echo -e "  4) Kill Ports"
    echo -e "  5) Doctor (Full Health Check)"
    echo -e "  6) Exit"
    echo ""

    read -p "Choice: " choice

    case $choice in
        1) scripts/env_info.sh ;;
        2) scripts/project_tree.sh ;;
        3) scripts/check_ports.sh ;;
        4) scripts/kill_ports.sh ;;
        5) scripts/doctor.sh ;;
        6) exit 0 ;;
        *) echo -e "[ERROR] Invalid choice" ;;
    esac
done
