# ============================================
# SSRF Command Console — Operator Makefile
# Project Root: ~/ssrf-command-console
# ============================================

PYTHON := python3
PROJECT_ROOT := $(PWD)

# -------------------------
# Core Execution Targets
# -------------------------

.PHONY: tui
tui:
	@echo "=== Running TUI Console ==="
	$(PYTHON) src/ssrf_console/console/main.py

.PHONY: backend
backend:
	@echo "=== Starting Backend ==="
	$(PYTHON) src/ssrf_console/app/main.py

.PHONY: all
all: tui backend

.PHONY: clean
clean:
	@echo "=== Cleaning Python Cache ==="
	find $(PROJECT_ROOT) -type d -name "__pycache__" -exec rm -rf {} +
	find $(PROJECT_ROOT) -type f -name "*.pyc" -delete
	@echo "=== Clean Complete ==="

# -------------------------
# Directory Structure Tools
# -------------------------

.PHONY: list-dirs
list-dirs:
	@echo "=== Directories in ssrf-command-console ==="
	@find $(PROJECT_ROOT) -maxdepth 1 -type d -printf "%f\n"

.PHONY: doctor-structure
doctor-structure:
	@echo "=== Running Structure Doctor ==="
	@$(PYTHON) tools/list_dirs.py
	@$(PYTHON) tools/normalize_root.py
	@if grep -q "BAD_DIRS = \[" tools/remove_bad_dirs.py; then \
		echo "=== Running Directory Cleanup ==="; \
		$(PYTHON) tools/remove_bad_dirs.py; \
	fi
	@echo "=== Structure Doctor Complete ==="

# -------------------------
# Import Validation
# -------------------------

.PHONY: doctor-imports
doctor-imports:
	@echo "=== Running Import Validator ==="
	$(PYTHON) scripts/validate_imports.py
	@echo "=== Import Validation Complete ==="

# -------------------------
# Unified Doctor Target
# -------------------------

.PHONY: doctor
doctor: doctor-structure doctor-imports
	@echo "=== Full Project Doctor Complete ==="

# -------------------------
# CI Target
# -------------------------

.PHONY: ci
ci: clean doctor
	@echo "=== CI Checks Complete ==="

.PHONY: help
help:
	@echo ""
	@echo "SSRF Command Console — Make Targets"
	@echo "-----------------------------------"
	@echo "  make tui              Run TUI console"
	@echo "  make backend          Start backend FastAPI app"
	@echo "  make all              Run TUI and backend"
	@echo "  make clean            Remove Python cache files"
	@echo "  make list-dirs        List top-level directories"
	@echo "  make doctor-structure Run structure checks (dirs, root, cleanup)"
	@echo "  make doctor-imports   Run import validator"
	@echo "  make doctor           Run full project doctor"
	@echo "  make ci               Run CI suite (clean + doctor)"
	@echo "  make help             Show this help menu"
	@echo ""


.PHONY: super-doctor
super-doctor:
	@echo "=== Running Super Doctor ==="
	$(PYTHON) tools/super_doctor.py
	@echo "=== Super Doctor Complete ==="
doctor: doctor-structure doctor-imports super-doctor
	@echo "=== Full Project Doctor Complete ==="

.PHONY: report
report:
	@echo "=== Running Super Doctor and Generating Report ==="
	$(PYTHON) tools/super_doctor.py
	$(PYTHON) tools/generate_super_doctor_report.py
	@echo "=== Report generation complete ==="


.PHONY: autopush
autopush:
	@echo "=== AutoPush: Running full doctor suite ==="
	make doctor || { echo 'Doctor failed — aborting push'; exit 1; }

	@echo "=== AutoPush: Staging all changes ==="
	git add -A

	@echo "=== AutoPush: Committing ==="
	git commit -m "AutoPush: $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")" || echo "No changes to commit"

	@echo "=== AutoPush: Pushing to main ==="
	git push origin main

	@echo "=== AutoPush Complete ==="
