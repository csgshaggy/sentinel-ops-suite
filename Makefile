# ============================================
# Sentinel Ops — Unified Operator Makefile
# Regenerated for ops_dir + ops wrapper layout
# ============================================

SHELL := /bin/bash

# -------------------------
# Core Paths
# -------------------------
OPS_WRAPPER := ./ops
OPS_DIR     := ./ops_dir
SELF_HEAL   := $(OPS_DIR)/self-heal.sh

# -------------------------
# Python / Backend
# -------------------------
VENV := .venv
PYTHON := $(VENV)/bin/python

.PHONY: venv install run backend

venv:
	python3 -m venv $(VENV)

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) run.py

backend:
	cd backend && $(PYTHON) main.py

# -------------------------
# Frontend
# -------------------------
.PHONY: frontend frontend-install frontend-build frontend-dev

frontend-install:
	cd frontend && npm install

frontend-build:
	cd frontend && npm run build

frontend-dev:
	cd frontend && npm run dev

# -------------------------
# Sync Pipeline
# -------------------------
.PHONY: sync pre-sync validate-sync

sync:
	@echo "🔄 Starting repository sync..."
	@$(MAKE) pre-sync
	@bash scripts/sync/sync.sh

pre-sync:
	@echo "🔍 Running pre-sync validator..."
	@node scripts/sync/pre-sync-validate.mjs

validate-sync:
	@echo "🔍 Validating sync..."
	@bash scripts/sync/validate.sh

# -------------------------
# Ops CLI Targets
# -------------------------
.PHONY: ops-help ops-health ops-bootstrap ops-drift ops-validate ops-checksum ops-self-heal ops-self-heal-dry

ops-help:
	@$(OPS_WRAPPER) help

ops-health:
	@echo "== Sentinel Ops — Ops Health =="
	@$(MAKE) sync
	@$(MAKE) ops-bootstrap
	@bash "$(SELF_HEAL)"

ops-bootstrap:
	@echo "== Sentinel Ops — Bootstrap =="
	@mkdir -p "$(OPS_DIR)"
	@echo "[ops-bootstrap] Using ops directory: $(OPS_DIR)"

ops-drift:
	@$(OPS_WRAPPER) drift

ops-validate:
	@$(OPS_WRAPPER) validate

ops-checksum:
	@$(OPS_WRAPPER) checksum

ops-self-heal:
	@bash "$(SELF_HEAL)"

ops-self-heal-dry:
	@DRY_RUN=1 bash "$(SELF_HEAL)"

# -------------------------
# Repo Health / Utilities
# -------------------------
.PHONY: health checksum clean

health:
	@bash scripts/health/health.sh

checksum:
	@bash scripts/checksum.sh

clean:
	rm -rf $(VENV)
	rm -rf frontend/node_modules
	rm -rf __pycache__
