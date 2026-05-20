# Plugin Catalog

SuperDoctor ships with **36 plugins**, grouped into four categories:

- **System & OS Health**
- **Python Environment**
- **Project / Repo Integrity**
- **Observability & Diagnostics**

Each plugin:

- Lives in `tools/plugins/<name>.py`
- Exposes `run_checks(mode, project_root)`
- Returns a list of `CheckResult` objects
