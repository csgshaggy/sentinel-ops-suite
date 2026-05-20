#!/bin/bash

GREEN="\e[32m"; RED="\e[31m"; YELLOW="\e[33m"; CYAN="\e[36m"; RESET="\e[0m"

echo -e "${CYAN}==========================================${RESET}"
echo -e "${GREEN}            Governance Score${RESET}"
echo -e "${CYAN}==========================================${RESET}"

SCORE=0
TOTAL=5

echo -e "\n🔐 MFA Check:"
node scripts/governance/governance-mfa-check.cjs && SCORE=$((SCORE+1))

echo -e "\n📁 Structure Check:"
node scripts/governance/governance-structure-check.cjs && SCORE=$((SCORE+1))

echo -e "\n📚 Docs Check:"
node scripts/governance/governance-docs-check.cjs && SCORE=$((SCORE+1))

echo -e "\n📦 Dependency Check:"
node scripts/governance/governance-deps-check.cjs && SCORE=$((SCORE+1))

echo -e "\n🧩 Makefile Validation:"
node scripts/make/validate-makefile.cjs && SCORE=$((SCORE+1))

echo -e "\n${YELLOW}Final Score:${RESET} $SCORE / $TOTAL"

if [ "$SCORE" -eq "$TOTAL" ]; then
    echo -e "${GREEN}✔ Governance is fully compliant${RESET}"
else
    echo -e "${RED}⚠ Governance issues detected${RESET}"
fi

echo
read -p "Press Enter to return..."

