# ---------------------------------------------------------
# Sentinel Ops Suite — Root Makefile
# ---------------------------------------------------------

# Default target
.DEFAULT_GOAL := help

# ---------------------------------------------------------
# Python Backend
# ---------------------------------------------------------

backend-run:
	@echo "🚀 Starting FastAPI backend..."
	uvicorn app.main:app --reload

backend-install:
	@echo "📦 Installing backend dependencies..."
	pip install -r app/requirements.txt

# ---------------------------------------------------------
# Frontend
# ---------------------------------------------------------

frontend-run:
	@echo "🚀 Starting Vite frontend..."
	cd frontend && npm run dev

frontend-install:
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install

# ---------------------------------------------------------
# MFA Structure Validation
# ---------------------------------------------------------

validate-mfa:
	@echo "🔍 Validating MFA module structure..."
	node frontend/scripts/validate-mfa-structure.js

# ---------------------------------------------------------
# Repo Hygiene
# ---------------------------------------------------------

format:
	@echo "🧹 Formatting code..."
	black app
	prettier --write frontend/src

lint:
	@echo "🔎 Linting..."
	flake8 app
	cd frontend && npm run lint

# ---------------------------------------------------------
# Help
# ---------------------------------------------------------

help:
	@echo ""
	@echo "Sentinel Ops Suite — Available Commands"
	@echo ""
	@echo "  backend-run           Start FastAPI backend"
	@echo "  backend-install       Install backend dependencies"
	@echo ""
	@echo "  frontend-run          Start Vite frontend"
	@echo "  frontend-install      Install frontend dependencies"
	@echo ""
	@echo "  validate-mfa          Validate MFA module structure"
	@echo ""
	@echo "  format                Format backend + frontend"
	@echo "  lint                  Lint backend + frontend"
	@echo ""
