# ============================================================
# SuperDoctor / CI / Structural Integrity Makefile
# ============================================================

SHELL := /bin/bash

# Colors
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m

# ============================================================
# HELP
# ============================================================

.PHONY: help
help:
	@echo -e "$(YELLOW)Available targets:$(NC)"
	@echo -e "  $(GREEN)doctor$(NC)          - Run SuperDoctor"
	@echo -e "  $(GREEN)doctor-dry$(NC)      - Run SuperDoctor in dry-run mode"
	@echo -e "  $(GREEN)doctor-fix$(NC)      - Cleanup + fix + validate structure"
	@echo -e "  $(GREEN)ci-trigger$(NC)      - Trigger GitHub Actions workflow"
	@echo -e "  $(GREEN)ci-sync-trigger$(NC) - Sync repo + trigger CI"
	@echo -e "  $(GREEN)install-prepush$(NC) - Install structural integrity pre-push hook"
	@echo -e "  $(GREEN)publish-report$(NC)  - Generate HTML report for GitHub Pages"
	@echo -e "  $(GREEN)sync$(NC)            - Git sync helper (pull + add + commit + push)"

# ============================================================
# SUPERDOCTOR COMMANDS
# ============================================================

.PHONY: doctor
doctor:
	@echo -e "$(YELLOW)=== Running SuperDoctor ===$(NC)"
	python tools/super_doctor.py

.PHONY: doctor-dry
doctor-dry:
	@echo -e "$(YELLOW)=== Running SuperDoctor (dry-run) ===$(NC)"
	python tools/super_doctor.py --dry-run

# ============================================================
# DOCTOR-FIX-CLEAN-VALIDATE PIPELINE
# ============================================================

.PHONY: doctor-fix
doctor-fix:
	@echo -e "$(YELLOW)=== Cleanup incorrect __init__.py files ===$(NC)"
	python tools/cleanup_bad_inits.py
	@echo -e "$(YELLOW)=== Fix missing __init__.py files (safe) ===$(NC)"
	python tools/fix_missing_inits.py
	@echo -e "$(YELLOW)=== Running SuperDoctor ===$(NC)"
	python tools/super_doctor.py
	@echo -e "$(YELLOW)=== Validating structure ===$(NC)"
	python tools/super_doctor.py --dry-run
	@echo -e "$(GREEN)✔ Structure validated. All checks passed.$(NC)"

# ============================================================
# GITHUB ACTIONS TRIGGERS
# ============================================================

.PHONY: ci-trigger
ci-trigger:
	@echo -e "$(YELLOW)=== Triggering SuperDoctor workflow ===$(NC)"
	gh workflow run superdoctor.yml --ref main
	@echo -e "$(GREEN)✔ Workflow triggered.$(NC)"

.PHONY: ci-sync-trigger
ci-sync-trigger:
	@echo -e "$(YELLOW)=== Syncing repo ===$(NC)"
	make sync
	@echo -e "$(YELLOW)=== Triggering SuperDoctor workflow ===$(NC)"
	gh workflow run superdoctor.yml --ref main
	@echo -e "$(GREEN)✔ Workflow triggered.$(NC)"

# ============================================================
# PRE-PUSH HOOK INSTALLER
# ============================================================

.PHONY: install-prepush
install-prepush:
	@echo -e "$(YELLOW)=== Installing pre-push hook ===$(NC)"
	mkdir -p .git/hooks
	cp tools/hooks/pre-push .git/hooks/pre-push
	chmod +x .git/hooks/pre-push
	@echo -e "$(GREEN)✔ Pre-push hook installed.$(NC)"

# ============================================================
# GITHUB PAGES REPORT PUBLISHER
# ============================================================

.PHONY: publish-report
publish-report:
	@echo -e "$(YELLOW)=== Generating HTML report ===$(NC)"
	python tools/superdoctor_html.py
	@echo -e "$(GREEN)✔ HTML report generated in reports/. Commit and push to publish.$(NC)"

# ============================================================
# SYNC HELPER
# ============================================================

.PHONY: sync
sync:
	@echo -e "$(YELLOW)=== Git sync ===$(NC)"
	git pull --rebase
	git add -A
	git commit -m "sync: automated sync"
	git push
	@echo -e "$(GREEN)✔ Sync complete.$(NC)"
