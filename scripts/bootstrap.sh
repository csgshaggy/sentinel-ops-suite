#!/usr/bin/env bash
set -e

GREEN="\033[1;32m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
RESET="\033[0m"

echo -e "${BLUE}=== Bootstrapping SSRF Console Project Structure ===${RESET}"

# Directories
DIRS=(
    "scripts"
    "tools"
    "tools/plugins"
    "backend"
)

for d in "${DIRS[@]}"; do
    if [[ ! -d "$d" ]]; then
        mkdir -p "$d"
        echo -e "${GREEN}[OK]${RESET} Created directory: $d"
    else
        echo -e "${YELLOW}[SKIP]${RESET} Directory already exists: $d"
    fi
done

# Mode file
if [[ ! -f ".superdoctor_mode" ]]; then
    echo "balanced" > .superdoctor_mode
    echo -e "${GREEN}[OK]${RESET} Created .superdoctor_mode"
else
    echo -e "${YELLOW}[SKIP]${RESET} .superdoctor_mode already exists"
fi

# Makefile placeholder
if [[ ! -f "Makefile" ]]; then
    echo -e "${YELLOW}[WARN]${RESET} No Makefile found. Creating placeholder."
    cat > Makefile <<EOF
# Placeholder Makefile — replace with full version
help:
\t@echo "Replace this Makefile with your full operator-grade version."
EOF
    echo -e "${GREEN}[OK]${RESET} Created placeholder Makefile"
else
    echo -e "${YELLOW}[SKIP]${RESET} Makefile already exists"
fi

echo -e "${BLUE}=== Bootstrap Complete ===${RESET}"
