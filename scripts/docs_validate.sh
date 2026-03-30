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

blue "=== Documentation Validator ==="
blue "Project root: $PROJECT_ROOT"
blue "Docs directory: $DOCS_DIR"
echo ""

# ----------------------------------------
# Load categories
# ----------------------------------------
categories=$(jq -r 'keys[]' "$MAP_FILE")

# ----------------------------------------
# 1. Validate category directories
# ----------------------------------------
blue "[1/4] Validating category directories..."

missing_dirs=0
for category in $categories; do
  if [[ ! -d "$DOCS_DIR/$category" ]]; then
    red "[MISSING] Directory: $category/"
    missing_dirs=$((missing_dirs + 1))
  else
    green "[OK] $category/"
  fi
done

if (( missing_dirs > 0 )); then
  red "ERROR: Missing category directories: $missing_dirs"
  exit 1
fi

echo ""

# ----------------------------------------
# 2. Validate mapped files exist
# ----------------------------------------
blue "[2/4] Validating mapped files..."

missing_files=0

for category in $categories; do
  files=$(jq -r --arg cat "$category" '.[$cat][]' "$MAP_FILE")

  for file in $files; do
    if [[ ! -f "$DOCS_DIR/$category/$file" ]]; then
      red "[MISSING] $category/$file"
      missing_files=$((missing_files + 1))
    else
      green "[OK] $category/$file"
    fi
  done
done

if (( missing_files > 0 )); then
  red "ERROR: Missing mapped files: $missing_files"
  exit 1
fi

echo ""

# ----------------------------------------
# 3. Detect misplaced mapped files
# ----------------------------------------
blue "[3/4] Checking for misplaced mapped files..."

misplaced=0

for category in $categories; do
  files=$(jq -r --arg cat "$category" '.[$cat][]' "$MAP_FILE")

  for file in $files; do
    # Search for file anywhere under docs/
    found_paths=$(find "$DOCS_DIR" -type f -name "$file")

    while IFS= read -r path; do
      expected="$DOCS_DIR/$category/$file"
      if [[ "$path" != "$expected" ]]; then
        red "[MISPLACED] $file found at: $path (expected: $expected)"
        misplaced=$((misplaced + 1))
      fi
    done <<< "$found_paths"
  done
done

if (( misplaced > 0 )); then
  red "ERROR: Misplaced files detected: $misplaced"
  exit 1
fi

echo ""

# ----------------------------------------
# 4. Detect unmapped Markdown files
# ----------------------------------------
blue "[4/4] Checking for unmapped Markdown files..."

mapped_files=$(jq -r '.[][]' "$MAP_FILE")
unmapped=0

while IFS= read -r file; do
  filename=$(basename "$file")

  if ! grep -qx "$filename" <<< "$mapped_files"; then
    yellow "[UNMAPPED] $file"
    unmapped=$((unmapped + 1))
  fi
done < <(find "$DOCS_DIR" -type f -name "*.md")

echo ""
green "Validation complete."

if (( unmapped > 0 )); then
  yellow "Warning: $unmapped unmapped Markdown files detected."
fi
