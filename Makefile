# ============================================================
# SSRF Command Console — Operator‑Grade Makefile
# Monorepo: backend/ + frontend/
# ============================================================

SHELL := /bin/bash

# ------------------------------------------------------------
# Git Hooks
# ------------------------------------------------------------

HOOKS = pre-commit pre-push pre-rebase pre-commit-msg commit-msg post-merge

install-hooks:
	@echo "🔧 Installing Git hooks..."
	@for hook in $(HOOKS); do \
		if [ -f .git/hooks/$$hook ]; then rm -f .git/hooks/$$hook; fi; \
		cp .git/hooks/$$hook .git/hooks/$$hook; \
		chmod +x .git/hooks/$$hook; \
		echo "   ✔ Installed $$hook"; \
	done
	@echo "✔ All hooks installed."

verify-hooks:
	@echo "🔍 Verifying hook presence..."
	@for hook in $(HOOKS); do \
		if [ ! -f .git/hooks/$$hook ]; then \
			echo "❌ Missing hook: $$hook"; \
			exit 1; \
		fi; \
	done
	@echo "✔ All hooks present."

# ------------------------------------------------------------
# Repo Structure Validation
# ------------------------------------------------------------

validate-structure:
	@./scripts/validate_structure.sh

# ------------------------------------------------------------
# Backend Commands
# ------------------------------------------------------------

backend-run:
	@echo "🚀 Starting backend..."
	cd backend && uvicorn ssrf_command_console.main:app --reload

backend-format:
	@echo "🧹 Formatting backend (Black)..."
	cd backend && black src

backend-lint:
	@echo "🔎 Linting backend (Ruff)..."
	cd backend && ruff src

backend-test:
	@echo "🧪 Running backend tests..."
	cd backend && pytest

backend-all: backend-format backend-lint backend-test

# ------------------------------------------------------------
# Frontend Commands
# ------------------------------------------------------------

frontend-dev:
	@echo "🚀 Starting frontend dev server..."
	cd frontend && npm run dev

frontend-build:
	@echo "🏗️ Building frontend..."
	cd frontend && npm run build

frontend-format:
	@echo "🧹 Formatting frontend (Prettier)..."
	cd frontend && npx prettier --write src

frontend-typecheck:
	@echo "🔎 Type-checking frontend..."
	cd frontend && npx tsc --noEmit

frontend-all: frontend-format frontend-typecheck frontend-build

# ------------------------------------------------------------
# Drift Detection
# ------------------------------------------------------------

drift:
	@echo "🔍 Running drift detector..."

	# Structure drift
	@test -d backend/src/ssrf_command_console || (echo "❌ Drift: backend/src/ssrf_command_console missing" && exit 1)
	@test -d frontend/src || (echo "❌ Drift: frontend/src missing" && exit 1)

	# Python formatting drift
	if command -v black >/dev/null 2>&1; then \
		black --check backend/src || (echo "❌ Python formatting drift detected" && exit 1); \
	fi

	# JS/TS formatting drift
	if command -v npx >/dev/null 2>&1; then \
		npx prettier --check "frontend/src/**/*.{js,jsx,ts,tsx}" || (echo "❌ JS/TS formatting drift detected" && exit 1); \
	fi

	@echo "✔ No drift detected."

# ------------------------------------------------------------
# CI Pipeline
# ------------------------------------------------------------

ci-backend:
	@echo "🏁 CI: Backend pipeline..."
	make validate-structure
	make backend-all

ci-frontend:
	@echo "🏁 CI: Frontend pipeline..."
	make validate-structure
	make frontend-all

ci-full:
	@echo "🏁 CI: Full monorepo CI..."
	make validate-structure
	make backend-all
	make frontend-all
	make drift
	@echo "✅ CI: All checks passed."

# ------------------------------------------------------------
# Clean
# ------------------------------------------------------------

clean:
	@echo "🧽 Cleaning build artifacts..."
	rm -rf frontend/dist
	rm -rf backend/.pytest_cache
	rm -rf backend/__pycache__
	find backend -type d -name "__pycache__" -exec rm -rf {} +
	@echo "✔ Clean complete."

# ------------------------------------------------------------
# Default
# ------------------------------------------------------------

help:
	@echo ""
	@echo "SSRF Command Console — Makefile Commands"
	@echo "----------------------------------------"
	@echo "make install-hooks        Install Git hooks"
	@echo "make verify-hooks         Verify hooks exist"
	@echo "make validate-structure   Validate monorepo layout"
	@echo "make backend-run          Run backend server"
	@echo "make backend-all          Format + lint + test backend"
	@echo "make frontend-dev         Run frontend dev server"
	@echo "make frontend-all         Format + typecheck + build frontend"
	@echo "make drift                Run drift detector"
	@echo "make ci-full              Full CI pipeline"
	@echo "make clean                Clean build artifacts"
	@echo ""
