# ---------------------------------------------------------
# Sentinel Ops Suite — Root Makefile
# Deterministic, operator‑grade repo workflows
# ---------------------------------------------------------

.DEFAULT_GOAL := help

# List of expected core targets (for self-check)
EXPECTED_TARGETS := \
	backend-run \
	backend-install \
	backend-format \
	backend-lint \
	frontend-run \
	frontend-install \
	frontend-format \
	frontend-lint \
	validate-mfa \
	format \
	lint \
	repo-health \
	validate-makefile \
	self-check

# ---------------------------------------------------------
# Backend (FastAPI)
# ---------------------------------------------------------

backend-run:
	@echo "🚀 Starting FastAPI backend..."
	uvicorn app.main:app --reload

backend-install:
	@echo "📦 Installing backend dependencies..."
	pip install -r app/requirements.txt

backend-format:
	@echo "🧹 Formatting backend..."
	black app

backend-lint:
	@echo "🔎 Linting backend..."
	flake8 app

# ---------------------------------------------------------
# Frontend (Vite + React)
# ---------------------------------------------------------

frontend-run:
	@echo "🚀 Starting Vite frontend..."
	cd frontend && npm run dev

frontend-install:
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install

frontend-format:
	@echo "🧹 Formatting frontend..."
	prettier --write frontend/src

frontend-lint:
	@echo "🔎 Linting frontend..."
	cd frontend && npm run lint

# ---------------------------------------------------------
# MFA Structure Validation
# ---------------------------------------------------------

validate-mfa:
	@echo "🔍 Validating MFA module structure..."
	node frontend/scripts/validate-mfa-structure.cjs

# ---------------------------------------------------------
# Repo Hygiene (Unified)
# ---------------------------------------------------------

format: backend-format frontend-format
	@echo "✨ Formatting complete."

lint: backend-lint frontend-lint
	@echo "✨ Linting complete."

# ---------------------------------------------------------
# Makefile Drift & Self-Validation
# ---------------------------------------------------------

# Drift-aware Makefile validator:
# - Ensures this Makefile is syntactically valid
# - Fails fast if parsing breaks (e.g., bad merge, manual edit)
validate-makefile:
	@echo "🔍 Validating Makefile syntax for drift..."
	@# Use 'make -n' on a no-op target to force parse
	@make -n help >/dev/null
	@echo "✅ Makefile syntax is valid."

# Makefile self-check:
# - Ensures all EXPECTED_TARGETS actually exist
self-check:
	@echo "🔍 Running Makefile self-check (expected targets)..."
	@missing=0; \
	for t in $(EXPECTED_TARGETS); do \
		if ! $(MAKE) -qp 2>/dev/null | awk -F':' '/^[a-zA-Z0-9][^$$#\/\t=]*:/ {print $$1}' | sort -u | grep -qx "$$t"; then \
			echo "❌ Missing expected target: $$t"; \
			missing=1; \
		fi; \
	done; \
	if [ $$missing -ne 0 ]; then \
		echo "❌ Makefile self-check failed: one or more expected targets are missing."; \
		exit 1; \
	fi; \
	echo "✅ Makefile self-check passed: all expected targets exist."

# Meta-target for full repo health:
# - Validates Makefile
# - Runs self-check
# - Runs lint + format
# - Runs MFA validator
repo-health: validate-makefile self-check lint format validate-mfa
	@echo "🩺 Full repo health check complete. All systems nominal."

# ---------------------------------------------------------
# Help Menu
# ---------------------------------------------------------

help:
	@echo ""
	@echo "Sentinel Ops Suite — Available Commands"
	@echo ""
	@echo " Backend:"
	@echo "   backend-run            Start FastAPI backend"
	@echo "   backend-install        Install backend dependencies"
	@echo "   backend-format         Format backend code"
	@echo "   backend-lint           Lint backend code"
	@echo ""
	@echo " Frontend:"
	@echo "   frontend-run           Start Vite frontend"
	@echo "   frontend-install       Install frontend dependencies"
	@echo "   frontend-format        Format frontend code"
	@echo "   frontend-lint          Lint frontend code"
	@echo ""
	@echo " MFA:"
	@echo "   validate-mfa           Validate MFA module structure"
	@echo ""
	@echo " Repo Hygiene:"
	@echo "   format                 Format backend + frontend"
	@echo "   lint                   Lint backend + frontend"
	@echo ""
	@echo " Makefile Integrity:"
	@echo "   validate-makefile      Validate Makefile syntax (drift-aware)"
	@echo "   self-check             Ensure all expected targets exist"
	@echo "   repo-health            Full repo health (lint, format, MFA, Makefile checks)"
	@echo ""
