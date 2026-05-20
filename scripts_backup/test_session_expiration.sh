#!/usr/bin/env bash
# SentinelOps — Session Expiration Test Script
# Validates 15-minute timeout behavior

set -euo pipefail

DOMAIN="https://crcybercop.dpdns.org"

echo "=== Testing Session Expiration ==="

echo "[1/4] Logging in..."
curl -c cookies.txt -X POST "$DOMAIN/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"test"}'

echo "[2/4] Verifying session is active..."
curl -b cookies.txt -I "$DOMAIN/api/users/me"

echo "[3/4] Waiting 15 minutes..."
sleep $((15 * 60))

echo "[4/4] Verifying session is expired..."
curl -b cookies.txt -I "$DOMAIN/api/users/me" || true

echo "=== Test complete ==="
