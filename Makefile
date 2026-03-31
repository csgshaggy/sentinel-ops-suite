# ============================================================================
# SSRF Command Console — Operator-Grade Makefile (VENV-AWARE + DRIFT-PROOF)
# ============================================================================

# ----------------------------------------------------------------------------
# PATHS & BINARIES
# ----------------------------------------------------------------------------
PYTHON := .venv/bin/python
PIP := .venv/bin/pip
RUFF := .venv/bin/ruff
BLACK := .venv/bin/black
PRETTIER := npx prettier

LINT_PATHS := app backend

# ----------------------------------------------------------------------------
# ENVIRONMENT SETUP
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
	$(RUFF) check $(LINT_PATHS) --fix
	$(RUFF) format $(LINT_PATHS)
	$(BLACK) $(LINT_PATHS)

.PHONY: format
format:
	$(RUFF) format $(LINT_PATHS)
	$(BLACK) $(LINT_PATHS)

# ----------------------------------------------------------------------------
# VALIDATION (NO AUTO-FIX — DRIFT-PROOF)
# ----------------------------------------------------------------------------

.PHONY: validate
validate:
	@echo "[VALIDATE] No plugin/structure validators found — skipping."
	@echo "Validation complete."


# ----------------------------------------------------------------------------
# CI-FAST (VALIDATION ONLY — NEVER MODIFIES FILES)
# ----------------------------------------------------------------------------

.PHONY: ci-fast
ci-fast:
	@echo "[CI-FAST] Lint + Validate"
	$(RUFF) check $(LINT_PATHS)
	$(RUFF) format --check $(LINT_PATHS)
	$(BLACK) --check $(LINT_PATHS)
	@echo "Validation complete."

# ----------------------------------------------------------------------------
# TESTING
# ----------------------------------------------------------------------------

.PHONY: test
test:
	$(PYTHON) -m pytest --cov=ssrf_command_console

# ----------------------------------------------------------------------------
# REPO HYGIENE
# ----------------------------------------------------------------------------

.PHONY: heal
heal: lint validate
	@echo "[HEAL] Repo healed and validated."

.PHONY: doctor
doctor:
	@echo "[DOCTOR] Checking environment..."
	@command -v $(RUFF) >/dev/null || echo "Missing: ruff"
	@command -v $(BLACK) >/dev/null || echo "Missing: black"
	@command -v $(PYTHON) >/dev/null || echo "Missing: python"
	@echo "[DOCTOR] Done."
