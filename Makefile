# ============================================================
# Project Makefile — Operator‑Grade, Deterministic, Drift‑Safe
# Regenerated: 2026‑03‑22 (Upgrade 5)
# ============================================================

PYTHON := python3

# Toggle: fail CI on drift (1 = fail, 0 = warn only)
DRIFT_FAIL ?= 1
export DRIFT_FAIL

# ------------------------------------------------------------
# HELP
# ------------------------------------------------------------
.PHONY: help
help:
	@echo ""
	@echo "==================== PROJECT COMMANDS ===================="
	@echo "Application:"
	@echo "  run                 Run the main application (run.py)"
	@echo "  run.sh              Run the shell wrapper"
	@echo "  ops                 Launch operator console (ops.sh)"
	@echo ""
	@echo "Documentation:"
	@echo "  docs.all            Run all documentation governance tasks"
	@echo "  docs.health         Score documentation health"
	@echo "  docs.index          Generate documentation index"
	@echo "  docs.diff           Compare docs against baseline"
	@echo ""
	@echo "Doctor Suite (Plugin-Based):"
	@echo "  doctor              Run all validators (auto-discovered)"
	@echo "  drift.reset         Regenerate structure baseline (with confirmation)"
	@echo ""
	@echo "CI Controls:"
	@echo "  DRIFT_FAIL=0 make doctor.drift   # warn only"
	@echo "  DRIFT_FAIL=1 make doctor.drift   # fail on drift"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean               Remove caches and temporary files"
	@echo "=========================================================="
	@echo ""

# ------------------------------------------------------------
# APPLICATION
# ------------------------------------------------------------
.PHONY: run
run:
	$(PYTHON) run.py

.PHONY: run.sh
run.sh:
	./run.sh

.PHONY: ops
ops:
	./ops.sh

# ------------------------------------------------------------
# DOCUMENTATION GOVERNANCE
# ------------------------------------------------------------
.PHONY: docs.all
docs.all: docs.health docs.index docs.diff

.PHONY: docs.health
docs.health:
	$(PYTHON) scripts/docs_health.py

.PHONY: docs.index
docs.index:
	$(PYTHON) scripts/docs_index.py

.PHONY: docs.diff
docs.diff:
	$(PYTHON) scripts/docs_diff.py

# ------------------------------------------------------------
# DOCTOR SUITE (PLUGIN LOADER)
# ------------------------------------------------------------
.PHONY: doctor
doctor:
	$(PYTHON) scripts/doctor/doctor_loader.py

# Drift detection (still available as a standalone)
.PHONY: doctor.drift
doctor.drift:
	@bash scripts/doctor/drift.sh

# Baseline reset
.PHONY: drift.reset
drift.reset:
	@bash scripts/doctor/drift_reset.sh

# ------------------------------------------------------------
# MAINTENANCE
# ------------------------------------------------------------
.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
