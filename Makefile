# ------------------------------------------------------------
# Sentinel Ops Suite — Makefile (Local‑First, Meta‑Targets, Drift Detection, Baseline History)
# Deterministic, operator‑grade, local‑ops‑friendly
# ------------------------------------------------------------

SHELL := /bin/bash

# ------------------------------------------------------------
# PHONY TARGETS
# ------------------------------------------------------------
.PHONY: \
	menu \
	sync pre-sync post-sync \
	quick-sync dev-sync \
	repo-health repo-health-snapshot repo-health-all \
	check-mfa check-structure check-docs check-deps governance-all \
	validate-makefile lint-makefile makefile-audit makefile-drift-check \
	update-makefile-baseline auto-update-baseline \
	baseline-diff baseline-rollback baseline-history-compare \
	baseline-integrity \
	governance-score \
	sync-heatmap \
	clean

# ------------------------------------------------------------
# Menu Launcher
# ------------------------------------------------------------

menu:
	@bash scripts/sync/sync-menu.sh

# ------------------------------------------------------------
# Baseline Integrity Checker
# ------------------------------------------------------------

baseline-integrity:
	@echo "🔐 Running baseline integrity check..."
	@bash scripts/sync/baseline-integrity.sh

# ------------------------------------------------------------
# Governance Score
# ------------------------------------------------------------

governance-score:
	@echo "📊 Calculating governance score..."
	@bash scripts/sync/governance-score.sh

# ------------------------------------------------------------
# Sync Heatmap
# ------------------------------------------------------------

sync-heatmap:
	@echo "🔥 Generating sync heatmap..."
	@bash scripts/sync/sync-heatmap.sh
