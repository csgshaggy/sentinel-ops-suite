![CI Status](https://github.com/csgshaggy/ssrf-command-console/actions/workflows/doctor-ci.yml/badge.svg)
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
