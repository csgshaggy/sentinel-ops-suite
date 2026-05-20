# ────────────────────────────────────────────────────────────────
#  Sentinel Ops Suite — Cross-Shell Init (Bash/Zsh)
# ────────────────────────────────────────────────────────────────

RED="\033[31m"; GREEN="\033[32m"; YELLOW="\033[33m"
BLUE="\033[34m"; MAGENTA="\033[35m"; CYAN="\033[36m"
RESET="\033[0m"

PROJECT_DIR="$HOME/sentinel-ops-suite"
VENV_DIR="$PROJECT_DIR/venv"

case "$-" in *i*) _INTERACTIVE=1 ;; *) _INTERACTIVE=0 ;; esac

if [ "$_INTERACTIVE" -eq 1 ]; then
    printf "%b\n" "${BLUE}┌──────────────────────────────────────────────┐${RESET}"
    printf "%b\n" "${BLUE}│${RESET}  ${CYAN}Sentinel Ops Suite — Environment Init${RESET}  ${BLUE}│${RESET}"
    printf "%b\n" "${BLUE}└──────────────────────────────────────────────┘${RESET}"

    if [ -d "$PROJECT_DIR" ]; then
        printf "%b\n" "${GREEN}[OK]${RESET} Project directory: ${CYAN}$PROJECT_DIR${RESET}"
        cd "$PROJECT_DIR" 2>/dev/null || :
    else
        printf "%b\n" "${YELLOW}[WARN]${RESET} Missing: ${RED}$PROJECT_DIR${RESET}"
    fi

    if [ -d "$VENV_DIR" ]; then
        printf "%b\n" "${GREEN}[OK]${RESET} Activating venv"
        . "$VENV_DIR/bin/activate" 2>/dev/null
    else
        printf "%b\n" "${YELLOW}[WARN]${RESET} No venv at: ${RED}$VENV_DIR${RESET}"
    fi

    printf "%b\n" "${MAGENTA}Environment initialization complete.${RESET}"
    printf "\n"
fi
