# ================================
#   SSRF Command Console Makefile
#   Regenerated: Structure‑A
# ================================

SHELL := /bin/bash

# ----------------
# Python settings
# ----------------
PYTHON := python3
APP_DIR := backend/app

# ----------------
# Core commands
# ----------------

.PHONY: install
install:
	$(PYTHON) -m pip install -r requirements.txt

.PHONY: run
run:
	$(PYTHON) -m backend.app.main

# ----------------
# SuperDoctor
# ----------------

.PHONY: superdoctor
superdoctor:
	$(PYTHON) tools/super_doctor.py

# ----------------
# Sync Pipeline
# ----------------

.PHONY: sync
sync:
	@echo "=== One‑Command Sync ===" | tee -a sync.log
	./sync | tee -a sync.log
	@echo "Sync Complete" | tee -a sync.log

# ----------------
# TUI
# ----------------

.PHONY: tui
tui:
	$(PYTHON) -m backend.app.tui.main

# ----------------
# HTML Report
# ----------------

.PHONY: html-report
html-report:
	$(PYTHON) -m backend.app.reports.html.generate_report

# ----------------
# Linting
# ----------------

.PHONY: lint
lint:
	ruff check .

.PHONY: format
format:
	ruff check --fix .

# ----------------
# Tests
# ----------------

.PHONY: test
test:
	pytest -q

# ----------------
# Git Utilities (placeholder for upcoming Git integrity module)
# ----------------

.PHONY: git-health
git-health:
	@echo "Git integrity module not yet installed."

.PHONY: git-repair
git-repair:
	@echo "Git repair module not yet installed."

# ----------------
# Cleanup
# ----------------

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
