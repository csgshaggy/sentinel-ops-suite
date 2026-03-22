# ============================================================
# mk/env.mk
# Environment validation, snapshots, and diffing
# ============================================================

SHELL := /bin/bash

# ------------------------------------------------------------
# Validate environment configuration
# ------------------------------------------------------------
.PHONY: env.validate
env.validate:
	@echo "[ENV] Validating environment configuration..."
	@python3 scripts/env/validate_env.py

# ------------------------------------------------------------
# Capture baseline environment snapshot
# ------------------------------------------------------------
.PHONY: env.snapshot
env.snapshot:
	@echo "[ENV] Capturing environment snapshot..."
	@python3 scripts/env/snapshot.py

# ------------------------------------------------------------
# Compare environment snapshots
# ------------------------------------------------------------
.PHONY: env.diff
env.diff:
	@echo "[ENV] Comparing environment snapshots..."
	@python3 scripts/env/diff_snapshots.py
