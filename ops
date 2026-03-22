#!/usr/bin/env bash

OS="$(uname -s)"

if [[ "$OS" == "Linux" || "$OS" == "Darwin" ]]; then
    scripts/ops_menu.sh
else
    powershell -ExecutionPolicy Bypass -File scripts/windows/doctor.ps1
fi
