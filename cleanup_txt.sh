#!/bin/bash

echo "Scanning for unnecessary .txt files..."

KEEP=("requirements.txt" "requirements-dev.txt")

for file in *.txt; do
    skip=false
    for keep in "${KEEP[@]}"; do
        if [[ "$file" == "$keep" ]]; then
            skip=true
            break
        fi
    done

    if [[ "$skip" == false ]]; then
        echo "Deleting: $file"
        rm "$file"
    else
        echo "Keeping:  $file"
    fi
done

echo "Cleanup complete."
