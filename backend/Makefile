# ============================
#  sentinel-ops-suite Backend
#  Operator-Grade Makefile
# ============================

PYTHON := .venv/bin/python
PIP := .venv/bin/pip

APP_PATH := app.main:app
HOST := 0.0.0.0
PORT := 8000

# ----------------------------
#  HELP MENU
# ----------------------------
help:
	@echo ""
	@echo "Sentinel Ops Suite — Backend Controls"
	@echo "--------------------------------------"
	@echo "make venv        - Create virtual environment"
	@echo "make install     - Install backend dependencies"
	@echo "make run         - Start FastAPI backend (dev mode)"
	@echo "make lint        - Run ruff linting"
	@echo "make fmt         - Format code with black"
	@echo "make test        - Run pytest suite"
	@echo "make clean       - Remove caches, pyc, build artifacts"
	@echo ""

# ----------------------------
#  ENVIRONMENT
# ----------------------------
venv:
	python3 -m venv .venv

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# ----------------------------
#  RUN BACKEND
# ----------------------------
run:
	$(PYTHON) -m uvicorn $(APP_PATH) --reload --host $(HOST) --port $(PORT)

# ----------------------------
#  LINT / FORMAT
# ----------------------------
lint:
	$(PYTHON) -m ruff check .

fmt:
	$(PYTHON) -m black .

# ----------------------------
#  TESTS
# ----------------------------
test:
	$(PYTHON) -m pytest -q

# ----------------------------
#  CLEANUP
# ----------------------------
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf build dist
