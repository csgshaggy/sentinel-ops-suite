#!/usr/bin/env bash
# SentinelOps — End‑to‑End Login Test Script
# Validates: login → session cookie → protected route → logout → session invalidation

set -euo pipefail

DOMAIN="https://crcybercop.dpdns.org"
COOKIE_JAR="e2e_cookies.txt"

echo "=== SentinelOps E2E Login Test ==="

# ---------------------------------------------------------------------------
# 1. CLEANUP
# ---------------------------------------------------------------------------
rm -f "$COOKIE_JAR"

# ---------------------------------------------------------------------------
# 2. LOGIN
# ---------------------------------------------------------------------------
echo "[1/5] Logging in..."
LOGIN_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
  -c "$COOKIE_JAR" \
  -X POST "$DOMAIN/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test"}')

if [[ "$LOGIN_RESPONSE" != "200" ]]; then
  echo "ERROR: Login failed (HTTP $LOGIN_RESPONSE)"
  exit 1
fi

echo "Login successful."

# ---------------------------------------------------------------------------
# 3. ACCESS PROTECTED ROUTE
# ---------------------------------------------------------------------------
echo "[2/5] Accessing protected route /api/users/me..."
ME_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
  -b "$COOKIE_JAR" \
  "$DOMAIN/api/users/me")

if [[ "$ME_RESPONSE" != "200" ]]; then
  echo "ERROR: Protected route failed (HTTP $ME_RESPONSE)"
  exit 1
fi

echo "Protected route access successful."

# ---------------------------------------------------------------------------
# 4. LOGOUT
# ---------------------------------------------------------------------------
echo "[3/5] Logging out..."
LOGOUT_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
  -b "$COOKIE_JAR" \
  -X POST "$DOMAIN/auth/logout")

if [[ "$LOGOUT_RESPONSE" != "200" ]]; then
  echo "ERROR: Logout failed (HTTP $LOGOUT_RESPONSE)"
  exit 1
fi

echo "Logout successful."

# ---------------------------------------------------------------------------
# 5. VERIFY SESSION INVALIDATION
# ---------------------------------------------------------------------------
echo "[4/5] Verifying session is invalid after logout..."
POST_LOGOUT_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
  -b "$COOKIE_JAR" \
  "$DOMAIN/api/users/me")

if [[ "$POST_LOGOUT_RESPONSE" == "200" ]]; then
  echo "ERROR: Session still valid after logout — expected 401"
  exit 1
fi

if [[ "$POST_LOGOUT_RESPONSE" != "401" ]]; then
  echo "ERROR: Unexpected response after logout (HTTP $POST_LOGOUT_RESPONSE)"
  exit 1
fi

echo "Session invalidation confirmed."

# ---------------------------------------------------------------------------
# 6. SUCCESS
# ---------------------------------------------------------------------------
echo "[5/5] E2E login test completed successfully."
echo "=== All checks passed ==="
