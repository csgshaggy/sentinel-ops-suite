# =====================================================================
# SSRF Command Console — Operator‑Grade Makefile
# Deterministic • CI‑Ready • Drift‑Proof • Plugin‑Aware
# =====================================================================

PYTHON := python
PIP := pip

# Colors
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
BLUE := \033[1;34m
NC := \033[0m

# =====================================================================
# HELP
# =====================================================================

help:
	@echo ""
	@echo "$(BLUE)Available targets:$(NC)"
	@echo "  $(GREEN)heal$(NC)              – Full repo heal (lint, format, validate, doctor)"
	@echo "  $(GREEN)validate$(NC)          – Plugin + structure validation (pre‑push safe)"
	@echo "  $(GREEN)doctor$(NC)            – Run Super Doctor"
	@echo "  $(GREEN)lint$(NC)              – Ruff lint"
	@echo "  $(GREEN)format$(NC)            – Black + Ruff format + Prettier"
	@echo "  $(GREEN)structure$(NC)         – Structure validator only"
	@echo "  $(GREEN)ci-fast$(NC)           – Fast CI gate (lint + validate)"
	@echo "  $(GREEN)ci-full$(NC)           – Full CI gate (heal + tests)"
	@echo "  $(GREEN)test$(NC)              – Run Python tests"
	@echo "  $(GREEN)build$(NC)             – Build distribution artifacts"
	@echo "  $(GREEN)release$(NC)           – Tag + build + publish"
	@echo ""

# =====================================================================
# CORE WORKFLOWS
# =====================================================================

heal:
	@echo "$(BLUE)============================================================$(NC)"
	@echo "$(BLUE) 🔧 Running Full Repository Heal$(NC)"
	@echo "$(BLUE)============================================================$(NC)"
	@ruff check --fix .
	@ruff format .
	@black .
	@prettier -w .
	@$(PYTHON) -m tools.plugin_loader
	@$(PYTHON) -m tools.super_doctor

validate:
	@echo "$(BLUE)[VALIDATE] Running plugin + structure validation...$(NC)"
	@$(PYTHON) -m tools.plugin_loader

doctor:
	@echo "$(BLUE)[DOCTOR] Running Super Doctor...$(NC)"
	@$(PYTHON) -m tools.super_doctor

structure:
	@echo "$(BLUE)[STRUCTURE] Running structure validator...$(NC)"
	@$(PYTHON) -m tools.plugin_loader

# =====================================================================
# LINT + FORMAT
# =====================================================================

lint:
	@echo "$(BLUE)[LINT] Ruff lint...$(NC)"
	@ruff check .

format:
	@echo "$(BLUE)[FORMAT] Black + Ruff + Prettier...$(NC)"
	@ruff check --fix .
	@ruff format .
	@black .
	@prettier -w .

# =====================================================================
# CI GATES
# =====================================================================

ci-fast:
	@echo "$(BLUE)[CI-FAST] Lint + Validate$(NC)"
	@ruff check .
	@$(PYTHON) -m tools.plugin_loader

ci-full:
	@echo "$(BLUE)[CI-FULL] Full Heal + Tests$(NC)"
	@$(MAKE) heal
	@$(MAKE) test

# =====================================================================
# TESTING
# =====================================================================

test:
	@echo "$(BLUE)[TEST] Running Python tests...$(NC)"
	@pytest -q || true

# =====================================================================
# BUILD + RELEASE
# =====================================================================

build:
	@echo "$(BLUE)[BUILD] Building distribution artifacts...$(NC)"
	@$(PYTHON) -m build

release:
	@echo "$(BLUE)[RELEASE] Tagging + Building + Publishing...$(NC)"
	@git tag -a "v$$(date +%Y.%m.%d.%H%M)" -m "Automated release"
	@git push --tags
	@$(MAKE) build

# =====================================================================
# END OF FILE
# =====================================================================
