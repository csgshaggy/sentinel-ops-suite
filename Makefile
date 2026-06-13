# ============================================
# Sentinel Ops Suite - Operator Grade Makefile
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
# Paths
# ----------------------------
BASE=/home/ubuntu/sentinel-ops-suite
LOGIN=$(BASE)/frontend/login-app
DASH=$(BASE)/frontend/dashboard-app
BACKEND=$(BASE)/backend
UNIFIED=$(BASE)/frontend/unified-frontend

DEPLOY_SCRIPT=$(BASE)/scripts/deploy/deploy.sh
CI_PIPELINE=$(BASE)/scripts/ci/ci_pipeline.sh
GUARDRAIL_SCRIPT=$(BASE)/scripts/guardrails/guard_manifest.sh
VALIDATOR_SCRIPT=$(BASE)/scripts/validators/validate_build.sh

# ----------------------------
# Default Target
# ----------------------------
help:
	@echo "$(GREEN)Sentinel Ops Suite Makefile$(RESET)"
	@echo ""
	@echo "$(BLUE)Available targets:$(RESET)"
	@echo "  make help              - Show this help menu"
	@echo "  make logs              - Stream backend logs"
	@echo "  make doctor            - Run system health checks"
	@echo "  make version           - Generate build stamp"
	@echo "  make validate          - Preflight validation + build checks"
	@echo "  make guardrail         - Run manifest guardrail"
	@echo "  make venv              - Activate backend Python virtual environment"
	@echo "  make lint-makefile     - Lint Makefile for tabs and ASCII"
	@echo "  make fix-tabs          - Auto-convert spaces to TABs"
	@echo "  make ascii-clean       - Strip non-ASCII characters"
	@echo "  make doctor-makefile   - Full Makefile health suite"
	@echo "  make login-build       - Build login frontend app"
	@echo "  make dashboard-build   - Build dashboard frontend app"
	@echo "  make frontend-build    - Build both frontend apps"
	@echo "  make backend-restart   - Restart backend service"
	@echo "  make nginx-reload      - Reload NGINX"
	@echo "  make deploy            - Deploy full stack via deploy.sh"
	@echo "  make ci                - Run unified CI pipeline"
	@echo "  make test              - Run Vitest"
	@echo "  make test-watch        - Run Vitest in watch mode"
	@echo "  make test-ui           - Launch Vitest UI"
	@echo "  make test-coverage     - Run Vitest with coverage"
	@echo "  make heal              - Auto-fix, validate, commit, and sync"
	@echo "  make heal-hard         - Full rebuild + redeploy"
	@echo "  make clean-all         - Purge caches, dist, node_modules, pycache"
	@echo "  make bootstrap         - Fresh environment setup"
	@echo "  make nuke              - Wipe everything except .git"
	@echo "  make rebuild-backend   - Rebuild backend environment"
	@echo "  make rebuild-frontend  - Rebuild both frontend apps"
	@echo "  make sync-hard         - Force rebase + force push"
	@echo ""

# ============================================
# Backend Logs
# ============================================
logs:
	@echo "$(BLUE)[LOGS]$(RESET) Streaming backend logs..."
	@sudo journalctl -u sentinel-backend.service -f -n 50

# ============================================
# Version Stamp
# ============================================
version:
	@echo "$(BLUE)[VERSION]$(RESET) Generating build stamp..."
	@date +"%Y-%m-%d_%H-%M-%S" > VERSION
	@echo "$(GREEN)[DONE]$(RESET) VERSION file updated."

# ============================================
# Makefile Linting
# ============================================
lint-makefile:
	@echo "$(BLUE)[LINT]$(RESET) Checking for spaces instead of tabs..."
	@grep -n "^[ ]\\+@" Makefile && echo "$(RED)Found invalid indentations.$(RESET)" || echo "$(GREEN)No invalid indentations.$(RESET)"

ascii-clean:
	@echo "$(BLUE)[ASCII]$(RESET) Removing non-ASCII characters..."
	@LC_ALL=C tr -cd '\11\12\15\40-\176' < Makefile > Makefile.clean
	@mv Makefile.clean Makefile
	@echo "$(GREEN)[DONE]$(RESET) ASCII cleanup complete."

fix-tabs:
	@echo "$(BLUE)[FIX]$(RESET) Converting leading spaces to tabs..."
	@sed -i 's/^[ ]\{4\}/\t/' Makefile
	@echo "$(GREEN)[DONE]$(RESET) Tabs fixed."

doctor-makefile: lint-makefile ascii-clean fix-tabs
	@echo "$(GREEN)[DONE]$(RESET) Makefile doctor complete."

