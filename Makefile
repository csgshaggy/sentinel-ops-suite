# =========================================================
# SSRF Command Console — Operational Makefile
# =========================================================

SHELL := /bin/bash
REPO_ROOT := $(shell git rev-parse --show-toplevel)
SCRIPTS := $(REPO_ROOT)/scripts
RUNTIME := $(REPO_ROOT)/runtime

BLUE  := \033[94m
GREEN := \033[92m
YELLOW:= \033[93m
RED   := \033[91m
END   := \033[0m

info  = @echo -e "$(BLUE)[INFO]$(END) $1"
ok    = @echo -e "$(GREEN)[OK]$(END) $1"
warn  = @echo -e "$(YELLOW)[WARN]$(END) $1"
fail  = @echo -e "$(RED)[FAIL]$(END) $1"


# =========================================================
# Validation
# =========================================================

.PHONY: doctor
doctor:
	$(call info,"Running doctor validators...")
	@python3 $(SCRIPTS)/doctor/run_doctor.py || { $(call fail,"Doctor failed"); exit 1; }
	$(call ok,"Doctor passed.")


# =========================================================
# Drift Detection
# =========================================================

BASELINE := $(RUNTIME)/baseline.json
DRIFT_JSON := $(RUNTIME)/drift_results.json
DRIFT_MD := $(RUNTIME)/drift_dashboard.md

.PHONY: baseline
baseline:
	$(call info,"Building baseline → $(BASELINE)")
	@python3 $(SCRIPTS)/drift_detector.py --mode baseline --baseline $(BASELINE)
	$(call ok,"Baseline created.")

.PHONY: drift
drift:
	$(call info,"Running drift comparison...")
	@python3 $(SCRIPTS)/drift_detector.py --mode compare --baseline $(BASELINE) > $(DRIFT_JSON)
	$(call ok,"Drift results written to $(DRIFT_JSON)")

.PHONY: drift-dashboard
drift-dashboard:
	$(call info,"Generating drift dashboard...")
	@python3 $(SCRIPTS)/ci/drift_dashboard.py || { $(call fail,"Dashboard generation failed"); exit 1; }
	$(call ok,"Dashboard generated at $(DRIFT_MD)")


# =========================================================
# CI Targets
# =========================================================

.PHONY: ci-drift
ci-drift: drift drift-dashboard
	$(call ok,"CI drift check complete.")

.PHONY: ci-doctor
ci-doctor: doctor
	$(call ok,"CI doctor check complete.")


# =========================================================
# Utility
# =========================================================

.PHONY: paths
paths:
	$(call info,"Repo root: $(REPO_ROOT)")
	$(call info,"Scripts:   $(SCRIPTS)")
	$(call info,"Runtime:   $(RUNTIME)")

.PHONY: clean-runtime
clean-runtime:
	$(call warn,"Cleaning runtime directory...")
	@rm -f $(RUNTIME)/*.json $(RUNTIME)/*.md
	$(call ok,"Runtime cleaned.")
