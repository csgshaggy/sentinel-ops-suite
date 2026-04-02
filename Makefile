# =====================================================================
# Sentinel Ops Suite — Operator-Grade Makefile
# Deterministic, Drift-Proof, CI-Enforced
# =====================================================================

SHELL := /bin/bash

# ---------------------------------------------------------------------
# Repo Health: Full System Validation
# ---------------------------------------------------------------------
repo-health: validate-makefile validate-mfa backend-lint frontend-lint
	@echo "✅ Repo health check complete."

# ---------------------------------------------------------------------
# Makefile Syntax + Structure Validation
# ---------------------------------------------------------------------
validate-makefile:
	@echo "🔍 Validating Makefile syntax for drift..."
	@make -n > /dev/null
	@echo "🔍 Running Makefile self-check (expected targets)..."
	@grep -q "repo-health" Makefile || (echo "❌ Missing repo-health target" && exit 1)
	@grep -q "backend-lint" Makefile || (echo "❌ Missing backend-lint target" && exit 1)
	@grep -q "frontend-lint" Makefile || (echo "❌ Missing frontend-lint target" && exit 1)
	@grep -q "validate-mfa" Makefile || (echo "❌ Missing validate-mfa target" && exit 1)
	@echo "✅ Makefile self-check passed: all expected targets exist."

# ---------------------------------------------------------------------
# MFA Structure Validator
# ---------------------------------------------------------------------
validate-mfa:
	@echo "🔍 Validating MFA module structure..."
	node frontend/scripts/validate-mfa-structure.cjs
	@echo "✅ MFA structure validated."

# ---------------------------------------------------------------------
# Backend Linting
# ---------------------------------------------------------------------
backend-lint:
	@echo "🔎 Linting backend..."
	flake8 app

# ---------------------------------------------------------------------
# Frontend Linting
# ---------------------------------------------------------------------
frontend-lint:
	@echo "🔎 Linting frontend..."
	cd frontend && npm run lint

# ---------------------------------------------------------------------
# Full Repository Sync (Operator-Grade)
# ---------------------------------------------------------------------
sync:
	@echo "🔄 Starting full repository sync..."
	@bash sync.sh
	@echo "✅ Sync complete."

# ---------------------------------------------------------------------
# Utility Targets
# ---------------------------------------------------------------------
clean:
	@echo "🧹 Cleaning Python caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "🧹 Cleaning Node modules caches..."
	rm -rf frontend/node_modules/.cache || true
	@echo "✅ Clean complete."

.PHONY: repo-health validate-makefile validate-mfa backend-lint frontend-lint sync clean
