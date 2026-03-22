# =========================================================
# SSRF Command Console — Operator‑Grade Makefile
# =========================================================

PYTHON := venv/bin/python
PIP := venv/bin/pip

# Colors
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[1;34m
NC := \033[0m

# ---------------------------------------------------------
# Help Menu
# ---------------------------------------------------------
help:
	@echo ""
	@echo "$(BLUE)SSRF Command Console — Available Targets$(NC)"
	@echo "--------------------------------------------------"
	@echo "$(GREEN)make bootstrap$(NC)        - Create venv + install dependencies"
	@echo "$(GREEN)make run$(NC)              - Start FastAPI server (auto‑venv)"
	@echo "$(GREEN)make dev$(NC)              - Kill stale processes + validators + run"
	@echo "$(GREEN)make kill-8000$(NC)        - Kill docker‑proxy or uvicorn on port 8000"
	@echo "$(GREEN)make api$(NC)              - Run FastAPI on alternate port 8010"
	@echo "$(GREEN)make self-check$(NC)       - Validate project structure + Makefile"
	@echo "$(GREEN)make docs.all$(NC)         - Full documentation pipeline"
	@echo "$(GREEN)make docs.search$(NC)      - Build search index"
	@echo "$(GREEN)make docs.health$(NC)      - Documentation health scoring"
	@echo "$(GREEN)make docs.index$(NC)       - Generate category index"
	@echo "$(GREEN)make docs.diff$(NC)        - Drift‑diff viewer"
	@echo "$(GREEN)make test$(NC)             - Run pytest suite"
	@echo "$(GREEN)make build$(NC)            - Package operator console"
	@echo "$(GREEN)make clean$(NC)            - Remove caches"
	@echo "$(GREEN)make deepclean$(NC)        - Full cleanup including venv"
	@echo ""

# ---------------------------------------------------------
# Bootstrap Environment
# ---------------------------------------------------------
bootstrap:
	@test -d venv || python3 -m venv venv
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "Bootstrap complete."

# ---------------------------------------------------------
# Run FastAPI App
# ---------------------------------------------------------
run:
	@echo "Starting SSRF Command Console..."
	@. venv/bin/activate && uvicorn app.main:app --reload

# Alternate port
api:
	@echo "Starting API on port 8010..."
	@. venv/bin/activate && uvicorn app.main:app --reload --port 8010

# ---------------------------------------------------------
# Dev Mode (Kill stale processes + validators + run)
# ---------------------------------------------------------
dev: kill-8000 self-check run

# ---------------------------------------------------------
# Kill stale Uvicorn or docker-proxy on port 8000
# ---------------------------------------------------------
kill-8000:
	@echo "Killing processes on port 8000..."
	@sudo lsof -t -i:8000 | xargs -r sudo kill -9 || true
	@echo "Port 8000 cleared."

# ---------------------------------------------------------
# Self‑Check (Makefile + Structure Validator)
# ---------------------------------------------------------
self-check:
	@echo "Running Makefile + structure validation..."
	@$(PYTHON) scripts/makefile_health.py
	@echo "Self‑check complete."

# ---------------------------------------------------------
# Documentation Pipeline
# ---------------------------------------------------------
docs.all: docs.index docs.search docs.health docs.diff
	@echo "Documentation pipeline complete."

docs.search:
	@$(PYTHON) scripts/docs_search.py

docs.health:
	@$(PYTHON) scripts/docs_health.py

docs.index:
	@$(PYTHON) scripts/docs_index.py

docs.diff:
	@$(PYTHON) scripts/docs_diff.py

# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------
test:
	@echo "Running tests..."
	@$(PYTHON) -m pytest -q

# ---------------------------------------------------------
# Build / Package
# ---------------------------------------------------------
build:
	@echo "Packaging operator console..."
	@$(PYTHON) setup.py sdist bdist_wheel
	@echo "Build complete."

# ---------------------------------------------------------
# Cleanup
# ---------------------------------------------------------
clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete."

deepclean: clean
	@rm -rf venv
	@echo "Deep clean complete (venv removed)."
