#!/usr/bin/env bash
set -e

# ============================================
#  SuperDoctor CLI Installer
# ============================================

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS_DIR="$PROJECT_ROOT/tools"
WRAPPER="$TOOLS_DIR/superdoctor"
SYMLINK="$HOME/.local/bin/superdoctor"
MODE_FILE="$PROJECT_ROOT/.superdoctor_mode"

GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
BLUE="\033[1;34m"
RESET="\033[0m"

echo -e "${BLUE}=== Installing SuperDoctor CLI ===${RESET}"

mkdir -p "$TOOLS_DIR"

# --------------------------------------------
# Create CLI wrapper
# --------------------------------------------
echo -e "${YELLOW}[..] Creating CLI wrapper...${RESET}"

cat > "$WRAPPER" << 'EOF'
#!/usr/bin/env bash

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE_FILE="$PROJECT_ROOT/.superdoctor_mode"

GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
RESET="\033[0m"

if [[ ! -f "$MODE_FILE" ]]; then
    echo "balanced" > "$MODE_FILE"
fi

cmd="$1"
arg="$2"

case "$cmd" in
    run)
        python3 "$PROJECT_ROOT/tools/super_doctor.py"
        ;;
    report)
        python3 "$PROJECT_ROOT/tools/super_doctor.py" --report
        ;;
    dashboard)
        python3 "$PROJECT_ROOT/tools/super_doctor.py" --dashboard
        ;;
    mode)
        if [[ "$arg" == "strict" || "$arg" == "balanced" ]]; then
            echo "$arg" > "$MODE_FILE"
            echo -e "${GREEN}Mode set to: $arg${RESET}"
        else
            echo -e "${RED}Invalid mode. Use: strict | balanced${RESET}"
        fi
        ;;
    show)
        echo -e "${GREEN}Current mode: $(cat "$MODE_FILE")${RESET}"
        ;;
    doctor)
        python3 "$PROJECT_ROOT/tools/tui_menu.py"
        ;;
    *)
        echo -e "${YELLOW}SuperDoctor CLI${RESET}"
        echo "Usage:"
        echo "  superdoctor run"
        echo "  superdoctor report"
        echo "  superdoctor dashboard"
        echo "  superdoctor mode strict|balanced"
        echo "  superdoctor show"
        echo "  superdoctor doctor"
        ;;
esac
EOF

chmod +x "$WRAPPER"
echo -e "${GREEN}[OK] CLI wrapper created${RESET}"

# --------------------------------------------
# Create symlink
# --------------------------------------------
mkdir -p "$HOME/.local/bin"

if [[ -L "$SYMLINK" || -f "$SYMLINK" ]]; then
    rm -f "$SYMLINK"
fi

ln -s "$WRAPPER" "$SYMLINK"
echo -e "${GREEN}[OK] Symlink created at $SYMLINK${RESET}"

# --------------------------------------------
# PATH check
# --------------------------------------------
if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
    echo -e "${GREEN}[OK] ~/.local/bin is in PATH${RESET}"
else
    echo -e "${YELLOW}[WARN] ~/.local/bin is NOT in PATH${RESET}"
    echo "Add this to your shell config:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo -e "${BLUE}=== Installation Complete ===${RESET}"
