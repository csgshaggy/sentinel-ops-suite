# ============================================================================
# SSRF Command Console — Operator-Grade Makefile (VENV-AWARE)
# ============================================================================

PYTHON := .venv/bin/python
PIP := .venv/bin/pip
RUFF := .venv/bin/ruff
BLACK := .venv/bin/black
PRETTIER := npx prettier

# ----------------------------------------------------------------------------
# ENVIRONMENT
# ----------------------------------------------------------------------------

.PHONY: venv
venv:
	python3 -m venv .venv
	$(PIP) install --upgrade pip

.PHONY: install
install: venv
	$(PIP) install -e .[dev]

# ----------------------------------------------------------------------------
# LINTING & FORMATTING (AUTO-FIX)
# ----------------------------------------------------------------------------

.PHONY: lint
lint:
	$(RUFF) check src/ssrf_command_console --fix
	$(RUFF) format src/ssrf_command_console
	$(BLACK) src/ssrf_command_console

.PHONY: format
format:
	$(RUFF) format src/ssrf_command_console
	$(BLACK) src/ssrf_command_console

# ----------------------------------------------------------------------------
# TESTING
# ----------------------------------------------------------------------------

.PHONY: test
test:
	$(PYTHON) -m pytest --cov=ssrf_command_console

# ----------------------------------------------------------------------------
# CI-FAST (VALIDATION ONLY — NO AUTO-FIX)
# ----------------------------------------------------------------------------

.PHONY: ci-fast
ci-fast:
	@echo "[CI-FAST] Lint + Validate"
	$(RUFF) check src/ssrf_command_console
	$(RUFF) format --check src/ssrf_command_console
	$(BLACK) --check src/ssrf_command_console
	@echo "Validation complete."
