#!/bin/bash
set -e

FRONTEND_ROOT="/var/www/sentinel-frontend"
REPO_ROOT="/home/ubuntu/sentinel-ops-suite/frontend"

echo "------------------------------------------------------------"
echo " 🔧 Building ALL Sentinel Frontend SPAs"
echo "------------------------------------------------------------"

# 1. LOGIN APP
echo "➡️  Building login-app..."
cd "$REPO_ROOT/login-app"
npm install --silent
npm run build

# 2. DASHBOARD APP (this IS your admin app)
echo "➡️  Building dashboard-app..."
cd "$REPO_ROOT/dashboard-app"
npm install --silent
npm run build

echo "------------------------------------------------------------"
echo " 🧹 Clearing deployed frontend directory"
echo "------------------------------------------------------------"

sudo rm -rf "$FRONTEND_ROOT"/*
sudo mkdir -p "$FRONTEND_ROOT"

echo "------------------------------------------------------------"
echo " 📦 Deploying dashboard-app (root)"
echo "------------------------------------------------------------"

sudo cp -r "$REPO_ROOT/dashboard-app/dist/"* "$FRONTEND_ROOT/"

echo "------------------------------------------------------------"
echo " 📦 Deploying login-app → /login"
echo "------------------------------------------------------------"

sudo mkdir -p "$FRONTEND_ROOT/login"
sudo cp -r "$REPO_ROOT/login-app/dist/"* "$FRONTEND_ROOT/login/"

echo "------------------------------------------------------------"
echo " 📦 Deploying dashboard-app → /admin"
echo "------------------------------------------------------------"

sudo mkdir -p "$FRONTEND_ROOT/admin"
sudo cp -r "$REPO_ROOT/dashboard-app/dist/"* "$FRONTEND_ROOT/admin/"

echo "------------------------------------------------------------"
echo " 🔄 Restarting NGINX"
echo "------------------------------------------------------------"

sudo systemctl restart nginx

echo "------------------------------------------------------------"
echo " ✅ Deployment Complete — All SPAs Built & Synced"
echo "------------------------------------------------------------"
