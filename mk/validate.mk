# ================================
# mk/validate.mk — Validation Pipeline
# ================================

validate: validate.python validate.js validate.structure validate.drift
	@echo "[validate] All validation checks passed."

validate.python:
	@echo "[validate.python] Running Python lint..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 backend || { echo "[validate.python] flake8 reported issues."; exit 1; }; \
	else \
		echo "[validate.python] flake8 not installed, skipping."; \
	fi

validate.js:
	@echo "[validate.js] Running JS/TS lint..."
	@if [ -f dashboard/package.json ]; then \
		if command -v eslint >/dev/null 2>&1; then \
			if npm run lint --prefix dashboard >/dev/null 2>&1; then \
				echo "[validate.js] Lint passed."; \
			else \
				echo "[validate.js] Lint reported issues."; exit 1; \
			fi; \
		else \
			echo "[validate.js] eslint not installed, skipping enforcement."; \
		fi; \
	else \
		echo "[validate.js] No dashboard/package.json found, skipping."; \
	fi

validate.structure:
	@echo "[validate.structure] Checking repo structure..."
	@test -d backend || (echo "[validate.structure] Missing backend/ directory" && exit 1)
	@test -d dashboard/src || (echo "[validate.structure] Missing dashboard/src directory" && exit 1)
	@echo "[validate.structure] Structure OK."

validate.drift:
	@echo "[validate.drift] Running drift validator..."
	@if [ -f scripts/validators/drift_validator.py ]; then \
		python3 scripts/validators/drift_validator.py || { echo "[validate.drift] Drift validator reported issues."; exit 1; }; \
	else \
		echo "[validate.drift] No drift validator found, skipping."; \
	fi
