#!/usr/bin/env bash
set -euo pipefail

required=(
  "app/main.py"
  "tools/plugins/pelm.py"
  "tests/pelm"
  "docs"
  "_config.yml"
)

for path in "${required[@]}"; do
  if [ ! -e "$path" ]; then
    echo "[structure] ERROR: Missing required path: $path"
    exit 1
  fi
done

echo "[structure] OK"
