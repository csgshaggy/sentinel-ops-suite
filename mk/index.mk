# ============================================================
# mk/index.mk — Canonical Index of Makefile Modules
# ============================================================
# This file documents the mk/ module structure and ensures
# deterministic ordering for CI drift detection.
#
# It contains NO logic, NO macros, and NO targets.
# ============================================================

# Module Order (Authoritative)
# 1. colors.mk      — ANSI color definitions
# 2. banners.mk     — reusable banners
# 3. env.mk         — environment variables
# 4. paths.mk       — canonical project paths
# 5. includes.mk    — orchestrator + shared helpers

# Notes:
# - This file is imported only by CI drift detectors.
# - The root Makefile should NOT import this file.
# - Contributors should NEVER reorder modules without approval.
# - This file acts as a contract for the Makefile architecture.
