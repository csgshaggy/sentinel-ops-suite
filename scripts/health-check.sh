#!/usr/bin/env bash
set -euo pipefail

# =========[ CONFIG ]=========
BACKEND_HEALTH_URL="http://localhost/api/health"
FRONTEND_HEALTH_URL="http://localhost/"
NGINX_STATUS_URL="http://localhost"
# ============================

# Colors
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
NC="\033[0m"

timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

log() {
  local level="$1"; shift
  local color="$1"; shift
  echo -e "[$(timestamp)] ${color}${level}${NC} $*"
}

info()  { log "INFO " "$BLUE"  "$*"; }
ok()    { log "OK   " "$GREEN" "$*"; }
warn()  { log "WARN " "$YELLOW" "$*"; }
error() { log "ERROR" "$RED"   "$*"; }

check_url() {
  local name="$1"
  local url="$2"

  info "Checking $name at $url"

  if curl -fsS "$url" >/dev/null; then
    ok "$name is healthy"
  else
    error "$name FAILED"
    return 1
  fi
}

info "=== Sentinel Ops — Health Check ==="

check_url "Backend" "$BACKEND_HEALTH_URL"
check_url "Frontend" "$FRONTEND_HEALTH_URL"
check_url "Nginx" "$NGINX_STATUS_URL"

ok "=== All Systems Healthy ==="
