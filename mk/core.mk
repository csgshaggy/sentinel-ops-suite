# ============================================================
# mk/core.mk
# Core operational targets for the hybrid Makefile system
# ============================================================

SHELL := /bin/bash

# ------------------------------------------------------------
# Bootstrap
# ------------------------------------------------------------
.PHONY: bootstrap
bootstrap:
	@echo "[BOOTSTRAP] Initializing environment..."
	@python3 scripts/bootstrap.py

# ------------------------------------------------------------
# Clean
# ------------------------------------------------------------
.PHONY: clean
clean:
	@echo "[CLEAN] Removing build artifacts..."
	@rm -rf build dist .cache __pycache__

# ------------------------------------------------------------
# Self-Check (Makefile + module integrity)
# ------------------------------------------------------------
.PHONY: self-check
self-check:
	@echo "[SELF-CHECK] Validating Makefile structure..."
	@python3 scripts/validate_makefile.py

# ------------------------------------------------------------
# Environment Inspector
# ------------------------------------------------------------
.PHONY: env.inspect
env.inspect:
	@echo "[ENV] Inspecting environment..."
	@python3 scripts/env/inspect.py

# ------------------------------------------------------------
# Dependency Graph
# ------------------------------------------------------------
.PHONY: deps.graph
deps.graph:
	@echo "[DEPS] Generating dependency graph..."
	@python3 scripts/deps/generate_graph.py

# ------------------------------------------------------------
# Plugin Loader
# ------------------------------------------------------------
.PHONY: plugins.load
plugins.load:
	@echo "[PLUGINS] Loading plugins..."
	@python3 scripts/plugins/load_plugins.py
