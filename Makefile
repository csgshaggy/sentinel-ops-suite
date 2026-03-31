# =====================================================================
# SSRF Command Console — Operator‑Grade Makefile
# Deterministic linting, formatting, testing, and runtime workflows
# =====================================================================

PYTHON := python
PIP := pip

# ---------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------

.PHONY: venv
venv:
	$(PYTHON) -m venv venv
	. venv/bin/activate && $(PIP) install -U pip

.PHONY: install
install:
	. venv/bin/activate && $(PIP) install -e .[dev]

# ---------------------------------------------------------------------
# Linting & Formatting
# ---------------------------------------------------------------------

.PHONY: lint
lint:
	@echo "== Running Linters =="
	ruff check .
	black --check .
	prettier -c .

.PHONY: fix
fix:
	@echo "== Auto‑fixing Codebase =="
	ruff check . --fix
	black .
	prettier -w .

# ---------------------------------------------------------------------
# Testing
# ---------------------------------------------------------------------

.PHONY: test
test:
	pytest -q

# ---------------------------------------------------------------------
# Application Runtime
# ---------------------------------------------------------------------

.PHONY: run
run:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# ---------------------------------------------------------------------
# Project Health & Structure Validation
# ---------------------------------------------------------------------

.PHONY: doctor
doctor:
	@echo "== Running Project Doctor =="
	$(PYTHON) tools/validate_structure.py

# ---------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

.PHONY: reset
reset: clean
	rm -rf venv
