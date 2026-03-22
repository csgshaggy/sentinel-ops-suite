# ============================================================
# mk/validate.mk
# Makefile structure validation and ordering enforcement
# ============================================================

SHELL := /bin/bash

# ------------------------------------------------------------
# Validate Makefile + module structure
# ------------------------------------------------------------
.PHONY: validate.structure
validate.structure:
	@echo "[VALIDATE] Running Makefile structure validator..."
	@python3 scripts/validate_makefile.py --strict

# ------------------------------------------------------------
# Enforce deterministic ordering rules
# ------------------------------------------------------------
.PHONY: validate.order
validate.order:
	@echo "[VALIDATE] Checking target ordering..."
	@python3 scripts/validate_makefile.py --check-order

# ------------------------------------------------------------
# Full validation suite
# ------------------------------------------------------------
.PHONY: validate.all
validate.all: validate.structure validate.order
	@echo "[VALIDATE] All validation checks passed."
