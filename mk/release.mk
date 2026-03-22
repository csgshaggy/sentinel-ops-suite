# ============================================================
# mk/release.mk
# Release packaging and version stamping
# ============================================================

SHELL := /bin/bash

# ------------------------------------------------------------
# Build release artifacts
# ------------------------------------------------------------
.PHONY: release
release:
	@echo "[RELEASE] Building release artifacts..."
	@python3 scripts/release/build_release.py

# ------------------------------------------------------------
# Stamp version metadata
# ------------------------------------------------------------
.PHONY: release.version
release.version:
	@echo "[RELEASE] Stamping version metadata..."
	@python3 scripts/release/stamp_version.py
