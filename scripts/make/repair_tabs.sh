#!/usr/bin/env bash
set -euo pipefail

FILE="Makefile"

# Convert leading spaces to a single TAB on recipe lines
# A recipe line is any line that begins with spaces followed by @ or a command
sed -i -E 's/^[ ]+(@|\S)/\t\1/' "$FILE"

# Remove stray CRLF or Unicode whitespace
sed -i 's/\r$//' "$FILE"
LC_ALL=C sed -i 's/[^[:print:]\t]//g' "$FILE"
