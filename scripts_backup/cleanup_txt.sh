#!/usr/bin/env bash
set -euo pipefail

# Chain banner
echo -e "\n\033[1;36m[CHAIN] Running: $(basename "$0")\033[0m"

echo "[cleanup_txt] Starting cleanup of stray .txt files and temp artifacts..."

# Resolve script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

TARGETS=(
    "$PROJECT_ROOT"
    "$PROJECT_ROOT/frontend"
    "$PROJECT_ROOT/backend"
)

echo "[cleanup_txt] Scanning project directories..."

# Remove stray .txt files except README or LICENSE
for dir in "${TARGETS[@]}"; do
    if [[ -d "$dir" ]]; then
        echo "[cleanup_txt] Checking: $dir"
        find "$dir" -maxdepth 3 -type f -name "*.txt" \
            ! -iname "readme.txt" \
            ! -iname "license.txt" \
            -print -exec rm -f {} \;
    fi
done

# Remove temp files
echo "[cleanup_txt] Removing temporary files (*.tmp, *.bak, *~)..."
find "$PROJECT_ROOT" -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*~" \) \
    -print -exec rm -f {} \;

# Normalize whitespace in .md and .sh files
echo "[cleanup_txt] Normalizing whitespace in Markdown and shell scripts..."
find "$PROJECT_ROOT" -type f \( -name "*.md" -o -name "*.sh" \) | while read -r file; do
    sed -i 's/[ \t]*$//' "$file"   # remove trailing whitespace
done

echo "[cleanup_txt] Cleanup complete."
