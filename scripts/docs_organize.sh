#!/usr/bin/env bash
set -euo pipefail

# ----------------------------------------
# Color helpers
# ----------------------------------------
blue()  { printf "\033[34m%s\033[0m\n" "$1"; }
green() { printf "\033[32m%s\033[0m\n" "$1"; }
yellow(){ printf "\033[33m%s\033[0m\n" "$1"; }
red()   { printf "\033[31m%s\033[0m\n" "$1"; }

# ----------------------------------------
# Resolve paths
# ----------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOCS_DIR="$PROJECT_ROOT/docs"
MAP_FILE="$DOCS_DIR/category_map.json"
LOG_FILE="$PROJECT_ROOT/docs_organize.log"

echo "=== Documentation Organizer ===" | tee "$LOG_FILE"
echo "Timestamp: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# ----------------------------------------
# Prerequisite checks
# ----------------------------------------
if [[ ! -d "$DOCS_DIR" ]]; then
  red "ERROR: docs/ directory not found at: $DOCS_DIR"
  exit 1
fi

if [[ ! -f "$MAP_FILE" ]]; then
  red "ERROR: category_map.json not found at: $MAP_FILE"
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  red "ERROR: jq is required but not installed."
  exit 1
fi

blue "[OK] Environment validated."
echo "" | tee -a "$LOG_FILE"

# ----------------------------------------
# Load categories
# ----------------------------------------
categories=$(jq -r 'keys[]' "$MAP_FILE")

# ----------------------------------------
# 1. Create category directories
# ----------------------------------------
blue "[1/3] Creating category directories..." | tee -a "$LOG_FILE"

for category in $categories; do
  target="$DOCS_DIR/$category"
  if [[ ! -d "$target" ]]; then
    mkdir -p "$target"
    green "[CREATE] $category/" | tee -a "$LOG_FILE"
  else
    yellow "[EXISTS] $category/" | tee -a "$LOG_FILE"
  fi
done

echo "" | tee -a "$LOG_FILE"

# ----------------------------------------
# 2. Move mapped files into correct directories
# ----------------------------------------
blue "[2/3] Moving mapped files..." | tee -a "$LOG_FILE"

for category in $categories; do
  files=$(jq -r --arg cat "$category" '.[$cat][]' "$MAP_FILE")

  for file in $files; do
    src="$DOCS_DIR/$file"
    dest="$DOCS_DIR/$category/$file"

    if [[ -f "$src" ]]; then
      mv "$src" "$dest"
      green "[MOVE] $file → $category/" | tee -a "$LOG_FILE"
    else
      yellow "[WARN] Missing file: $file (expected at docs/)" | tee -a "$LOG_FILE"
    fi
  done
done

echo "" | tee -a "$LOG_FILE"

# ----------------------------------------
# 3. Detect unmapped Markdown files
# ----------------------------------------
blue "[3/3] Checking for unmapped Markdown files..." | tee -a "$LOG_FILE"

mapped=$(jq -r '.[][]' "$MAP_FILE")
unmapped_count=0

while IFS= read -r file; do
  filename=$(basename "$file")

  if ! grep -qx "$filename" <<< "$mapped"; then
    yellow "[UNMAPPED] $file" | tee -a "$LOG_FILE"
    unmapped_count=$((unmapped_count + 1))
  fi
done < <(find "$DOCS_DIR" -maxdepth 1 -type f -name "*.md")

if (( unmapped_count > 0 )); then
  yellow "Unmapped files detected: $unmapped_count" | tee -a "$LOG_FILE"
else
  green "No unmapped files." | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
green "=== Documentation Organization Complete ===" | tee -a "$LOG_FILE"
