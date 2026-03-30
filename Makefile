# =====================================================================
# SSRF Command Console — Root Makefile (Hardened + Drift-Aware)
# =====================================================================

SHELL := /bin/bash

# ---------------------------------------------------------------------
# Include modular Makefile components
# ---------------------------------------------------------------------
include mk/core.mk
include mk/env.mk
include mk/docs.mk
include mk/release.mk
include mk/validate.mk

# ---------------------------------------------------------------------
# High-level operator targets
# ---------------------------------------------------------------------

.PHONY: help
help:
	@echo ""
	@echo "=== SSRF Command Console — Operator Targets ==="
	@echo ""
	@echo "  make validate        - Run structure validator"
	@echo "  make drift-check     - Run drift-aware validator"
	@echo "  make drift-report    - Alias for drift-check"
	@echo "  make status          - Show repo status summary"
	@echo "  make clean           - Clean build artifacts"
	@echo "  make safe-clean      - Run safe_clean.sh workflow"
	@echo "  make doctor          - Full health check"
	@echo ""

# ---------------------------------------------------------------------
# Drift-Aware Validator
# ---------------------------------------------------------------------

.PHONY: drift-check
drift-check:
	@echo "=== DRIFT CHECK ==="
	@python3 scripts/validators/drift_validator.py

.PHONY: drift-report
drift-report: drift-check

# ---------------------------------------------------------------------
# Safe Clean
# ---------------------------------------------------------------------

.PHONY: safe-clean
safe-clean:
	@echo "=== SAFE CLEAN ==="
	@bash scripts/safe_clean.sh

# ---------------------------------------------------------------------
# Status Summary
# ---------------------------------------------------------------------

.PHONY: status
status:
	@echo "=== STATUS ==="
	@git status
	@echo ""
	@echo "=== VALIDATE ==="
	@python3 scripts/structure_validator.py || true
	@echo ""
	@echo "=== DRIFT CHECK ==="
	@python3 scripts/validators/drift_validator.py || true

# ---------------------------------------------------------------------
# Doctor (Full Health Check)
# ---------------------------------------------------------------------

.PHONY: doctor
doctor:
	@echo "=== DOCTOR ==="
	@echo ""
	@echo "[1/3] Structure Validator"
	@python3 scripts/structure_validator.py
	@echo ""
	@echo "[2/3] Drift-Aware Validator"
	@python3 scripts/validators/drift_validator.py
	@echo ""
	@echo "[3/3] Environment Check"
	@$(MAKE) env.inspect
	@echo ""
	@echo "Doctor complete."

# ---------------------------------------------------------------------
# Clean
# ---------------------------------------------------------------------

.PHONY: clean
clean:
	@echo "=== CLEAN ==="
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -rf build dist .pytest_cache
