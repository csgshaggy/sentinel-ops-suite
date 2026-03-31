# =====================================================================
# SSRF Command Console — Operator-Grade Makefile
# Deterministic, drift-proof, modular, and CI-aligned
# =====================================================================

SHELL := /bin/bash
PYTHON := python3
VENV := venv
PRETTIER := prettier
BLACK := black
RUFF := ruff

# ---------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------

.PHONY: venv
venv:
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@echo "[OK] Virtual environment ready."

.PHONY: install
install: venv
	@$(VENV)/bin/pip install -U pip
	@$(VENV)/bin/pip install -e .
	@$(VENV)/bin/pip install -r requirements.txt || true
	@echo "[OK] Dependencies installed."

# ---------------------------------------------------------------------
# Linting & Formatting
# ---------------------------------------------------------------------

.PHONY: ruff
ruff:
	@$(VENV)/bin/$(RUFF) check .

.PHONY: ruff-fix
ruff-fix:
	@$(VENV)/bin/$(RUFF) check . --fix

.PHONY: ruff-format
ruff-format:
	@$(VENV)/bin/$(RUFF) format .

.PHONY: black
black:
	@$(VENV)/bin/$(BLACK) .

.PHONY: prettier
prettier:
	@$(PRETTIER) -w .

# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

.PHONY: test
test:
	@$(VENV)/bin/pytest -q

# ---------------------------------------------------------------------
# Repo Hygiene
# ---------------------------------------------------------------------

.PHONY: clean
clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .pytest_cache
	@rm -rf .ruff_cache
	@echo "[OK] Cleaned caches."

.PHONY: doctor
doctor:
	@echo "[INFO] Running project doctor..."
	@$(VENV)/bin/$(PYTHON) -m tools.doctor || true

.PHONY: structure
structure:
	@echo "[INFO] Validating project structure..."
	@$(VENV)/bin/$(PYTHON) -m tools.plugin_loader --validate || true

# ---------------------------------------------------------------------
# Full Repo Heal Target
# ---------------------------------------------------------------------

.PHONY: heal
heal:
	@echo "============================================================"
	@echo " 🔧 Running Full Repository Heal"
	@echo "============================================================"
	@echo "[1/6] Ruff auto-fix..."
	@$(VENV)/bin/$(RUFF) check . --fix
	@echo "[2/6] Ruff format..."
	@$(VENV)/bin/$(RUFF) format .
	@echo "[3/6] Black formatting..."
	@$(VENV)/bin/$(BLACK) .
	@echo "[4/6] Prettier formatting..."
	@$(PRETTIER) -w .
	@echo "[5/6] Structure validation..."
	@$(VENV)/bin/$(PYTHON) -m tools.plugin_loader --validate || true
	@echo "[6/6] Doctor..."
	@$(VENV)/bin/$(PYTHON) -m tools.doctor || true
	@echo "============================================================"
	@echo " ✅ Heal complete — repo is clean, sorted, formatted, and validated."
	@echo "============================================================"

# ---------------------------------------------------------------------
# Development Server
# ---------------------------------------------------------------------

.PHONY: run
run:
	@$(VENV)/bin/uvicorn backend.main:app --reload

# ---------------------------------------------------------------------
# Default
# ---------------------------------------------------------------------

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo ""
	@echo "SSRF Command Console — Operator-Grade Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  venv           Create virtual environment"
	@echo "  install        Install dependencies"
	@echo "  ruff           Run Ruff lint"
	@echo "  ruff-fix       Run Ruff auto-fix"
	@echo "  ruff-format    Run Ruff formatter"
	@echo "  black          Run Black formatter"
	@echo "  prettier       Run Prettier formatter"
	@echo "  test           Run tests"
	@echo "  clean          Clean caches"
	@echo "  doctor         Run project doctor (tools.doctor)"
	@echo "  structure      Validate plugin structure (tools.plugin_loader)"
	@echo "  heal           Full repo cleanup (Ruff + Black + Prettier + Doctor)"
	@echo "  run            Start FastAPI dev server"
	@echo ""
