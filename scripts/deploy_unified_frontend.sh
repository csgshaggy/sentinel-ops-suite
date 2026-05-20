#!/usr/bin/env bash
set -euo pipefail

########################################
# Paths
########################################

PROJECT_ROOT="/home/ubuntu/sentinel-ops-suite/frontend/unified-frontend"
DEPLOY_ROOT="/var/www/sentinel-ops-frontend"
LOG_FILE="$PROJECT_ROOT/deploy.log"

########################################
# Logging helpers
########################################

log() {
  local level="$1"; shift
  local msg="$*"
  local ts
  ts="$(date '+%Y-%m-%d %H:%M:%S')"
  echo "[$ts] [$level] $msg"
  echo "[$ts] [$level] $msg" >> "$LOG_FILE"
}

fail() {
  log "ERROR" "$*"
  exit 1
}

########################################
# Pre-flight checks
########################################

log "INFO" "Starting unified-frontend deployment..."

if [[ ! -d "$PROJECT_ROOT" ]]; then
  fail "PROJECT_ROOT does not exist: $PROJECT_ROOT"
fi

command -v npm >/dev/null 2>&1 || fail "npm not installed"
command -v rsync >/dev/null 2>&1 || fail "rsync not installed"

########################################
# Build frontend
########################################

log "INFO" "Changing to project directory: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

log "INFO" "Running npm install (if needed)..."
npm install --silent

log "INFO" "Running npm run build..."
npm run build

########################################
# Clean deploy root (CRITICAL FIX)
########################################

log "INFO" "Cleaning deploy root: $DEPLOY_ROOT"
sudo rm -rf "$DEPLOY_ROOT"/*
sudo mkdir -p "$DEPLOY_ROOT"
sudo chown -R ubuntu:ubuntu "$DEPLOY_ROOT"

########################################
# Sync public/ and dist/ to deploy root
########################################

if [[ -d "$PROJECT_ROOT/public" ]]; then
  log "INFO" "Copying public/ to $DEPLOY_ROOT..."
  rsync -av "$PROJECT_ROOT/public/" "$DEPLOY_ROOT/"
else
  log "WARNING" "public/ directory not found"
fi

if [[ -d "$PROJECT_ROOT/dist" ]]; then
  log "INFO" "Copying dist/ to $DEPLOY_ROOT..."
  rsync -av "$PROJECT_ROOT/dist/" "$DEPLOY_ROOT/"
else
  fail "dist/ directory not found. Build may have failed."
fi

########################################
# Sanity checks for favicon assets
########################################

check_file() {
  local path="$1"
  if [[ -f "$path" ]]; then
    log "INFO" "Found: $path"
  else
    log "WARNING" "Missing expected file: $path"
  fi
}

log "INFO" "Checking favicon and manifest files..."

check_file "$DEPLOY_ROOT/favicon.ico"
check_file "$DEPLOY_ROOT/favicon.svg"
check_file "$DEPLOY_ROOT/site.webmanifest"

########################################
# Reload NGINX
########################################

log "INFO" "Reloading NGINX..."
sudo systemctl reload nginx

########################################
# Print deployed bundle names
########################################

log "INFO" "Deployed bundle files:"
ls -1 "$DEPLOY_ROOT" | grep -E "index-|assets" | tee -a "$LOG_FILE"

log "INFO" "Deployment completed successfully."
