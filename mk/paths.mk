# ============================================================
# Canonical Path Registry
# ============================================================

# Root directories
ROOT        := $(shell pwd)
MK_DIR      := mk
TOOLS_DIR   := tools
SCRIPTS_DIR := scripts
CI_DIR      := scripts/ci
RUNTIME_DIR := runtime

# Common subpaths
DRIFT_DIR        := $(RUNTIME_DIR)/drift
DASHBOARD_DIR    := $(RUNTIME_DIR)
SNAPSHOT_DIR     := $(RUNTIME_DIR)/drift-history
