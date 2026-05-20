# ============================================
# Sentinel Ops Suite - Operator Grade Makefile
# Absolute Path: /home/ubuntu/sentinel-ops-suite/Makefile
# ============================================

# ----------------------------
# Color Variables (Item 1)
# ----------------------------
BLUE=\033[1;34m
GREEN=\033[1;32m
YELLOW=\033[1;33m
RED=\033[1;31m
RESET=\033[0m

# ----------------------------
# Default Target
# ----------------------------
help:
    @echo "$(GREEN)Sentinel Ops Suite Makefile$(RESET)"
    @echo ""
    @echo "$(BLUE)Available targets:$(RESET)"
    @echo "  make help            - Show this help menu"
    @echo "  make logs            - Stream backend logs (Item 2)"
    @echo "  make doctor          - Run system health checks (Item 3)"
    @echo "  make version         - Generate build stamp (Item 4)"
    @echo "  make validate        - Preflight validation (Item 5)"
    @echo "  make lint-makefile   - Lint Makefile for tabs and ASCII"
    @echo "  make fix-tabs        - Auto-convert spaces to TABs"
    @echo "  make deploy          - Deploy full stack (existing)"
    @echo ""

# ============================================
# ITEM 2 - Backend Logs Target
# ============================================
logs:
    @echo "$(BLUE)[LOGS]$(RESET) Streaming backend logs..."
    @sudo journalctl -u sentinel-backend.service -f -n 50

# ============================================
# ITEM 3 - Forensic Health Check
# ============================================
doctor:
    @echo "$(BLUE)[DOCTOR]$(RESET) Running Sentinel Ops health checks..."
    @echo ""
    @echo "$(YELLOW)[CHECK]$(RESET) Backend service status:"
    @systemctl is-active --quiet sentinel-backend.service && \
        echo "$(GREEN)OK$(RESET) Backend service is active." || \
        echo "$(RED)FAIL$(RESET) Backend service is NOT active."

    @echo ""
    @echo "$(YELLOW)[CHECK]$(RESET) NGINX status:"
    @systemctl is-active --quiet nginx && \
        echo "$(GREEN)OK$(RESET) NGINX is active." || \
        echo "$(RED)FAIL$(RESET) NGINX is NOT active."

    @echo ""
    @echo "$(YELLOW)[CHECK]$(RESET) Python virtual environment:"
    @[ -d "backend/venv" ] && \
        echo "$(GREEN)OK$(RESET) venv exists." || \
        echo "$(RED)FAIL$(RESET) venv missing."

    @echo ""
    @echo "$(YELLOW)[CHECK]$(RESET) Frontend build directory:"
    @[ -d "frontend/dashboard-app/dist" ] && \
        echo "$(GREEN)OK$(RESET) Frontend build exists." || \
        echo "$(RED)FAIL$(RESET) No frontend build found."

    @echo ""
    @echo "$(GREEN)[DONE]$(RESET) Health check complete."

# ============================================
# ITEM 4 - Build Version Stamp
# ============================================
version:
    @echo "$(BLUE)[VERSION]$(RESET) Generating build stamp..."
    @mkdir -p backend/app
    @echo "timestamp=$$(date -u +\"%Y-%m-%dT%H:%M:%SZ\")" > backend/app/version.txt
    @echo "commit=$$(git rev-parse --short HEAD 2>/dev/null || echo 'no-git')" >> backend/app/version.txt
    @echo "host=$$(hostname)" >> backend/app/version.txt
    @echo "user=$$(whoami)" >> backend/app/version.txt
    @echo "build_id=$$(uuidgen 2>/dev/null || echo 'no-uuid')" >> backend/app/version.txt
    @echo "$(GREEN)[DONE]$(RESET) Version file written to backend/app/version.txt"

# ============================================
# ITEM 5 - Preflight Validation
# ============================================
validate:
    @echo "$(BLUE)[VALIDATE]$(RESET) Running preflight checks..."
    @echo ""

    @echo "$(YELLOW)[CHECK]$(RESET) Required directories:"
    @[ -d "backend" ] && echo "$(GREEN)OK$(RESET) backend/" || echo "$(RED)FAIL$(RESET) backend/ missing"
    @[ -d "frontend/dashboard-app" ] && echo "$(GREEN)OK$(RESET) dashboard-app/" || echo "$(RED)FAIL$(RESET) dashboard-app/ missing"

    @echo ""
    @echo "$(YELLOW)[CHECK]$(RESET) Required commands:"
    @command -v npm >/dev/null 2>&1 && echo "$(GREEN)OK$(RESET) npm found" || echo "$(RED)FAIL$(RESET) npm missing"
    @command -v python3 >/dev/null 2>&1 && echo "$(GREEN)OK$(RESET) python3 found" || echo "$(RED)FAIL$(RESET) python3 missing"
    @command -v git >/dev/null 2>&1 && echo "$(GREEN)OK$(RESET) git found" || echo "$(RED)FAIL$(RESET) git missing"

    @echo ""
    @echo "$(YELLOW)[CHECK]$(RESET) Backend service file:"
    @[ -f "/etc/systemd/system/sentinel-backend.service" ] && \
        echo "$(GREEN)OK$(RESET) service file exists" || \
        echo "$(RED)FAIL$(RESET) service file missing"

    @echo ""
    @echo "$(YELLOW)[CHECK]$(RESET) NGINX config:"
    @[ -f "/etc/nginx/sites-enabled/sentinel-ops.conf" ] && \
        echo "$(GREEN)OK$(RESET) nginx config exists" || \
        echo "$(RED)FAIL$(RESET) nginx config missing"

    @echo ""
    @echo "$(GREEN)[DONE]$(RESET) Preflight validation complete."

# ============================================
# Makefile Lint - Enforce Tabs and ASCII Only
# ============================================
lint-makefile:
    @echo "$(BLUE)[LINT]$(RESET) Checking Makefile formatting..."
    @echo ""

    @echo "$(YELLOW)[CHECK]$(RESET) Tabs vs spaces:"
    @if grep -n "^[ ]\+" Makefile >/dev/null; then \
        echo "$(RED)FAIL$(RESET) Found lines starting with spaces instead of TABs."; \
        grep -n "^[ ]\+" Makefile; \
        exit 1; \
    else \
        echo "$(GREEN)OK$(RESET) No space-indented command lines found."; \
    fi

    @echo ""
    @echo "$(YELLOW)[CHECK]$(RESET) Non-ASCII characters:"
    @if LC_ALL=C grep -n "[^ -~]" Makefile >/dev/null; then \
        echo "$(RED)FAIL$(RESET) Found non-ASCII characters."; \
        LC_ALL=C grep -n "[^ -~]" Makefile; \
        exit 1; \
    else \
        echo "$(GREEN)OK$(RESET) ASCII-only confirmed."; \
    fi

    @echo ""
    @echo "$(GREEN)[DONE]$(RESET) Makefile linting complete."

# ============================================
# Auto-Fix - Convert Spaces to Tabs
# ============================================
fix-tabs:
    @echo "$(BLUE)[FIX]$(RESET) Converting leading spaces to TABs..."
    @echo ""
    @if grep -n "^[ ]\+" Makefile >/dev/null; then \
        echo "$(YELLOW)[ACTION]$(RESET) Fixing lines with space indentation..."; \
        sed -i 's/^[ ]\+/\t/' Makefile; \
        echo "$(GREEN)[DONE]$(RESET) All leading spaces converted to TABs."; \
    else \
        echo "$(GREEN)[OK]$(RESET) No space-indented lines found."; \
    fi

# ============================================
# Deployment (Existing Target)
# ============================================
deploy:
    @echo "$(YELLOW)[DEPLOY]$(RESET) Building frontend..."
    @cd frontend/dashboard-app && npm install && npm run build

    @echo "$(YELLOW)[DEPLOY]$(RESET) Clearing old frontend files..."
    @sudo rm -rf /var/www/sentinel-ops-frontend/*

    @echo "$(YELLOW)[DEPLOY]$(RESET) Deploying new frontend build..."
    @sudo cp -r frontend/dashboard-app/dist/* /var/www/sentinel-ops-frontend/

    @echo "$(YELLOW)[DEPLOY]$(RESET) Restarting backend service..."
    @sudo systemctl restart sentinel-backend.service

    @echo "$(YELLOW)[DEPLOY]$(RESET) Reloading NGINX..."
    @sudo systemctl reload nginx

    @echo "$(GREEN)[DONE]$(RESET) Deployment complete."
