#!/usr/bin/env bash
set -euo pipefail

SITE_CONF="/etc/nginx/sites-enabled/sentinel"
DASHBOARD_ASSETS="/home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/dist/assets"

echo "[NGINX] Syntax check..."
sudo nginx -t

echo "[NGINX] Checking sentinel is enabled..."
if [ ! -L "$SITE_CONF" ] && [ ! -f "$SITE_CONF" ]; then
  echo "[ERROR] Sentinel config not enabled: $SITE_CONF"
  exit 1
fi

echo "[NGINX] Checking dashboard assets directory..."
if [ ! -d "$DASHBOARD_ASSETS" ]; then
  echo "[ERROR] Dashboard assets directory missing: $DASHBOARD_ASSETS"
  exit 1
fi

echo "[NGINX] Checking /admin/assets/ block exists..."
if ! sudo nginx -T | grep -q "location /admin/assets/"; then
  echo "[ERROR] /admin/assets/ block missing in active config."
  exit 1
fi

echo "[NGINX] Checking ordering of /admin/assets/ before /admin/..."
ORDER=$(sudo nginx -T | awk '
  /location \/admin\/assets\// {assets=NR}
  /location \/admin\// && !/assets/ {admin=NR}
  END {
    if (assets && admin && assets < admin) print "OK";
    else print "BAD";
  }')

if [ "$ORDER" != "OK" ]; then
  echo "[ERROR] /admin/assets/ does NOT appear before /admin/ in active config."
  exit 1
fi

echo "[NGINX] Validator passed."
