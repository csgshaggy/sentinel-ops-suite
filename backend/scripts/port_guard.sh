#!/usr/bin/env bash
#
# SentinelOps Port Guard
# Forensic-grade port conflict detector and cleaner
# Ensures port 8000 is free for manual uvicorn development
#

PORT=8000
SERVICE_NAME="sentinel-backend.service"

echo "------------------------------------------------------------"
echo "🔍 SentinelOps Port Guard — Port $PORT Diagnostic"
echo "------------------------------------------------------------"

echo ""
echo "📌 Step 1 — Checking for systemd backend service..."
SERVICE_STATUS=$(systemctl is-active $SERVICE_NAME 2>/dev/null)

if [[ "$SERVICE_STATUS" == "active" ]]; then
    echo "⚠️  Systemd service '$SERVICE_NAME' is RUNNING — stopping it..."
    sudo systemctl stop $SERVICE_NAME
    sleep 1
else
    echo "✅ Systemd service '$SERVICE_NAME' is not running."
fi

echo ""
echo "📌 Step 2 — Checking if service is enabled..."
SERVICE_ENABLED=$(systemctl is-enabled $SERVICE_NAME 2>/dev/null)

if [[ "$SERVICE_ENABLED" == "enabled" ]]; then
    echo "⚠️  Service is ENABLED — disabling to prevent auto-respawn..."
    sudo systemctl disable $SERVICE_NAME
else
    echo "✅ Service is disabled."
fi

echo ""
echo "📌 Step 3 — Checking for uvicorn processes..."
UVICORN_PIDS=$(pgrep -f uvicorn)

if [[ -n "$UVICORN_PIDS" ]]; then
    echo "⚠️  Found uvicorn processes:"
    echo "$UVICORN_PIDS"
    echo "🔪 Killing uvicorn processes..."
    sudo pkill -f uvicorn
    sleep 1
else
    echo "✅ No uvicorn processes running."
fi

echo ""
echo "📌 Step 4 — Checking for python processes holding port $PORT..."
PORT_PIDS=$(sudo lsof -t -i :$PORT)

if [[ -n "$PORT_PIDS" ]]; then
    echo "⚠️  Port $PORT is still in use by:"
    sudo lsof -i :$PORT
    echo "🔪 Killing processes holding port $PORT..."
    sudo kill -9 $PORT_PIDS
    sleep 1
else
    echo "✅ No python processes holding port $PORT."
fi

echo ""
echo "📌 Step 5 — Final verification..."
FINAL_CHECK=$(sudo lsof -i :$PORT)

if [[ -z "$FINAL_CHECK" ]]; then
    echo "🎉 SUCCESS — Port $PORT is now FREE."
else
    echo "❌ ERROR — Port $PORT is STILL in use."
    echo "Here are the remaining processes:"
    sudo lsof -i :$PORT
    echo "You may need to manually inspect these."
fi

echo ""
echo "------------------------------------------------------------"
echo "🟢 Port Guard complete."
echo "You can now safely run: uvicorn app.main:app --reload"
echo "------------------------------------------------------------"
