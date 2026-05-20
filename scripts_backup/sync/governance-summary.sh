#!/bin/bash

RED="\e[31m"; GREEN="\e[32m"; BLUE="\e[34m"; RESET="\e[0m"

echo -e "${BLUE}==========================================${RESET}"
echo -e "${GREEN}        Governance Summary Report${RESET}"
echo -e "${BLUE}==========================================${RESET}"

echo -e "\n🔐 MFA Check:"
node scripts/governance/governance-mfa-check.cjs || echo -e "${RED}⚠️ MFA check failed${RESET}"

echo -e "\n📁 Structure Check:"
node scripts/governance/governance-structure-check.cjs || echo -e "${RED}⚠️ Structure check failed${RESET}"

echo -e "\n📚 Docs Check:"
node scripts/governance/governance-docs-check.cjs || echo -e "${RED}⚠️ Docs check failed${RESET}"

echo -e "\n📦 Dependency Check:"
node scripts/governance/governance-deps-check.cjs || echo -e "${RED}⚠️ Dependency check failed${RESET}"

echo -e "\n🧩 Makefile Validation:"
node scripts/make/validate-makefile.cjs || echo -e "${RED}⚠️ Makefile validation failed${RESET}"

echo
read -p "Press Enter to return..."
