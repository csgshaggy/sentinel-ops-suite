# =====================================================================
# audit.mk — Repo Hygiene / Drift
# =====================================================================

.PHONY: audit.gitclean audit.state audit.all

audit.gitclean:
	$(call util.section,Checking git working tree cleanliness)
	if ! git diff --quiet || ! git diff --cached --quiet; then \
		$(call util.warn,Git tree is not clean); \
		git status --short; \
	else \
		$(call util.ok,Git tree is clean); \
	fi

audit.state:
	$(call util.section,Checking state/ + drift artifacts)
	if [ -d "$(ROOT_DIR)/state" ]; then \
		$(call util.ok,state/ directory present); \
	else \
		$(call util.warn,state/ directory missing); \
	fi

audit.all: audit.gitclean audit.state
	$(call util.ok,Audit suite complete)
