# ============================================================
# Backend Makefile — FastAPI / Python Service
# Location: backend/Makefile
# ============================================================

SHELL := /bin/bash

# Colors
GREEN := \033[0;32m
BLUE  := \033[0;34m
CYAN  := \033[0;36m
RESET := \033[0m

# Python virtual environment
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# ------------------------------------------------------------
# HELP
# ------------------------------------------------------------
.PHONY: help
help:
	@echo -e "$(CYAN)Backend Makefile — FastAPI Service$(RESET)"
	@echo -e "$(BLUE)make venv$(RESET)            - Create Python virtual environment"
	@echo -e "$(BLUE)make install$(RESET)         - Install backend dependencies"
	@echo -e "$(BLUE)make dev$(RESET)             - Start FastAPI dev server (uvicorn)"
	@echo -e "$(BLUE)make test-unit$(RESET)       - Run backend unit tests (pytest)"
	@echo -e "$(BLUE)make clean$(RESET)           - Remove venv + caches"

# ------------------------------------------------------------
# ENVIRONMENT
# ------------------------------------------------------------
$(VENV):
	python3 -m venv $(VENV)

.PHONY: venv
venv: $(VENV)

# ------------------------------------------------------------
# INSTALLATION
# ------------------------------------------------------------
.PHONY: install
install: venv
	@echo -e "$(GREEN)Installing backend dependencies...$(RESET)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# ------------------------------------------------------------
# DEVELOPMENT SERVER
# ------------------------------------------------------------
.PHONY: dev
dev: install
	@echo -e "$(GREEN)Starting FastAPI dev server...$(RESET)"
	$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# ------------------------------------------------------------
# TESTING
# ------------------------------------------------------------
.PHONY: test-unit
test-unit: install
	@echo -e "$(GREEN)Running backend unit tests...$(RESET)"
	$(PYTHON) -m pytest -q

# ------------------------------------------------------------
# CLEAN
# ------------------------------------------------------------
.PHONY: clean
clean:
	rm -rf $(VENV)
	rm -rf __pycache__ */__pycache__
	rm -rf .pytest_cache
