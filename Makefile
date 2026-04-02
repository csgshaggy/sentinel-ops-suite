# ------------------------------------------------------------
# Sentinel Ops Suite — Makefile (Local‑First, Meta‑Targets, Drift Detection, Baseline History)
# Deterministic, operator‑grade, local‑ops‑friendly
# ------------------------------------------------------------

SHELL := /bin/bash

# ------------------------------------------------------------
# PHONY TARGETS
# ------------------------------------------------------------
.PHONY: \
	sync pre-sync post-sync \
	quick-sync dev-sync \
	repo-health repo-health-snapshot repo-health-all \
	check-mfa check-structure check-docs check-deps governance-all \
	validate-makefile lint-makefile makefile-audit makefile-drift-check \
	update-makefile-baseline auto-update-baseline \
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

repo-health-all:
	@echo "📊 Running full repo health suite..."
	$(MAKE) repo-health
	$(MAKE) repo-health-snapshot

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

governance-all:
	@echo "🛡️ Running full governance suite..."
	$(MAKE) check-mfa
	$(MAKE) check-structure
	$(MAKE) check-docs
	$(MAKE) check-deps

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
# Makefile Self-Audit & Drift Detection (Local‑First)
# ------------------------------------------------------------

makefile-drift-check:
	@echo "🧭 Checking Makefile drift..."
	@STRICT=$(STRICT) node scripts/make/makefile-drift-check.cjs

makefile-audit:
	@echo "🔍 Running Makefile self-audit..."
	$(MAKE) validate-makefile
	$(MAKE) lint-makefile
	$(MAKE) makefile-drift-check

update-makefile-baseline:
	@echo "📌 Updating Makefile baseline..."
	@mkdir -p .meta/makefile/history
	@if [ -f .meta/makefile/Makefile.baseline ]; then \
		cp .meta/makefile/Makefile.baseline .meta/makefile/history/Makefile.$(shell date -u +'%Y%m%d-%H%M%S').bak; \
		echo "🗄️ Archived previous baseline."; \
	fi
	@cp Makefile .meta/makefile/Makefile.baseline
	@echo "✅ Baseline updated."

auto-update-baseline:
	@echo "📌 Updating Makefile baseline and committing..."
	$(MAKE) update-makefile-baseline
	git add .meta/makefile/Makefile.baseline
	git add .meta/makefile/history
	git commit -m "baseline: updated Makefile baseline on $(shell date -u +'%Y-%m-%d %H:%M:%S')" || true
	git push origin HEAD:main
	@echo "✅ Baseline updated and committed."

# ------------------------------------------------------------
# Fast Sync Variants
# ------------------------------------------------------------

quick-sync:
	@echo "⚡ Running quick sync (no governance, no snapshots)..."
	git add -A
	git add .
	git commit -m "quick-sync: $(shell date -u +'%Y-%m-%d %H:%M:%S')" || true
	git fetch origin main
	git rebase origin/main || true
	git push origin HEAD:main
	@echo "⚡ Quick sync complete."

dev-sync:
	@echo "🛠️ Running dev sync (governance only, no snapshots)..."
	$(MAKE) check-mfa
	$(MAKE) check-structure
	$(MAKE) check-docs
	$(MAKE) check-deps
	@echo "📦 Staging changes..."
	git add -A
	git add .
	git commit -m "dev-sync: $(shell date -u +'%Y-%m-%d %H:%M:%S')" || true
	git fetch origin main
	git rebase origin/main || true
	git push origin HEAD:main
	@echo "🛠️ Dev sync complete."

# ------------------------------------------------------------
# Full Sync Pipeline
# ------------------------------------------------------------

pre-sync:
	@echo "🔍 Running pre-sync validation..."
	@node scripts/preflight/pre-sync-validate.cjs

post-sync:
	@echo "📊 Running post-sync health snapshot..."
	$(MAKE) repo-health-all
	@echo "🔍 Running post-sync governance checks..."
	$(MAKE) governance-all
	$(MAKE) makefile-audit

sync:
	@echo "🔄 Running full repository sync..."
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
