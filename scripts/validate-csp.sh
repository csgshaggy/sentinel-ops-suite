#!/usr/bin/env bash
set -euo pipefail

SENTINEL_CONF="/etc/nginx/sites-available/sentinel"

echo "[CSP] Validating CSP header formatting..."

CSP_LINE=$(grep -E 'add_header[[:space:]]+Content-Security-Policy' "$SENTINEL_CONF" || true)

if [ -z "$CSP_LINE" ]; then
    echo "[ERROR] CSP header not found in sentinel config."
    exit 1
fi

MULTILINE_COUNT=$(grep -n "Content-Security-Policy" -A5 "$SENTINEL_CONF" | grep -E '^[[:space:]]+"' || true | wc -l)


if [ "$MULTILINE_COUNT" -gt 0 ]; then
    echo "[ERROR] CSP appears to be MULTILINE — this will break HTTP/2."
    exit 1
fi

if echo "$CSP_LINE" | grep -qE '[[:space:]]+$'; then
    echo "[ERROR] CSP line has trailing whitespace — unsafe for HTTP/2."
    exit 1
fi

if grep -n "Content-Security-Policy" -A1 "$SENTINEL_CONF" | sed -n '2p' | grep -qE '^[[:space:]]+' || false; then
    echo "[ERROR] CSP header is folded onto the next line — invalid for HTTP/2."
    exit 1
fi

echo "[CSP] CSP formatting is valid and HTTP/2-safe."
exit 0
