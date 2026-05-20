#!/usr/bin/env bash
set -euo pipefail

CONF="/etc/nginx/sites-available/sentinel"

echo "[HEADERS] Scanning for HTTP/2‑forbidden folded headers..."

# Find any line that starts with add_header
HEADER_LINES=$(grep -n "add_header" "$CONF" | cut -d: -f1)

if [ -z "$HEADER_LINES" ]; then
    echo "[ERROR] No add_header directives found — unexpected."
    exit 1
fi

BAD=0

while read -r LINE; do
    NEXT_LINE=$((LINE + 1))

    # Extract next line
    CONTENT=$(sed -n "${NEXT_LINE}p" "$CONF")

    # If next line begins with whitespace, it's a folded header
    if echo "$CONTENT" | grep -qE '^[[:space:]]+"'; then
        echo "[ERROR] Folded header detected at line $LINE → next line begins with whitespace."
        echo "        This will break HTTP/2."
        BAD=1
    fi
done <<< "$HEADER_LINES"

if [ "$BAD" -eq 1 ]; then
    echo "[HEADERS] Folding errors detected — fix required."
    exit 1
fi

echo "[HEADERS] No folded headers detected. Safe for HTTP/2."

