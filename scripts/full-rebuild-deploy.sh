#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# SentinelOps — Full Blue/Green Rebuild + Deploy
# ============================================================

FRONTEND_DIR="/home/ubuntu/sentinel-ops-suite/frontend/unified-frontend"
BACKEND_DIR="/home/ubuntu/sentinel-ops-suite/backend"
ACTIVE_LINK="/var/www/sentinel-ops"

BLUE="/var/www/sentinel-ops-blue"
GREEN="/var/www/sentinel-ops-green"

echo "============================================================"
echo "1. Determine Active Deployment"
echo "============================================================"

if [ -L "$ACTIVE_LINK" ]; then
    CURRENT_TARGET=$(readlink -f "$ACTIVE_LINK")
else
    echo "[ERROR] Active symlink missing. Creating default BLUE."
    sudo ln -sfn "$BLUE" "$ACTIVE_LINK"
    CURRENT_TARGET="$BLUE"
fi

echo "Active target: $CURRENT_TARGET"

if [[ "$CURRENT_TARGET" == "$BLUE" ]]; then
    TARGET="$GREEN"
    NEXT="GREEN"
else
    TARGET="$BLUE"
    NEXT="BLUE"
fi

echo "Deploying to: $TARGET"

# ============================================================
# 2. Build Frontend
# ============================================================
echo "============================================================"
echo "2. Building Frontend"
echo "============================================================"

cd "$FRONTEND_DIR"
npm install --silent
npm run build

echo "[OK] Frontend build complete."

# ============================================================
# 3. Deploy Frontend to Blue/Green Target
# ============================================================
echo "============================================================"
echo "3. Deploying Frontend to $TARGET"
echo "============================================================"

sudo rm -rf "$TARGET"/*
sudo mkdir -p "$TARGET"
sudo cp -r "$FRONTEND_DIR/dist/"* "$TARGET/"

echo "[OK] Frontend deployed to $TARGET"

# ============================================================
# 4. Backend Build + Restart
# ============================================================
echo "============================================================"
echo "4. Backend Build + Restart"
echo "============================================================"

cd "$BACKEND_DIR"
source .venv/bin/activate
pip install -r requirements.txt --quiet

sudo systemctl restart sentinel-backend.service
sleep 2

echo "[OK] Backend restarted."

# ============================================================
# 5. Switch Symlink
# ============================================================
echo "============================================================"
echo "5. Switching Active Deployment"
echo "============================================================"

sudo ln -sfn "$TARGET" "$ACTIVE_LINK"
echo "[OK] Active symlink now points to: $TARGET"

# ============================================================
# 6. Reload NGINX
# ============================================================
echo "============================================================"
echo "6. Reloading NGINX"
echo "============================================================"

sudo nginx -t
sudo systemctl reload nginx

echo "[OK] NGINX reloaded."

# ============================================================
# 7. Health Checks
# ============================================================
echo "============================================================"
echo "7. Running Health Checks"
echo "============================================================"

sleep 1

HTTP_CODE=$(curl -k -o /dev/null -s -w "%{http_code}" https://crcybercop.dpdns.org)
API_CODE=$(curl -k -o /dev/null -s -w "%{http_code}" https://crcybercop.dpdns.org/api/auth/me)

echo "Frontend HTTP: $HTTP_CODE"
echo "API /auth/me: $API_CODE"

if [[ "$HTTP_CODE" != "200" ]]; then
    echo "[ERROR] Frontend health check failed."
    exit 1
fi

echo "[OK] Deployment healthy."

# ============================================================
# 8. Rollback Support
# ============================================================
if [[ "${1:-}" == "rollback" ]]; then
    echo "============================================================"
    echo "ROLLBACK REQUESTED"
    echo "============================================================"

    if [[ "$NEXT" == "GREEN" ]]; then
        sudo ln -sfn "$BLUE" "$ACTIVE_LINK"
        echo "[OK] Rolled back to BLUE"
    else
        sudo ln -sfn "$GREEN" "$ACTIVE_LINK"
        echo "[OK] Rolled back to GREEN"
    fi

    sudo systemctl reload nginx
    exit 0
fi

echo "============================================================"
echo "🎉 Deployment Complete — Active: $NEXT"
echo "============================================================"
