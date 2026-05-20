#!/bin/bash

set -e

FRONTEND_DIR="/home/ubuntu/sentinel-ops-suite/frontend/unified-frontend"
PROD_DIR="/var/www/sentinel-ops-frontend"

echo "Building unified-frontend..."
cd "$FRONTEND_DIR"
npm run build

echo "Clearing old production files..."
sudo rm -rf "$PROD_DIR"/*

echo "Deploying new build..."
sudo cp -r dist/* "$PROD_DIR"/

echo "Reloading nginx..."
sudo systemctl reload nginx

echo "Deployment complete."
