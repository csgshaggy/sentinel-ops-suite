# ================================
# mk/core.mk — Core Build Logic
# ================================

SHELL := /bin/bash

bootstrap:
	@echo "[bootstrap] Installing dependencies..."
	@pip install -r requirements.txt >/dev/null 2>&1 || true
	@npm install --prefix dashboard >/dev/null 2>&1 || true
	@echo "[bootstrap] Done."

clean:
	@echo "[clean] Removing build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + || true
	@find . -type d -name "dist" -exec rm -rf {} + || true
	@find . -type d -name "build" -exec rm -rf {} + || true
	@echo "[clean] Done."

env.inspect:
	@echo "[env] Python: $$(python3 --version)"
	@echo "[env] Node:   $$(node --version)"
	@echo "[env] NPM:    $$(npm --version)"
	@echo "[env] Git:    $$(git --version)"

deps.graph:
	@echo "[deps] Generating dependency graph..."
	@pipdeptree || echo "pipdeptree not installed"
