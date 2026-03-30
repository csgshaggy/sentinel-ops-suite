# ============================================================================
# SSRF Command Console — Operator-Grade Makefile
# ============================================================================

PYTHON := .venv/bin/python
PIP := .venv/bin/pip

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
# LINTING & FORMATTING
# ----------------------------------------------------------------------------

.PHONY: lint
lint:
	$(PYTHON) -m ruff check src/ssrf_command_console

.PHONY: format
format:
	$(PYTHON) -m ruff format src/ssrf_command_console

# ----------------------------------------------------------------------------
# TESTING
# ----------------------------------------------------------------------------

.PHONY: test
test:
	$(PYTHON) -m pytest --cov=ssrf_command_console

# ----------------------------------------------------------------------------
# STRUCTURE VALIDATION
# ----------------------------------------------------------------------------

.PHONY: structure
structure:
	$(PYTHON) scripts/structure_validator.py

# ----------------------------------------------------------------------------
# CLI STRUCTURE VALIDATION (NO HEREDOC)
# ----------------------------------------------------------------------------

.PHONY: cli-validate
cli-validate:
	$(PYTHON) scripts/cli_validator.py

# ----------------------------------------------------------------------------
# FULL DOCTOR SUITE
# ----------------------------------------------------------------------------

.PHONY: doctor
doctor:
	@echo ""
	@echo "Running full doctor suite..."
	$(MAKE) structure
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) cli-validate
	@echo ""
	@echo "All checks passed!"
	@echo ""

# ----------------------------------------------------------------------------
# CLEANUP
# ----------------------------------------------------------------------------

.PHONY: clean
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
