# ------------------------------------------------------------
# Sentinel Ops Suite — Makefile (Regenerated with PHONY targets)
# Deterministic, operator‑grade, CI‑safe
# ------------------------------------------------------------

SHELL := /bin/bash

# ------------------------------------------------------------
# PHONY TARGETS
# ------------------------------------------------------------
.PHONY: \
    sync pre-sync post-sync \
    repo-health repo-health-snapshot \
    check-mfa check-structure check-docs check-deps \
    validate-makefile lint-makefile \
    clean

# ------------------------------------------------------------
# Repo Health
# ------------------------------------------------------------

repo-health:
	@echo "🔍 Running RepoHealth..."
	cd frontend && npx ts-node src/dashboard/repo-health/runRepoHealth.ts

repo-health-snapshot:
	@echo "📊 Capturing repo health snapshot..."
	cd frontend && npx ts-node src/dashboard/repo-health/runRepoHealth.ts --snapshot

# ------------------------------------------------------------
# Governance Checks
# ------------------------------------------------------------

check-mfa:
	@node scripts/governance/governance-mfa-check.cjs

check-structure:
	@node scripts/governance/governance-structure-check.cjs

check-docs:
	@node scripts/governance/governance-docs-check.cjs

check-deps:
	@node scripts/governance/governance-deps-check.cjs

validate-makefile:
	@node scripts/make/validate-makefile.cjs

lint-makefile:
	@echo "🔍 Linting Makefile with checkmake..."
	@if command -v checkmake >/dev/null 2>&1; then \
		checkmake Makefile; \
	else \
		echo "⚠️ checkmake not found, skipping Makefile lint"; \
	fi

# ------------------------------------------------------------
# Sync Pipeline
# ------------------------------------------------------------

pre-sync:
	@echo "🔍 Running pre-sync validation..."
	@node scripts/preflight/pre-sync-validate.cjs

post-sync:
	@echo "📊 Running post-sync health snapshot..."
	$(MAKE) repo-health-snapshot
	@echo "🔍 Running post-sync governance checks..."
	$(MAKE) check-mfa
	$(MAKE) check-structure
	$(MAKE) check-docs
	$(MAKE) check-deps
	$(MAKE) validate-makefile
	$(MAKE) lint-makefile

sync:
	@echo "🔄 Running repository sync..."
	$(MAKE) pre-sync
	@echo "📦 Staging tracked changes..."
	git add -A
	@echo "📦 Auto-adding untracked files..."
	git add .
	@echo "📝 Committing changes..."
	git commit -m "sync: automated repository sync on $(shell date -u +'%Y-%m-%d %H:%M:%S')" || true
	@echo "📥 Fetching latest from origin..."
	git fetch origin main
	@echo "🔁 Rebasing onto origin/main..."
	git rebase origin/main || true
	@echo "📤 Pushing to origin..."
	git push origin HEAD:main
	$(MAKE) post-sync

# ------------------------------------------------------------
# Utility
# ------------------------------------------------------------

clean:
	@echo "🧹 Cleaning repo..."
	git clean -fdx
