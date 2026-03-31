# ----------------------------------------------------------------------------
# LINTING & FORMATTING (AUTO-FIX)
# ----------------------------------------------------------------------------

LINT_PATHS := app backend

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
# CI-FAST (VALIDATION ONLY — NO AUTO-FIX)
# ----------------------------------------------------------------------------

.PHONY: ci-fast
ci-fast:
	@echo "[CI-FAST] Lint + Validate"
	$(RUFF) check $(LINT_PATHS)
	$(RUFF) format --check $(LINT_PATHS)
	$(BLACK) --check $(LINT_PATHS)
	@echo "Validation complete."
