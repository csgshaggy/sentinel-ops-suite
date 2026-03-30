# ============================================
# ROOT MAKEFILE — HARDENED EDITION
# ============================================

# Include modular Makefile components
include mk/core.mk
include mk/env.mk
include mk/docs.mk
include mk/release.mk
include mk/validate.mk

.PHONY: all
all: validate

# --------------------------------------------
# VALIDATION
# --------------------------------------------
.PHONY: validate
validate:
	@echo "=== VALIDATE ==="
	@python3 scripts/structure_validator.py
	@echo "Structure OK."

# --------------------------------------------
# SAFE CLEAN (HARDENED)
# --------------------------------------------
.PHONY: safe-clean
safe-clean:
	@echo "=== SAFE CLEAN ==="
	@./scripts/safe_clean.sh --force-clean

# --------------------------------------------
# DOCTOR
# --------------------------------------------
.PHONY: doctor
doctor:
	@python3 scripts/doctor/run_doctor.py

# --------------------------------------------
# STATUS
# --------------------------------------------
.PHONY: status
status:
	@python3 scripts/project_health.py

# --------------------------------------------
# RUN BACKEND + FRONTEND
# --------------------------------------------
.PHONY: run
run:
	@echo "Starting backend..."
	@uvicorn app.main:app --reload

.PHONY: build
build:
	@echo "Building backend + dashboard..."
	@make -C backend build
	@make -C dashboard build
