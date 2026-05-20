# ============================================
# Sentinel Ops Suite - Frontend Makefile
# Location: frontend/dashboard-app/Makefile
# ============================================

# ----------------------------
# Color Variables
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
    @echo "$(GREEN)Sentinel Ops Frontend Makefile$(RESET)"
    @echo ""
    @echo "$(BLUE)Available targets:$(RESET)"
    @echo "  make help          - Show this help menu"
    @echo "  make install       - Install npm dependencies"
    @echo "  make dev           - Start Vite dev server"
    @echo "  make build         - Build production bundle"
    @echo "  make preview       - Preview production build"
    @echo "  make lint          - Run ESLint"
    @echo "  make format        - Run Prettier formatting"
    @echo "  make audit         - Run npm security audit"
    @echo "  make clean         - Remove node_modules and dist"
    @echo "  make doctor-frontend - Full frontend health suite"
    @echo ""

# ============================================
# Install Dependencies
# ============================================
install:
    @echo "$(BLUE)[INSTALL]$(RESET) Installing npm dependencies..."
    @npm install

# ============================================
# Development Server
# ============================================
dev:
    @echo "$(BLUE)[DEV]$(RESET) Starting Vite development server..."
    @npm run dev

# ============================================
# Production Build
# ============================================
build:
    @echo "$(BLUE)[BUILD]$(RESET) Building production bundle..."
    @npm run build

# ============================================
# Preview Production Build
# ============================================
preview:
    @echo "$(BLUE)[PREVIEW]$(RESET) Previewing production build..."
    @npm run preview

# ============================================
# Linting (ESLint)
# ============================================
lint:
    @echo "$(BLUE)[LINT]$(RESET) Running ESLint..."
    @npm run lint || true

# ============================================
# Formatting (Prettier)
# ============================================
format:
    @echo "$(BLUE)[FORMAT]$(RESET) Running Prettier formatting..."
    @npm run format || true

# ============================================
# Security Audit
# ============================================
audit:
    @echo "$(BLUE)[AUDIT]$(RESET) Running npm security audit..."
    @npm audit || true

# ============================================
# Clean Workspace
# ============================================
clean:
    @echo "$(BLUE)[CLEAN]$(RESET) Removing node_modules and dist..."
    @rm -rf node_modules
    @rm -rf dist
    @echo "$(GREEN)[DONE]$(RESET) Clean complete."

# ============================================
# Frontend Doctor - Full Health Suite
# ============================================
doctor-frontend:
    @echo "$(BLUE)[FRONTEND-DOCTOR]$(RESET) Running frontend diagnostics..."
    @echo ""

    @echo "$(YELLOW)[CHECK]$(RESET) Checking for missing node_modules..."
    @if [ ! -d "node_modules" ]; then \
        echo "$(RED)ISSUE$(RESET) node_modules missing. Run: make install"; \
    else \
        echo "$(GREEN)OK$(RESET) node_modules present."; \
    fi
    @echo ""

    @echo "$(YELLOW)[CHECK]$(RESET) Checking for missing package.json..."
    @if [ ! -f "package.json" ]; then \
        echo "$(RED)ISSUE$(RESET) package.json missing."; \
    else \
        echo "$(GREEN)OK$(RESET) package.json found."; \
    fi
    @echo ""

    @echo "$(YELLOW)[CHECK]$(RESET) Running ESLint..."
    @npm run lint || echo "$(RED)ISSUE$(RESET) ESLint reported problems."
    @echo ""

    @echo "$(YELLOW)[CHECK]$(RESET) Running Prettier..."
    @npm run format || echo "$(RED)ISSUE$(RESET) Prettier formatting issues."
    @echo ""

    @echo "$(YELLOW)[CHECK]$(RESET) Checking Vite config..."
    @if [ ! -f "vite.config.js" ] && [ ! -f "vite.config.ts" ]; then \
        echo "$(RED)ISSUE$(RESET) No Vite config found."; \
    else \
        echo "$(GREEN)OK$(RESET) Vite config present."; \
    fi
    @echo ""

    @echo "$(GREEN)[DONE]$(RESET) Frontend diagnostics complete."
