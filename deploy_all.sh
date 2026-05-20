#!/bin/bash
set -e

echo "=== Sentinel Ops Full Deployment ==="

BASE="/home/ubuntu/sentinel-ops-suite"

echo "[1/2] Deploying backend..."
"$BASE/deploy_backend.sh"

echo "[2/2] Deploying frontend..."
"$BASE/deploy_frontend.sh"

echo "=== Full deployment complete ==="
