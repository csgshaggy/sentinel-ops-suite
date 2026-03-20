# SSRF Command Console

![CI Status](https://github.com/csgshaggy/ssrf-command-console/actions/workflows/doctor-ci.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/csgshaggy/ssrf-command-console)
![License](https://img.shields.io/github/license/csgshaggy/ssrf-command-console)
# 🔍 Features Overview

The SSRF Command Console provides a modular, operator‑grade toolkit for analyzing, validating, and managing SSRF‑related workflows. The system is built for clarity, reproducibility, and extensibility.

## Core Features
- **Modular Architecture** — Clean separation between console logic, scripts, runtime assets, and operational tooling.
- **Automated Project Health Checks** — `doctor.py` validates imports, module placement, encoding, and structural integrity.
- **Root Cleanup & Repair Tools** — `cleanup_root.py` detects root‑owned files, misplaced modules, and environment drift.
- **Unified Dashboard Asset Pipeline** — All static files, templates, and UI assets consolidated under `scripts/`.
- **CI Integration** — GitHub Actions workflow (`doctor-ci.yml`) ensures every commit passes structural validation.
- **Operator‑Grade Makefile** — Provides deterministic commands for validation, cleanup, and environment management.
- **Extensible Mode System** — Designed for future plugin‑style scanning modes and dashboard integrations.

# 🛣️ Roadmap for v1.1.0

The next release focuses on authentication, role‑based access, and dashboard modernization.

## Planned Enhancements
### 🔐 Authentication & Security
- Add OAuth2 login flow (FastAPI‑native)
- Implement secure session cookies
- Add refresh tokens and session persistence
- Introduce RBAC (Role‑Based Access Control)

### 🖥️ Dashboard Modernization
- Replace static HTML with dynamic, authenticated dashboard views
- Add role‑based UI rendering
- Integrate real‑time scan status and logs

### 🧩 Backend Improvements
- Convert operator scripts into plugin‑style modules
- Add structured logging with timestamps and trace IDs
- Introduce environment validation hooks

### 🧪 Testing & CI
- Add unit tests for doctor and cleanup utilities
- Add integration tests for dashboard endpoints
- Expand CI to include linting and type checks

## Target Release Window
**v1.1.0 — Q2 2026**


# 🔄 Migration Notes for Developers (v1.0.0)

This release includes a full structural migration. Developers upgrading from earlier versions should review the following changes.

## Directory Changes
- All dashboard assets moved from:
src/ssrf_console/app/static/ src/ssrf_console/app/templates/ src/ssrf_console/dashboard/dashboard/ src/ssrf_console/static/static/
to scripts/.


## Removed Modules
The following modules were deprecated and removed:
- `auto_repair_structure.py`
- `fix_imports.py`
- `project_doctor.py`

## Updated Tools
- `doctor.py` now performs full project‑health validation.
- `cleanup_root.py` now detects root‑owned files and venv placement.

## Developer Actions Required
- Update any imports referencing old dashboard paths.
- Ensure your local environment uses the updated Makefile targets.
- Recreate your virtual environment if it lives inside the project root.
