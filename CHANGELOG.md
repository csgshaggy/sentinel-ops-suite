# Changelog — SSRF Command Console

All notable changes to this project will be documented in this file.

The format follows a simplified version of Keep a Changelog.

---

## [Unreleased]

### Added

- Operator‑grade Makefile with full lifecycle coverage.
- Documentation suite under `docs/` (architecture, operations, development, troubleshooting, security, Makefile reference).
- GitHub Actions CI workflow using Makefile targets.
- Helper scripts under `scripts/` (Linux/macOS).
- Windows PowerShell mirrors under `scripts/windows/`.
- Unified `ops` wrapper and TUI operator menu.
- Bootstrap wizard (`tools/bootstrap_wizard.py`).
- Makefile integrity validator (`validators/makefile_integrity_validator.py`).

### Improved

- Consistent operator‑grade echo banners across scripts.
- Deterministic environment setup workflows (pip, uv, Poetry).
- Docker build and run workflows.

### Fixed

- Structural drift issues caught by validators.
- Minor inconsistencies in Makefile target descriptions.

---

## [0.1.0] — Initial Operator Console

### Added

- Initial FastAPI backend structure.
- Basic SSRF scanning pipeline.
- Core validators:
  - `project_structure_validator.py`
  - `python_import_validator.py`
  - `makefile_integrity_validator.py`
- Initial Makefile with bootstrap, self‑check, and release targets.
