# ============================================================
# Environment Variables (Canonical)
# ============================================================

# Root directory (inherited from Makefile)
export ROOT := $(ROOT)

# Python path for all tools and CI runners
export PYTHONPATH := $(ROOT)

# Drift enforcement toggle (CI + local)
# 1 = fail on drift
# 0 = warn only
export DRIFT_FAIL ?= 1

# Default Python interpreter
export PYTHON ?= python3

# Default shell for Makefile execution
export SHELL := /bin/bash
