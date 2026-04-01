# ============================================================
#   SSRF Command Console — Makefile (Regenerated)
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
# HTML Report
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
# Enhanced Git Repair Module (Forensic Grade)
# ------------------------------------------------------------

.PHONY: git-repair
git-repair:
	@echo "[GIT-REPAIR] Starting forensic repair sequence..."

	@echo "[1/7] Validating object database..."
	git fsck --full || true

	@echo "[2/7] Cleaning orphaned packfiles..."
	find .git/objects/pack -type f -name "*.keep" -delete || true
	find .git/objects/pack -type f -name "*.old" -delete || true

	@echo "[3/7] Rebuilding missing references..."
	git show-ref --head || true
	git update-ref --no-deref HEAD HEAD || true

	@echo "[4/7] Rebuilding reflog..."
	git reflog expire --expire=now --all
	git reflog expire --expire-unreachable=now --all

	@echo "[5/7] Pruning unreachable objects..."
	git prune --expire=now --progress || true

	@echo "[6/7] Running aggressive garbage collection..."
	git gc --aggressive --prune=now

	@echo "[7/7] Final integrity check..."
	git fsck --full

	@echo "[OK] Git repair complete — repository is stable."


# ------------------------------------------------------------
# Pre‑Push Corruption Guard
# ------------------------------------------------------------

.PHONY: pre-push-guard
pre-push-guard:
	@echo "[PRE-PUSH GUARD] Running corruption and drift checks..."

	@echo "[1/6] Checking Makefile structure..."
	make self-check || { echo "[FAIL] Makefile structure invalid"; exit 1; }

	@echo "[2/6] Running fast CI checks..."
	make ci-fast || { echo "[FAIL] CI-fast checks failed"; exit 1; }

	@echo "[3/6] Validating Git object graph..."
	git fsck --full || { echo "[FAIL] Git fsck detected corruption"; exit 1; }

	@echo "[4/6] Ensuring HEAD is valid..."
	git show-ref --head > /dev/null || { echo "[FAIL] HEAD reference missing"; exit 1; }

	@echo "[5/6] Ensuring no unstaged changes..."
	git diff --quiet || { echo "[FAIL] Unstaged changes detected"; exit 1; }

	@echo "[6/6] Ensuring no untracked critical files..."
	git ls-files --others --exclude-standard | grep -E '\.py|Makefile|sync|\.sh' && { \
		echo "[FAIL] Untracked critical files detected"; exit 1; } || true

	@echo "[OK] Pre‑push guard passed — safe to push."


# ------------------------------------------------------------
# Git Metadata Snapshot
# ------------------------------------------------------------

.PHONY: git-snapshot
git-snapshot:
	@echo "[GIT-SNAPSHOT] Capturing Git metadata..."
	./tools/git_snapshot.sh


# ------------------------------------------------------------
# Git Snapshot Diff
# ------------------------------------------------------------

.PHONY: git-snapshot-diff
git-snapshot-diff:
	@echo "[GIT-SNAPSHOT-DIFF] Diffing latest two snapshots..."
	./tools/git_snapshot_diff.sh


# ------------------------------------------------------------
# Git Snapshot HTML Viewer
# ------------------------------------------------------------

.PHONY: git-snapshot-html
git-snapshot-html:
	@echo "[GIT-SNAPSHOT-HTML] Rendering latest snapshot to HTML..."
	$(PYTHON) -m backend.app.reports.html.git_snapshot_viewer


# ------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
