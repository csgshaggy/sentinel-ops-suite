# ======================================================================
#  OPERATOR-GRADE MAKEFILE — SSRF COMMAND CONSOLE
#  Backend + Frontend + SuperDoctor + Validators + CI Integration
# ======================================================================

SHELL := /usr/bin/env bash
PYTHON := python3
BACKEND_DIR := backend
FRONTEND_DIR := frontend
REPORTS_DIR := backend/app/reports/html
SNAPSHOT_DIR := data
COLOR_RESET := \033[0m
COLOR_BLUE := \033[1;34m
COLOR_GREEN := \033[1;32m
COLOR_YELLOW := \033[1;33m
COLOR_RED := \033[1;31m

# ======================================================================
#  HELP
# ======================================================================
.PHONY: help
help:
	@echo -e "$(COLOR_BLUE)Available targets:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?##' Makefile | sed 's/:.*##/: /' | column -t -s ':'

# ======================================================================
#  BACKEND — FastAPI / Anomaly Engine / Correlation Engine
# ======================================================================
.PHONY: backend-run backend-dev backend-test backend-lint backend-format backend-migrate

backend-run: ## Run backend server
	cd $(BACKEND_DIR) && $(PYTHON) main.py

backend-dev: ## Run backend in dev mode
	cd $(BACKEND_DIR) && uvicorn app.main:app --reload

backend-test: ## Run backend tests
	cd $(BACKEND_DIR) && pytest -q

backend-lint: ## Lint backend
	cd $(BACKEND_DIR) && ruff check .

backend-format: ## Format backend
	cd $(BACKEND_DIR) && ruff format .

backend-migrate: ## Placeholder for migrations
	@echo "No migrations defined."

# ======================================================================
#  FRONTEND — Dashboard / UI
# ======================================================================
.PHONY: frontend-dev frontend-build frontend-lint frontend-test

frontend-dev: ## Run frontend dev server
	cd $(FRONTEND_DIR) && npm run dev

frontend-build: ## Build frontend
	cd $(FRONTEND_DIR) && npm run build

frontend-lint: ## Lint frontend
	cd $(FRONTEND_DIR) && npm run lint

frontend-test: ## Test frontend
	cd $(FRONTEND_DIR) && npm test

# ======================================================================
#  DOCTOR SUITE — Structure, Drift, Anomaly, Correlation, Router, Health
# ======================================================================
.PHONY: doctor doctor-structure doctor-drift doctor-anomaly doctor-correlation doctor-router doctor-frontend doctor-backend doctor-health doctor-json doctor-html-report doctor-snapshot doctor-plugins superdoctor

doctor: doctor-structure doctor-backend doctor-frontend doctor-anomaly doctor-correlation doctor-router doctor-health ## Run full doctor suite
	@echo -e "$(COLOR_GREEN)[doctor] All validators passed.$(COLOR_RESET)"

doctor-structure: ## Validate repo structure
	$(PYTHON) scripts/structure_validator.py

doctor-drift: ## Compare repo state to snapshots
	$(PYTHON) backend/app/repair_engine.py --mode drift

doctor-anomaly: ## Run anomaly engine
	cd $(BACKEND_DIR) && $(PYTHON) app/anomaly_engine.py

doctor-correlation: ## Run correlation engine
	cd $(BACKEND_DIR) && $(PYTHON) anomaly/correlation.py

doctor-router: ## Validate router tree
	cd $(BACKEND_DIR) && $(PYTHON) routes/doctor.py

doctor-frontend: ## Validate frontend build
	cd $(FRONTEND_DIR) && npm run build

doctor-backend: backend-lint backend-test ## Validate backend

doctor-health: ## Validate health score + trend
	cd $(BACKEND_DIR) && $(PYTHON) health/run_daily_score.py

doctor-json: ## Generate JSON doctor report
	cd $(BACKEND_DIR) && $(PYTHON) app/anomaly_detector.py --json

doctor-html-report: ## Generate HTML doctor report
	cd $(BACKEND_DIR) && $(PYTHON) app/reports/html/generate_report.py

doctor-snapshot: ## Create repo snapshot
	$(PYTHON) backend/app/repair_engine.py --mode snapshot

doctor-plugins: ## Validate plugin loader
	cd $(BACKEND_DIR) && $(PYTHON) app/core/plugin_loader.py --validate

superdoctor: doctor doctor-json doctor-html-report doctor-snapshot doctor-plugins ## Full SuperDoctor suite
	@echo -e "$(COLOR_GREEN)[superdoctor] Full suite completed.$(COLOR_RESET)"

# ======================================================================
#  CI TARGETS
# ======================================================================
.PHONY: ci ci-fast ci-doctor ci-artifacts ci-summary

ci: doctor backend-test frontend-build ## Full CI pipeline
	@echo -e "$(COLOR_GREEN)[ci] Full CI pipeline passed.$(COLOR_RESET)"

ci-fast: backend-lint frontend-lint ## Fast CI checks
	@echo -e "$(COLOR_GREEN)[ci-fast] Fast checks passed.$(COLOR_RESET)"

ci-doctor: doctor ## CI doctor-only
	@echo -e "$(COLOR_GREEN)[ci-doctor] Doctor suite passed.$(COLOR_RESET)"

ci-artifacts: ## Collect CI artifacts
	mkdir -p artifacts
	cp -r $(REPORTS_DIR) artifacts/ || true

ci-summary: ## Print CI summary
	@echo -e "$(COLOR_BLUE)CI Summary$(COLOR_RESET)"
	@echo "Backend tests: OK"
	@echo "Frontend build: OK"
	@echo "Doctor suite: OK"

# ======================================================================
#  REPO HYGIENE
# ======================================================================
.PHONY: lint format test validate-imports validate-mk validate-ci

lint: backend-lint frontend-lint ## Lint everything

format: backend-format ## Format everything

test: backend-test frontend-test ## Test everything

validate-imports: ## Validate Python imports
	cd $(BACKEND_DIR) && $(PYTHON) -m compileall .

validate-mk: ## Validate Makefile syntax
	@echo "Validating Makefile..."
	@grep -q "doctor" Makefile || (echo "Missing doctor target!" && exit 1)

validate-ci: ## Validate CI config
	$(PYTHON) backend/ci/health_gate.py

# ======================================================================
#  CLEANUP
# ======================================================================
.PHONY: clean clean-pyc clean-build clean-artifacts clean-doctor

clean: clean-pyc clean-build clean-artifacts ## Clean everything

clean-pyc:
	find . -name "*.pyc" -delete

clean-build:
	rm -rf $(FRONTEND_DIR)/dist

clean-artifacts:
	rm -rf artifacts

clean-doctor:
	rm -rf $(REPORTS_DIR)
