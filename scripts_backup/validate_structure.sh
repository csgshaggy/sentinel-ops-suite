#!/usr/bin/env bash
set -e

RED="\033[0;31m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
NC="\033[0m"

echo -e "${BLUE}[STRUCTURE] Validating monorepo layout...${NC}"

REQUIRED_DIRS=(
  "backend"
  "backend/src"
  "backend/src/ssrf_command_console"
  "frontend"
  "frontend/src"
)

for d in "${REQUIRED_DIRS[@]}"; do
  if [ ! -d "$d" ]; then
    echo -e "${RED}[STRUCTURE] MISSING: $d${NC}"
    exit 1
  fi
done

echo -e "${GREEN}[STRUCTURE] OK${NC}"
exit 0
