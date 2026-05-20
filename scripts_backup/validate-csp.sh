#!/usr/bin/env bash
set -euo pipefail

SENTINEL_CONF="/etc/nginx/sites-available/sentinel"

echo "[CSP] Validating CSP header formatting..."

# Extract the CSP line exactly as NGINX will read it
CSP_LINE=$(grep -E 'add_header[[:space:]]+Content-Security-Policy' "$SENTINEL_CONF" || true)

if [ -z "$CSP_LINE" ]; then
    echo "[ERROR] CSP header not found in sentinel config."
    exit 1
fi

# Check for line breaks in the CSP block
MULTILINE_COUNT=$(grep -n "Content-Security-Policy" -A5 "$SENTINEL_CONF" | grep -E '^[[:space:]]+"' | wc -l)

if [ "$MULTILINE_COUNT" -gt 0 ]; then
    echo "[ERROR] CSP appears to be MULTILINE — this will break HTTP/2."
    exit 1
fi

# Check for trailing whitespace
if echo "$CSP_LINE" | grep -qE '[[:space:]]+$'; then
    echo "[ERROR] CSP line has trailing whitespace — unsafe for HTTP/2."
    exit 1
fi

# Check for folded header (line starting with whitespace after CSP)
if grep -n "Content-Security-Policy" -A1 "$SENTINEL_CONF" | sed -n '2p' | grep -qE '^[[:space:]]+'; then
    echo "[ERROR] CSP header is folded onto the next line — invalid for HTTP/2."
    exit 1
fi

echo "[CSP] CSP formatting is valid and HTTP/2-safe."
