# Changelog

## [1.0.0] - 2026-03-20
### Added
- Introduced `doctor-ci.yml` GitHub Actions workflow for automated project health checks.
- Added new `scripts/` directory containing all dashboard assets, templates, and config fragments.
- Added CI test file `ci_test.txt`.

### Changed
- Migrated all static files, templates, and dashboard assets from `src/ssrf_console/...` into `scripts/`.
- Updated `doctor.py` with improved project health reporting.
- Updated `cleanup_root.py` to detect root-owned files and venv placement.
- Updated `Makefile` to support new structure and CI integration.

### Removed
- Removed legacy dashboard directories under `src/ssrf_console/app/static`, `templates`, and `dashboard/`.
- Removed deprecated modules: `auto_repair_structure.py`, `fix_imports.py`, `project_doctor.py`.
- Removed old static assets and template duplicates under `src/ssrf_console/static/` and `templates/`.

### Notes
- This release represents a full structural migration to a modular, operator‑grade layout.
- All pre‑commit hooks validated the project as clean, consistent, and dependency‑correct.
