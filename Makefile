# Makefile — SSRF Command Console (CLI + backend)
# Operator-grade, deterministic targets.

PYTHON ?= python
VENV_DIR ?= venv
PIP := $(VENV_DIR)/bin/pip
PYTHON_VENV := $(VENV_DIR)/bin/python

APP_PACKAGE := ssrf_command_console

.DEFAULT_GOAL := help

# -------------------------------------------------------------------
# Environment / venv
# -------------------------------------------------------------------

$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)

.PHONY: venv
venv: $(VENV_DIR)
	@echo "[venv] Virtual environment ready at $(VENV_DIR)"

.PHONY: install
install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -e .

.PHONY: install-dev
install-dev: venv
	$(PIP) install --upgrade pip
	$(PIP) install -e .[dev]

# -------------------------------------------------------------------
# CLI targets
# -------------------------------------------------------------------

.PHONY: cli-run
cli-run:
	$(PYTHON_VENV) -m $(APP_PACKAGE).cli hello

.PHONY: cli-test
cli-test:
	$(PYTHON_VENV) -m pytest -q tests || true

# -------------------------------------------------------------------
# Backend targets (FastAPI / Uvicorn)
# -------------------------------------------------------------------

.PHONY: backend-run
backend-run:
	$(PYTHON_VENV) -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

.PHONY: backend-test
backend-test:
	$(PYTHON_VENV) -m pytest -q backend/tests || true

# -------------------------------------------------------------------
# Lint / Format / Validate
# -------------------------------------------------------------------

.PHONY: lint
lint:
	$(PYTHON_VENV) -m ruff check src backend

.PHONY: format
format:
	$(PYTHON_VENV) -m black src backend

.PHONY: format-check
format-check:
	$(PYTHON_VENV) -m black --check src backend

.PHONY: validate-structure
validate-structure:
	$(PYTHON_VENV) scripts/structure_validator.py

.PHONY: doctor
doctor: validate-structure
	$(PYTHON_VENV) -m $(APP_PACKAGE).cli doctor env
	$(PYTHON_VENV) -m $(APP_PACKAGE).cli doctor plugins
	$(PYTHON_VENV) -m $(APP_PACKAGE).cli doctor structure

# -------------------------------------------------------------------
# CI targets
# -------------------------------------------------------------------

.PHONY: test
test: backend-test cli-test

.PHONY: ci
ci: lint format-check validate-structure test

# -------------------------------------------------------------------
# Help
# -------------------------------------------------------------------

.PHONY: help
help:
	@echo "SSRF Command Console — Makefile"
	@echo ""
	@echo "Environment:"
	@echo "  make venv              Create virtual environment"
	@echo "  make install           Install package (editable)"
	@echo "  make install-dev       Install package with dev deps"
	@echo ""
	@echo "CLI:"
	@echo "  make cli-run           Run basic CLI sanity check"
	@echo "  make cli-test          Run CLI-related tests"
	@echo ""
	@echo "Backend:"
	@echo "  make backend-run       Run FastAPI backend with Uvicorn"
	@echo "  make backend-test      Run backend tests"
	@echo ""
	@echo "Quality / CI:"
	@echo "  make lint              Run Ruff lint"
	@echo "  make format            Run Black formatter"
	@echo "  make format-check      Check formatting only"
	@echo "  make validate-structure Validate repo structure"
	@echo "  make doctor            Run doctor commands"
	@echo "  make test              Run tests"
	@echo "  make ci                Full CI suite"
