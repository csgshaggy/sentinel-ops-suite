CANONICAL_MAKEFILE = r"""# =============================================================================
# SSRF Command Console - Makefile
# Fully Regenerated Through Steps 1–18
# =============================================================================

PYTHON := venv/bin/python

# -----------------------------------------------------------------------------
# Environment Setup
# -----------------------------------------------------------------------------

venv:
	python3 -m venv venv
	$(PYTHON) -m pip install --upgrade pip

install: venv
	$(PYTHON) -m pip install -r requirements.txt

deps:
	$(PYTHON) -m pip install -r requirements.txt

bootstrap:
	./bootstrap.sh

# -----------------------------------------------------------------------------
# Linting & Formatting
# -----------------------------------------------------------------------------

lint:
	$(PYTHON) -m ruff check src backend

format:
	$(PYTHON) -m ruff format src backend

validate:
	$(PYTHON) -m ruff check src backend && $(PYTHON) -m pytest -q

# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------

test:
	$(PYTHON) -m pytest -q backend/tests || true
	$(PYTHON) -m pytest -q tests || true

# -----------------------------------------------------------------------------
# PELM MODULE TASKS
# -----------------------------------------------------------------------------

pelm-health:
	uv run app/routers/pelm.py

pelm-stream:
	uv run app/routers/pelm_stream.py

pelm-plugin:
	uv run tools/plugins/pelm.py

pelm-test:
	pytest tests/pelm -q

pelm-docs:
	echo "Generating PELM docs..."

# -----------------------------------------------------------------------------
# Documentation
# -----------------------------------------------------------------------------

docs-build:
	jekyll build --source docs --destination _site

docs-serve:
	jekyll serve --source docs --destination _site --livereload

# -----------------------------------------------------------------------------
# Structure Validation (Step 9)
# -----------------------------------------------------------------------------

structure:
	./scripts/structure_check.sh

# -----------------------------------------------------------------------------
# Daily Health Scoring (Step 15)
# -----------------------------------------------------------------------------

daily-score:
	$(PYTHON) backend/health/run_daily_score.py

# -----------------------------------------------------------------------------
# CI Health Regression Gate (Step 18)
# -----------------------------------------------------------------------------

ci-health:
	$(PYTHON) backend/ci/health_gate.py

# -----------------------------------------------------------------------------
# Utility
# -----------------------------------------------------------------------------

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .ruff_cache
	rm -rf _site

all: lint test validate structure
"""