# ============================================
# Validation
# ============================================
validate:
	@echo "$(BLUE)[VALIDATE]$(RESET) Running preflight checks..."
	@test -d frontend/dashboard-app || (echo "Missing frontend/dashboard-app directory" && exit 1)
	@test -d frontend/login-app || (echo "Missing frontend/login-app directory" && exit 1)
	@test -d backend || (echo "Missing backend directory" && exit 1)
	@echo "$(BLUE)[VALIDATE]$(RESET) Running build validator..."
	@bash $(VALIDATOR_SCRIPT)
	@echo "$(GREEN)[OK]$(RESET) Validation passed."

# ============================================
# Environment (Python Virtual Env)
# ============================================
venv:
	@echo "$(BLUE)[VENV]$(RESET) Activating backend virtual environment..."
	@bash -c "source $(BACKEND)/.venv/bin/activate && exec bash"

# ============================================
# CI GUARDRAIL (Manifest Guardrail)
# ============================================
guardrail:
	@echo "$(BLUE)[GUARDRAIL]$(RESET) Running Sentinel manifest guardrail..."
	@bash $(GUARDRAIL_SCRIPT)
	@echo "$(GREEN)[DONE]$(RESET) Guardrail passed."

prebuild:
	@./scripts/prebuild_chain.sh

# ============================================
# Frontend Builds
# ============================================
login-build:
	@echo "$(BLUE)[BUILD]$(RESET) Building login app..."
	@cd $(LOGIN) && rm -rf dist && npm install --silent && npm run build
	@echo "$(GREEN)[DONE]$(RESET) Login app build complete."

dashboard-build:
	@echo "$(BLUE)[BUILD]$(RESET) Building dashboard app..."
	@cd $(DASH) && rm -rf dist && npm install --silent && npm run build
	@echo "$(GREEN)[DONE]$(RESET) Dashboard app build complete."

frontend-build: login-build dashboard-build
	@echo "$(GREEN)[DONE]$(RESET) All frontend apps built."

# ============================================
# Backend + NGINX
# ============================================
backend-restart:
	@echo "$(BLUE)[BACKEND]$(RESET) Restarting backend service..."
	@sudo systemctl restart sentinel-backend.service
	@echo "$(GREEN)[DONE]$(RESET) Backend restarted."

nginx-reload:
	@echo "$(BLUE)[NGINX]$(RESET) Testing and reloading NGINX..."
	@sudo nginx -t && sudo systemctl reload nginx
	@echo "$(GREEN)[DONE]$(RESET) NGINX reloaded."

# ============================================
# Deployment (via deploy.sh)
# ============================================
deploy:
	@echo "$(BLUE)[DEPLOY]$(RESET) Running deploy script..."
	@bash $(DEPLOY_SCRIPT)
	@echo "$(GREEN)[DONE]$(RESET) Full stack deployed via deploy.sh."

# ============================================
# CI Pipeline
# ============================================
ci:
	@echo "$(BLUE)[CI]$(RESET) Running unified CI pipeline..."
	@bash $(CI_PIPELINE)
	@echo "$(GREEN)[DONE]$(RESET) CI pipeline complete."

# ============================================
# Vitest Test Runner
# ============================================
test:
	@echo "$(BLUE)[TEST]$(RESET) Running Vitest..."
	@cd $(UNIFIED) && npm run test

test-watch:
	@echo "$(BLUE)[TEST]$(RESET) Running Vitest in watch mode..."
	@cd $(UNIFIED) && npm run test:watch

test-ui:
	@echo "$(BLUE)[TEST]$(RESET) Launching Vitest UI..."
	@cd $(UNIFIED) && npm run test:ui

test-coverage:
	@echo "$(BLUE)[TEST]$(RESET) Running Vitest with coverage..."
	@cd $(UNIFIED) && npm run test:coverage

# ============================================
# HEAL (Auto-fix  Validate  Commit  Sync)
# ============================================
heal:
	@echo "$(BLUE)[HEAL]$(RESET) Running unified import fixer..."
	@./scripts/fix_imports_unified.sh || true

	@echo "$(BLUE)[HEAL]$(RESET) Running formatters..."
	@if command -v ruff >/dev/null 2>&1; then ruff check --fix . || true; fi
	@if command -v black >/dev/null 2>&1; then black . || true; fi
	@if command -v prettier >/dev/null 2>&1; then prettier --write . || true; fi

	@echo "$(BLUE)[HEAL]$(RESET) Running validators..."
	@if [ -x frontend/unified-frontend/scripts/ci_validate_imports.sh ]; then ./frontend/unified-frontend/scripts/ci_validate_imports.sh || true; fi

	@echo "$(BLUE)[HEAL]$(RESET) Staging all changes..."
	@git add -A

	@echo "$(BLUE)[HEAL]$(RESET) Committing..."
	@git commit -m "heal: $$(date -u +"%Y-%m-%dT%H:%M:%SZ")" || true

	@echo "$(BLUE)[HEAL]$(RESET) Running sync engine..."
	@./sync.sh

	@echo "$(GREEN)[DONE]$(RESET) Heal complete."

