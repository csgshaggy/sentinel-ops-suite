# ============================================================
# OPERATOR-GRADE MAKEFILE — WITH IDRIM + CI ENFORCEMENT
# ============================================================

SHELL := /bin/bash

# Colors
RED    := \033[31m
GREEN  := \033[32m
YELLOW := \033[33m
BLUE   := \033[34m
CYAN   := \033[36m
RESET  := \033[0m

# -----------------------------------------
# HELP
# -----------------------------------------

help:
	@echo ""
	@echo "$(CYAN)Core$(RESET)"
	@echo "  $(GREEN)make venv$(RESET)                - Create Python virtualenv"
	@echo "  $(GREEN)make install$(RESET)             - Install Python dependencies"
	@echo "  $(GREEN)make freeze$(RESET)              - Freeze requirements"
	@echo ""
	@echo "$(CYAN)Lint & Format$(RESET)"
	@echo "  $(GREEN)make lint$(RESET)                - Run Ruff lint"
	@echo "  $(GREEN)make lint-fix$(RESET)            - Auto-fix lint issues"
	@echo "  $(GREEN)make format$(RESET)              - Run Black + Prettier"
	@echo ""
	@echo "$(CYAN)Backend$(RESET)"
	@echo "  $(GREEN)make backend-run$(RESET)         - Run FastAPI backend"
	@echo "  $(GREEN)make backend-test$(RESET)        - Run backend tests"
	@echo ""
	@echo "$(CYAN)Frontend$(RESET)"
	@echo "  $(GREEN)make frontend-install$(RESET)    - Install frontend deps"
	@echo "  $(GREEN)make frontend-dev$(RESET)        - Run frontend dev server"
	@echo "  $(GREEN)make frontend-build$(RESET)      - Build frontend"
	@echo ""
	@echo "$(CYAN)PELM$(RESET)"
	@echo "  $(GREEN)make pelm-run$(RESET)            - Run PELM analysis"
	@echo "  $(GREEN)make pelm-baseline$(RESET)       - Rebuild PELM baseline"
	@echo "  $(GREEN)make pelm-diff$(RESET)           - Show PELM diff"
	@echo ""
	@echo "$(CYAN)Anomaly$(RESET)"
	@echo "  $(GREEN)make anomaly-run$(RESET)         - Run anomaly engine"
	@echo "  $(GREEN)make anomaly-score$(RESET)       - Fetch anomaly score"
	@echo ""
	@echo "$(CYAN)IDRIM$(RESET)"
	@echo "  $(GREEN)make idrim-run$(RESET)           - Run IDRIM drift analysis"
	@echo "  $(GREEN)make idrim-baseline$(RESET)      - Rebuild IDRIM baseline"
	@echo "  $(GREEN)make idrim-diff$(RESET)          - Show IDRIM diff"
	@echo "  $(GREEN)make ci-idrim-baseline$(RESET)   - CI check: IDRIM baseline freshness"
	@echo ""
	@echo "$(CYAN)Repo Hygiene$(RESET)"
	@echo "  $(GREEN)make validate-structure$(RESET)  - Validate repo structure"
	@echo "  $(GREEN)make validate-makefile$(RESET)   - Validate Makefile targets"
	@echo "  $(GREEN)make validate-all$(RESET)        - Lint + structure + Makefile"
	@echo ""
	@echo "$(CYAN)Git Integrity$(RESET)"
	@echo "  $(GREEN)make git-health$(RESET)          - Run git integrity checks"
	@echo "  $(GREEN)make git-repair$(RESET)          - Attempt git repair"
	@echo "  $(GREEN)make snapshot-metadata$(RESET)   - Snapshot git metadata"
	@echo ""
	@echo "$(CYAN)Cleanup$(RESET)"
	@echo "  $(GREEN)make clean$(RESET)               - Clean caches"
	@echo "  $(GREEN)make clean-all$(RESET)           - Clean all (incl venv, node_modules)"
	@echo ""

# -----------------------------------------
# PYTHON ENVIRONMENT
# -----------------------------------------

venv:
	python3 -m venv .venv

install:
	. .venv/bin/activate && pip install -r requirements.txt

freeze:
	. .venv/bin/activate && pip freeze > requirements.txt

# -----------------------------------------
# LINTING & FORMATTING
# -----------------------------------------

lint:
	@echo "$(YELLOW)[LINT] Running Ruff...$(RESET)"
	@ruff check .

lint-fix:
	@echo "$(YELLOW)[LINT] Running Ruff with --fix...$(RESET)"
	@ruff check . --fix

format:
	@echo "$(YELLOW)[FORMAT] Running Black + Prettier...$(RESET)"
	@black .
	@prettier --write .

# -----------------------------------------
# BACKEND — FASTAPI
# -----------------------------------------

backend-run:
	@echo "$(BLUE)[BACKEND] Starting FastAPI on :8000...$(RESET)"
	@uvicorn backend.app.main:app --reload --port 8000

backend-test:
	@echo "$(BLUE)[BACKEND] Running tests...$(RESET)"
	@pytest -q

# -----------------------------------------
# FRONTEND — DASHBOARD
# -----------------------------------------

frontend-install:
	@echo "$(BLUE)[FRONTEND] Installing dependencies...$(RESET)"
	@cd frontend && npm install

frontend-dev:
	@echo "$(BLUE)[FRONTEND] Starting dev server...$(RESET)"
	@cd frontend && npm run dev

frontend-build:
	@echo "$(BLUE)[FRONTEND] Building frontend...$(RESET)"
	@cd frontend && npm run build

# -----------------------------------------
# PELM — Privilege Escalation & Lateral Movement
# -----------------------------------------

pelm-run:
	@echo "$(CYAN)[PELM] Running PELM analysis...$(RESET)"
	@curl -s http://localhost:8000/pelm/run | jq .

pelm-baseline:
	@echo "$(CYAN)[PELM] Rebuilding PELM baseline...$(RESET)"
	@curl -s -X POST http://localhost:8000/pelm/baseline/rebuild | jq .

pelm-diff:
	@echo "$(CYAN)[PELM] Computing PELM diff...$(RESET)"
	@curl -s http://localhost:8000/pelm/diff | jq .

# -----------------------------------------
# ANOMALY SUBSYSTEM
# -----------------------------------------

anomaly-run:
	@echo "$(CYAN)[ANOMALY] Running anomaly engine...$(RESET)"
	@curl -s http://localhost:8000/anomaly/run | jq .

anomaly-score:
	@echo "$(CYAN)[ANOMALY] Fetching anomaly score...$(RESET)"
	@curl -s http://localhost:8000/anomaly/score | jq .

# -----------------------------------------
# IDRIM — IAM Drift & Role Integrity Monitor
# -----------------------------------------

idrim-run:
	@echo "$(CYAN)[IDRIM] Running IDRIM drift analysis...$(RESET)"
	@curl -s http://localhost:8000/idrim/run | jq .

idrim-baseline:
	@echo "$(CYAN)[IDRIM] Rebuilding IDRIM IAM baseline...$(RESET)"
	@curl -s -X POST http://localhost:8000/idrim/baseline/rebuild | jq .

idrim-diff:
	@echo "$(CYAN)[IDRIM] Computing IDRIM baseline diff...$(RESET)"
	@curl -s http://localhost:8000/idrim/diff | jq .

# -----------------------------------------
# CI: IDRIM BASELINE FRESHNESS
# -----------------------------------------

ci-idrim-baseline:
	@echo "$(YELLOW)[CI][IDRIM] Checking baseline freshness...$(RESET)"
	@if [ ! -f idrim_baseline.json ]; then \
		echo "$(RED)[CI][IDRIM] Baseline file missing: idrim_baseline.json$(RESET)"; \
		exit 1; \
	fi
	@TS=$$(jq -r '.timestamp // empty' idrim_baseline.json); \
	if [ -z "$$TS" ] || [ "$$TS" = "null" ]; then \
		echo "$(RED)[CI][IDRIM] Baseline missing or stale (timestamp not found).$(RESET)"; \
		exit 1; \
	fi; \
	echo "$(GREEN)[CI][IDRIM] Baseline timestamp OK: $$TS$(RESET)"

# -----------------------------------------
# REPO HYGIENE & STRUCTURE VALIDATION
# -----------------------------------------

validate-structure:
	@echo "$(YELLOW)[VALIDATE] Checking repo structure...$(RESET)"
	@python tools/validators/structure_validator.py

validate-makefile:
	@echo "$(YELLOW)[VALIDATE] Checking Makefile targets...$(RESET)"
	@python tools/validators/makefile_validator.py

validate-all: lint validate-structure validate-makefile

# -----------------------------------------
# GIT INTEGRITY & SNAPSHOTS
# -----------------------------------------

git-health:
	@echo "$(YELLOW)[GIT] Running git integrity checks...$(RESET)"
	@python tools/superdoctor/git_integrity_check.py

git-repair:
	@echo "$(YELLOW)[GIT] Attempting git repair...$(RESET)"
	@python tools/superdoctor/git_repair.py

snapshot-metadata:
	@echo "$(YELLOW)[GIT] Snapshotting git metadata...$(RESET)"
	@python tools/superdoctor/snapshot_metadata.py

# -----------------------------------------
# CLEANUP
# -----------------------------------------

clean:
	@echo "$(YELLOW)[CLEAN] Removing caches...$(RESET)"
	@rm -rf __pycache__ */__pycache__ */*/__pycache__
	@rm -rf .pytest_cache
	@rm -rf .ruff_cache

clean-all: clean
	@echo "$(YELLOW)[CLEAN] Removing venv and node_modules...$(RESET)"
	@rm -rf .venv
	@rm -rf frontend/node_modules
