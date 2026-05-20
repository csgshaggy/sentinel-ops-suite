#!/usr/bin/env bash
set -euo pipefail

BASE="http://127.0.0.1:8000"
COOKIE_JAR="/tmp/sentinel_cookies.txt"

echo "=== SentinelOps Backend Regression Test Suite ==="
echo

rm -f "$COOKIE_JAR"

# ---------------------------------------------------------
# 1. Health Check
# ---------------------------------------------------------
echo "[1] Health Check"
curl -s "$BASE/health"
echo -e "\n"

# ---------------------------------------------------------
# 2. OpenAPI Check
# ---------------------------------------------------------
echo "[2] OpenAPI Check"
curl -s "$BASE/openapi.json" > /dev/null && echo "OpenAPI OK"
echo

# ---------------------------------------------------------
# 3. Heartbeat (unauthenticated)
# ---------------------------------------------------------
echo "[3] Heartbeat (unauthenticated)"
curl -s -o /dev/null -w "%{http_code}\n" "$BASE/api/auth/heartbeat"
echo

# ---------------------------------------------------------
# 4. Login Attempt
# ---------------------------------------------------------
echo "[4] Login Attempt"
curl -s -c "$COOKIE_JAR" -X POST "$BASE/api/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"admin"}'
echo -e "\n"

# ---------------------------------------------------------
# 5. Heartbeat (authenticated)
# ---------------------------------------------------------
echo "[5] Heartbeat (authenticated)"
curl -s -b "$COOKIE_JAR" "$BASE/api/auth/heartbeat"
echo -e "\n"

# ---------------------------------------------------------
# 6. Session Restore
# ---------------------------------------------------------
echo "[6] Session Restore"
curl -s -b "$COOKIE_JAR" "$BASE/api/auth/session/restore"
echo -e "\n"

# ---------------------------------------------------------
# 7. Session Status
# ---------------------------------------------------------
echo "[7] Session Status"
curl -s -b "$COOKIE_JAR" "$BASE/api/auth/session"
echo -e "\n"

# ---------------------------------------------------------
# 8. Logout
# ---------------------------------------------------------
echo "[8] Logout"
curl -s -b "$COOKIE_JAR" -X POST "$BASE/api/auth/logout"
echo -e "\n"

# ---------------------------------------------------------
# 9. Heartbeat After Logout
# ---------------------------------------------------------
echo "[9] Heartbeat After Logout"
curl -s -o /dev/null -w "%{http_code}\n" "$BASE/api/auth/heartbeat"
echo

echo "=== Regression Test Suite Complete ==="