# ============================================
# HEAL-HARD (Full rebuild + redeploy)
# ============================================
heal-hard: clean-all frontend-build backend-restart nginx-reload deploy
	@echo "$(BLUE)[HEAL-HARD]$(RESET) Running full rebuild + redeploy..."
	@./scripts/fix_imports_unified.sh || true
	@git add -A
	@git commit -m "heal-hard: $$(date -u +"%Y-%m-%dT%H:%M:%SZ")" || true
	@./sync.sh
	@echo "$(GREEN)[DONE]$(RESET) heal-hard complete."

# ============================================
# CLEAN-ALL (Purge caches, node_modules, dist, pycache)
# ============================================
clean-all:
	@echo "$(BLUE)[CLEAN]$(RESET) Purging frontend build artifacts..."
	@find frontend -type d -name "dist" -exec rm -rf {} +
	@find frontend -type d -name "node_modules" -exec rm -rf {} +
	@echo "$(BLUE)[CLEAN]$(RESET) Purging backend caches..."
	@find backend -type d -name "__pycache__" -exec rm -rf {} +
	@find backend -type d -name ".pytest_cache" -exec rm -rf {} +
	@find backend -type d -name ".ruff_cache" -exec rm -rf {} +
	@echo "$(GREEN)[DONE]$(RESET) clean-all complete."

# ============================================
# BOOTSTRAP (Fresh environment setup)
# ============================================
bootstrap:
	@echo "$(BLUE)[BOOTSTRAP]$(RESET) Creating Python venv..."
	@python3 -m venv $(BACKEND)/.venv || true
	@echo "$(BLUE)[BOOTSTRAP]$(RESET) Installing backend dependencies..."
	@bash -c "source $(BACKEND)/.venv/bin/activate && pip install -U pip && pip install -r $(BACKEND)/requirements.txt || true"

	@echo "$(BLUE)[BOOTSTRAP]$(RESET) Installing frontend dependencies..."
	@cd $(LOGIN) && npm install --silent || true
	@cd $(DASH) && npm install --silent || true
	@cd $(UNIFIED) && npm install --silent || true

	@echo "$(BLUE)[BOOTSTRAP]$(RESET) Running unified import fixer..."
	@./scripts/fix_imports_unified.sh || true

	@echo "$(BLUE)[BOOTSTRAP]$(RESET) Running validators..."
	@if [ -x frontend/unified-frontend/scripts/ci_validate_imports.sh ]; then ./frontend/unified-frontend/scripts/ci_validate_imports.sh || true; fi

	@echo "$(GREEN)[DONE]$(RESET) bootstrap complete."

# ============================================
# NUKE (Wipe everything except .git)
# ============================================
nuke:
	@echo "$(RED)[NUKE] WARNING: This will delete EVERYTHING except .git$(RESET)"
	@sleep 2
	@find . -mindepth 1 -maxdepth 1 ! -name ".git" ! -name ".gitignore" -exec rm -rf {} +
	@echo "$(GREEN)[DONE]$(RESET) Repo nuked. Only .git remains."

# ============================================
# REBUILD-BACKEND (Fresh backend environment)
# ============================================
rebuild-backend: clean-all
	@echo "$(BLUE)[BACKEND]$(RESET) Rebuilding backend environment..."
	@rm -rf $(BACKEND)/.venv
	@python3 -m venv $(BACKEND)/.venv
	@bash -c "source $(BACKEND)/.venv/bin/activate && pip install -U pip && pip install -r $(BACKEND)/requirements.txt"
	@echo "$(GREEN)[DONE]$(RESET) Backend rebuild complete."

# ============================================
# REBUILD-FRONTEND (Fresh frontend builds)
# ============================================
rebuild-frontend: clean-all
	@echo "$(BLUE)[FRONTEND]$(RESET) Reinstalling frontend dependencies..."
	@cd $(LOGIN) && npm install --silent
	@cd $(DASH) && npm install --silent
	@cd $(UNIFIED) && npm install --silent
	@echo "$(BLUE)[FRONTEND]$(RESET) Rebuilding apps..."
	@cd $(LOGIN) && npm run build
	@cd $(DASH) && npm run build
	@cd $(UNIFIED) && npm run build
	@echo "$(GREEN)[DONE]$(RESET) Frontend rebuild complete."

# ============================================
# SYNC-HARD (Force rebase + force push)
# ============================================
sync-hard:
	@echo "$(RED)[SYNC-HARD] WARNING: This will force push to origin/main$(RESET)"
	@sleep 2
	@git fetch origin
	@git rebase origin/main || true
	@git add -A
	@git commit -m "sync-hard: $$(date -u +"%Y-%m-%dT%H:%M:%SZ")" || true
	@git push origin HEAD:main --force
	@echo "$(GREEN)[DONE]$(RESET) sync-hard complete."
