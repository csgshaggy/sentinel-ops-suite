# ============================================
# Dashboard Makefile
# Location: dashboard/Makefile
# Purpose: Unified test + dev automation
# ============================================

SHELL := /bin/bash

# Colors
GREEN := \033[0;32m
BLUE  := \033[0;34m
CYAN  := \033[0;36m
RESET := \033[0m

# --------------------------------------------
# HELP
# --------------------------------------------
.PHONY: help
help:
	@echo -e "$(CYAN)Dashboard Makefile Targets$(RESET)"
	@echo -e "$(BLUE)make dev$(RESET)            - Start Vite dev server"
	@echo -e "$(BLUE)make test-unit$(RESET)       - Run Vitest unit tests"
	@echo -e "$(BLUE)make test-ui$(RESET)         - Run Playwright E2E tests"
	@echo -e "$(BLUE)make test-ui-ci$(RESET)      - Run Playwright tests in CI mode"
	@echo -e "$(BLUE)make install$(RESET)         - Install npm dependencies"
	@echo -e "$(BLUE)make browsers$(RESET)        - Install Playwright browsers"
	@echo -e "$(BLUE)make clean$(RESET)           - Remove node_modules + lockfile"

# --------------------------------------------
# INSTALLATION
# --------------------------------------------
.PHONY: install
install:
	npm install

.PHONY: browsers
browsers:
	npx playwright install --with-deps

# --------------------------------------------
# DEVELOPMENT
# --------------------------------------------
.PHONY: dev
dev:
	npm run dev

# --------------------------------------------
# UNIT TESTS (VITEST)
# --------------------------------------------
.PHONY: test-unit
test-unit:
	npx vitest run

# --------------------------------------------
# E2E TESTS (PLAYWRIGHT)
# --------------------------------------------
.PHONY: test-ui
test-ui:
	npx playwright test

# --------------------------------------------
# CI MODE (NO WATCH, NO HEADLESS OVERRIDE)
# --------------------------------------------
.PHONY: test-ui-ci
test-ui-ci:
	npx playwright install --with-deps
	npx playwright test --reporter=line

# --------------------------------------------
# CLEAN
# --------------------------------------------
.PHONY: clean
clean:
	rm -rf node_modules package-lock.json
