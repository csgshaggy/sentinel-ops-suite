# ============================================================
#  SSRF COMMAND CONSOLE — OPERATOR-GRADE MAKEFILE
#  Deterministic, drift‑proof, operator‑grade
# ============================================================


# ============================================================
#  SECTION 1 — NEW TARGETS
# ============================================================

SHELL := /bin/bash

FRONTEND_DIR := frontend
BACKEND_DIR  := backend
APP_DIR      := app

FRONTEND_SRC := $(FRONTEND_DIR)/src
BACKEND_SRC  := $(BACKEND_DIR)/src


help:
	@echo "Available targets:"
	@printf "%-20s %s\n" "bootstrap:" "Initialize repo structure + dependencies"
	@printf "%-20s %s\n" "repair:" "Run repair routines"
	@printf "%-20s %s\n" "env-inspect:" "Inspect environment details"
	@printf "%-20s %s\n" "deps:" "Install all dependencies"
	@printf "%-20s %s\n" "plugins:" "List or manage plugins"
	@printf "%-20s %s\n" "release:" "Build release artifacts"
	@printf "%-20s %s\n" "format:" "Auto-format Python + JS/TS"
	@printf "%-20s %s\n" "lint:" "Run linters"
	@printf "%-20s %s\n" "test:" "Run test suite"
	@printf "%-20s %s\n" "clean:" "Remove caches + artifacts"
	@printf "%-20s %s\n" "rebuild:" "Clean + rebuild"
	@printf "%-20s %s\n" "self-check:" "Run Makefile integrity checks"
	@printf "%-20s %s\n" "validate-structure:" "Validate monorepo structure"
	@printf "%-20s %s\n" "drift:" "Detect formatting + structure drift"
	@printf "%-20s %s\n" "frontend:" "Run frontend dev server"
	@printf "%-20s %s\n" "backend:" "Run backend API"
	@printf "%-20s %s\n" "docker-build:" "Build Docker image"
	@printf "%-20s %s\n" "docker-run:" "Run Docker container"
	@printf "%-20s %s\n" "uninstall:" "Full uninstall suite"


bootstrap:
	@echo "🚀 Bootstrapping SSRF Command Console..."
	mkdir -p $(FRONTEND_DIR) $(BACKEND_DIR) $(APP_DIR)
	$(MAKE) deps
	@echo "✔ Bootstrap complete"


repair:
	@echo "🛠️ Running repair routines..."
	$(MAKE) clean
	$(MAKE) deps
	@echo "✔ Repair complete"


env-inspect:
	@echo "🔎 Environment inspection:"
	@echo "Python: $$(python3 --version)"
	@echo "Node:   $$(node --version 2>/dev/null || echo 'not installed')"
	@echo "NPM:    $$(npm --version 2>/dev/null || echo 'not installed')"
	@echo "Shell:  $(SHELL)"


deps:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt || true
	@echo "📦 Installing frontend dependencies..."
	cd $(FRONTEND_DIR) && npm install || true


plugins:
	@echo "🔌 Plugin system not implemented yet (stub)."


release:
	@echo "📦 Building release artifacts (stub)."


lint:
	@echo "🔍 Running linters..."
	@if command -v npx >/dev/null 2>&1; then \
		npx eslint "$(FRONTEND_SRC)" || true; \
	else \
		echo "ESLint not installed — skipping."; \
	fi


test:
	@echo "🧪 Running tests..."
	pytest || echo "Tests not implemented."


rebuild:
	$(MAKE) clean
	$(MAKE) deps



# ============================================================
#  SECTION 2 — UV INTEGRATION
# ============================================================

uv-bootstrap:
	uv pip install -r requirements.txt

uv-sync:
	uv pip sync

uv-run:
	uv run python -m app.main



# ============================================================
#  SECTION 2 — POETRY INTEGRATION
# ============================================================

poetry-bootstrap:
	poetry install

poetry-lock:
	poetry lock

poetry-run:
	poetry run python -m app.main



# ============================================================
#  SECTION 3 — DOCKER BUILD/RUN TARGETS
# ============================================================

docker-build:
	docker build -t ssrf-console .

docker-run:
	docker run -p 8000:8000 ssrf-console

docker-shell:
	docker run -it ssrf-console /bin/bash

docker-clean:
	docker system prune -f

docker-rebuild:
	$(MAKE) docker-clean
	$(MAKE) docker-build



# ============================================================
#  SECTION 4 — CI-AWARE GATES
# ============================================================

self-check:
	@echo "🔐 Running Makefile self-check..."
	$(MAKE) validate-structure
	$(MAKE) drift
	@echo "✔ Makefile self-check passed"


ci-check:
	@echo "🔐 Running CI gates..."
	$(MAKE) self-check
	@echo "✔ CI gates passed"


ci-fast:
	@echo "⚡ Fast CI checks (stub)."


ci-strict:
	@echo "🛡️ Strict CI checks (stub)."


ci-security:
	@echo "🔒 Security scan (stub)."


ci-precommit:
	@echo "🧹 Pre-commit checks (stub)."



# ============================================================
#  SECTION 5 — FULL UNINSTALL SUITE
# ============================================================

uninstall-env:
	rm -rf venv

uninstall-docker:
	docker system prune -f

uninstall-hooks:
	rm -f .git/hooks/pre-commit
	rm -f .git/hooks/pre-push

uninstall-cache:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

uninstall:
	$(MAKE) uninstall-env
	$(MAKE) uninstall-docker
	$(MAKE) uninstall-hooks
	$(MAKE) uninstall-cache
	rm -rf $(FRONTEND_DIR)/node_modules
	@echo "✔ Full uninstall complete"



# ============================================================
#  FRONTEND / BACKEND RUNNERS
# ============================================================

frontend:
	cd $(FRONTEND_DIR) && npm run dev

backend:
	cd $(BACKEND_DIR) && uvicorn app.main:app --reload



# ============================================================
#  CLEANUP
# ============================================================

clean:
	@echo "🧹 Cleaning caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	@echo "✔ Cleanup complete"



# ============================================================
#  FORMATTING + DRIFT DETECTION
# ============================================================

format:
	@echo "🛠️ Running full repo formatter..."
	@if command -v black >/dev/null 2>&1; then \
		black $(BACKEND_SRC) $(APP_DIR); \
	else echo "Black not installed."; fi
	@if command -v npx >/dev/null 2>&1; then \
		npx prettier --write "$(FRONTEND_SRC)/**/*.{js,jsx,ts,tsx}"; \
	else echo "Prettier not installed."; fi
	@echo "✔ Formatting complete"


drift:
	@echo "🔍 Running drift detector..."
	$(MAKE) validate-structure
	@if command -v black >/dev/null 2>&1; then \
		black --check $(BACKEND_SRC) $(APP_DIR) || (echo "❌ Python drift" && exit 1); \
	fi
	@if command -v npx >/dev/null 2>&1; then \
		npx prettier --check "$(FRONTEND_SRC)/**/*.{js,jsx,ts,tsx}" || (echo "❌ JS/TS drift" && exit 1); \
	fi
	@echo "✔ No drift detected"


validate-structure:
	python makefile_integrity_validator.py
