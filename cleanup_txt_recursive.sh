#!/bin/bash

# SentinelOps — Recursive TXT Cleanup Script (Safe Edition)

ROOT_DIR="$(pwd)"

echo "Starting recursive cleanup in: $ROOT_DIR"
echo

# Files to keep (exact names)
KEEP_FILES=(
    "requirements.txt"
    "requirements-dev.txt"
)

# Directories to skip entirely
SKIP_DIRS=(
    ".git"
    ".github"
    "node_modules"
    "dist"
    "build"
    "venv"
    ".venv"
    "__pycache__"
)

should_skip_dir() {
    for skip in "${SKIP_DIRS[@]}"; do
        if [[ "$1" == *"/$skip"* ]]; then
            return 0
        fi
    done
    return 1
}

should_keep_file() {
    filename=$(basename "$1")
    for keep in "${KEEP_FILES[@]}"; do
        if [[ "$filename" == "$keep" ]]; then
            return 0
        fi
    done
    return 1
}

echo "Scanning for .txt files..."
echo

find "$ROOT_DIR" -type f -name "*.txt" | while read -r file; do
    # Skip protected directories
    if should_skip_dir "$file"; then
        echo "Skipping (dir protected): $file"
        continue
    fi

    # Keep important files
    if should_keep_file "$file"; then
        echo "Keeping: $file"
        continue
    fi

    echo "Deleting: $file"
    rm -f "$file"
done

echo
echo "Cleanup complete."
