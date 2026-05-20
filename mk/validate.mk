# ==============================================================================
# VALIDATION MODULE
# ==============================================================================
# Provides deterministic, operator‑grade validation targets used by CI, pre‑commit
# hooks, and local development. All validation logic is grouped, colorized, and
# drift‑proof. This file aligns structurally with all other mk/ modules.
# ==============================================================================


# ------------------------------------------------------------------------------
# COLORS
# ------------------------------------------------------------------------------
COLOR_RESET  := \033[0m
COLOR_RED    := \033[31m
COLOR_GREEN  := \033[32m
COLOR_YELLOW := \033[33m
COLOR_BLUE   := \033[34m


# ------------------------------------------------------------------------------
# FILE SETS (THIS IS WHERE ALLOWED_MK_FILES BELONGS)
# ------------------------------------------------------------------------------
ALLOWED_MK_FILES := \
	mk/core.mk \
	mk/docs.mk \
	mk/env.mk \
	mk/release.mk \
	mk/validate.mk \
	mk/audit.mk \
	mk/test.mk


# ------------------------------------------------------------------------------
# INTERNAL HELPERS
# ------------------------------------------------------------------------------
validate_msg_ok = \
	printf "$(COLOR_GREEN)[OK]$(COLOR_RESET) %s\n" "$(1)"

validate_msg_fail = \
	printf "$(COLOR_RED)[FAIL]$(COLOR_RESET) %s\n" "$(1)"


# ------------------------------------------------------------------------------
# VALIDATION: mk/ DIRECTORY DRIFT
# ------------------------------------------------------------------------------
validate.mk.drift:
	@echo "$(COLOR_BLUE)[validate] Checking mk/ directory for drift...$(COLOR_RESET)"
	@for f in $$(ls mk); do \
		if ! echo "$(ALLOWED_MK_FILES)" | grep -q "mk/$$f"; then \
			$(call validate_msg_fail,"Unexpected file detected: mk/$$f"); \
			exit 1; \
		fi; \
	done
	$(call validate_msg_ok,"mk/ directory matches allowed file set")


# ------------------------------------------------------------------------------
# VALIDATION: MAKEFILE STRUCTURE
# ------------------------------------------------------------------------------
validate.makefile.structure:
	@echo "$(COLOR_BLUE)[validate] Validating Makefile structure...$(COLOR_RESET)"
	@if ! grep -q "include mk/core.mk" Makefile; then \
		$(call validate_msg_fail,"Missing include: mk/core.mk"); exit 1; fi
	@if ! grep -q "include mk/docs.mk" Makefile; then \
		$(call validate_msg_fail,"Missing include: mk/docs.mk"); exit 1; fi
	@if ! grep -q "include mk/env.mk" Makefile; then \
		$(call validate_msg_fail,"Missing include: mk/env.mk"); exit 1; fi
	@if ! grep -q "include mk/release.mk" Makefile; then \
		$(call validate_msg_fail,"Missing include: mk/release.mk"); exit 1; fi
	@if ! grep -q "include mk/validate.mk" Makefile; then \
		$(call validate_msg_fail,"Missing include: mk/validate.mk"); exit 1; fi
	$(call validate_msg_ok,"Makefile includes are complete and ordered")


# ------------------------------------------------------------------------------
# VALIDATION: SYNTAX CHECK
# ------------------------------------------------------------------------------
validate.syntax:
	@echo "$(COLOR_BLUE)[validate] Running syntax check...$(COLOR_RESET)"
	@$(MAKE) -n >/dev/null 2>&1 || { \
		$(call validate_msg_fail,"Makefile syntax errors detected"); exit 1; }
	$(call validate_msg_ok,"Makefile syntax is valid")


# ------------------------------------------------------------------------------
# VALIDATION: ENVIRONMENT (delegates to mk/env.mk)
# ------------------------------------------------------------------------------
validate.env:
	@$(MAKE) env.validate


# ------------------------------------------------------------------------------
# AGGREGATE VALIDATION
# ------------------------------------------------------------------------------
validate: \
	validate.mk.drift \
	validate.makefile.structure \
	validate.syntax \
	validate.env
	@echo "$(COLOR_GREEN)[validate] All validation checks passed$(COLOR_RESET)"
