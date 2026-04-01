# ============================================================
#   SSRF Command Console — Makefile (Regenerated, PELM Report)
#   Structure‑A Aligned • Operator‑Grade • Drift‑Proof
# ============================================================

SHELL := /bin/bash
PYTHON := python3
APP_DIR := backend/app

# ------------------------------------------------------------
# Python Environment
# ------------------------------------------------------------

.PHONY: install
install:
	$(PYTHON) -m pip install -r requirements.txt

# ------------------------------------------------------------
# Application Entrypoints
# ------------------------------------------------------------

.PHONY: run
run:
	$(PYTHON) -m backend.app.main

# ------------------------------------------------------------
# SuperDoctor
# ------------------------------------------------------------

.PHONY: superdoctor
superdoctor:
	$(PYTHON) tools/super_doctor.py

# ------------------------------------------------------------
# Sync Pipeline
# ------------------------------------------------------------

.PHONY: sync
sync:
	@echo "=== One‑Command Sync ===" | tee -a sync.log
	./sync | tee -a sync.log
	@echo "=== Sync Complete ==="

# ------------------------------------------------------------
# TUI
# ------------------------------------------------------------

.PHONY: tui
tui:
	$(PYTHON) -m backend.app.tui.main

# ------------------------------------------------------------
# HTML Report (General)
# ------------------------------------------------------------

.PHONY: html-report
html-report:
	$(PYTHON) -m backend.app.reports.html.generate_report

# ------------------------------------------------------------
# Linting & Formatting
# ------------------------------------------------------------

.PHONY: lint
lint:
	ruff check .

.PHONY: format
format:
	ruff check --fix .

# ------------------------------------------------------------
# Tests
# ------------------------------------------------------------

.PHONY: test
test:
	pytest -q

# ------------------------------------------------------------
# Git Integrity Module
# ------------------------------------------------------------

.PHONY: self-check
self-check:
	@echo "[SELF-CHECK] Validating Makefile structure..."
	@grep -q "sync:" Makefile || { echo "[ERROR] Missing sync target"; exit 1; }
	@grep -q "tui:" Makefile || { echo "[ERROR] Missing tui target"; exit 1; }
	@grep -q "html-report:" Makefile || { echo "[ERROR] Missing html-report target"; exit 1; }
	@echo "[OK] Makefile structure validated."

.PHONY: ci-fast
ci-fast:
	@echo "[CI-FAST] Running fast CI checks..."
	ruff check .
	@echo "[OK] CI-fast checks passed."

.PHONY: git-health
git-health:
	@echo "[GIT-HEALTH] Checking repository integrity..."
	git fsck --full
	git status
	@echo "[OK] Git health check complete."

# ------------------------------------------------------------
# Enhanced Git Repair Module
# ------------------------------------------------------------

.PHONY: git-repair
git-repair:
	@echo "[GIT-REPAIR] Starting forensic repair sequence..."
	git fsck --full || true
	find .git/objects/pack -type f -name "*.keep" -delete || true
	find .git/objects/pack -type f -name "*.old" -delete || true
	git show-ref --head || true
	git update-ref --no-deref HEAD HEAD || true
	git reflog expire --expire=now --all
	git reflog expire --expire-unreachable=now --all
	git prune --expire=now --progress || true
	git gc --aggressive --prune=now
	git fsck --full
	@echo "[OK] Git repair complete."

# ------------------------------------------------------------
# Pre‑Push Corruption Guard
# ------------------------------------------------------------

.PHONY: pre-push-guard
pre-push-guard:
	@echo "[PRE-PUSH GUARD] Running corruption and drift checks..."
	make self-check
	make ci-fast
	git fsck --full
	git show-ref --head > /dev/null
	git diff --quiet
	git ls-files --others --exclude-standard | grep -E '\.py|Makefile|sync|\.sh' && { echo "[FAIL] Untracked critical files"; exit 1; } || true
	@echo "[OK] Pre‑push guard passed."

# ------------------------------------------------------------
# Git Metadata Snapshot
# ------------------------------------------------------------

.PHONY: git-snapshot
git-snapshot:
	@echo "[GIT-SNAPSHOT] Capturing Git metadata..."
	./tools/git_snapshot.sh

# ------------------------------------------------------------
# Snapshot Diff
# ------------------------------------------------------------

.PHONY: git-snapshot-diff
git-snapshot-diff:
	@echo "[GIT-SNAPSHOT-DIFF] Diffing latest two snapshots..."
	./tools/git_snapshot_diff.sh

# ------------------------------------------------------------
# Snapshot HTML Viewer
# ------------------------------------------------------------

.PHONY: git-snapshot-html
git-snapshot-html:
	@echo "[GIT-SNAPSHOT-HTML] Rendering latest snapshot to HTML..."
	$(PYTHON) -m backend.app.reports.html.git_snapshot_viewer

# ------------------------------------------------------------
# Snapshot Dashboard Target
# ------------------------------------------------------------

.PHONY: git-snapshot-dashboard
git-snapshot-dashboard:
	@echo "[GIT-SNAPSHOT-DASHBOARD] Generating snapshot + HTML..."
	make git-snapshot
	make git-snapshot-html

# ------------------------------------------------------------
# Snapshot Retention Policy
# ------------------------------------------------------------

.PHONY: git-snapshot-clean
git-snapshot-clean:
	@echo "[GIT-SNAPSHOT-CLEAN] Applying retention policy..."
	./tools/git_snapshot_cleanup.sh

# ------------------------------------------------------------
# PELM HTML Report
# ------------------------------------------------------------

.PHONY: pelm-report
pelm-report:
	@echo "[PELM-REPORT] Generating PELM HTML report..."
	$(PYTHON) -m backend.app.reports.html.pelm_report

# ------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
