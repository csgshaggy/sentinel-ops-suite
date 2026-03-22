# SSRF Command Console — Operator-Grade Makefile

This document describes the operator-grade Makefile that drives the SSRF Command Console project.

The Makefile is designed to be:

- **Deterministic:** Every target is explicit and composable.
- **Operator-focused:** Clear echo banners, safe defaults, and lifecycle coverage.
- **Tooling-aware:** Supports pip, uv, Poetry, Docker, and CI workflows.
- **Reversible:** Includes a full uninstall suite.

---

## Core targets

### `make help`

Show the banner and a categorized list of all available targets.

### `make self-check`

Run the core validator suite:

- `validators/project_structure_validator.py`
- `validators/python_import_validator.py`
- `validators/makefile_integrity_validator.py`

Use this to confirm the project is structurally sound.

### `make bootstrap`

Install Python dependencies from `requirements.txt` and install Git hooks via:

- `tools/install_git_hooks.py`

Run this when first setting up the project or after a fresh clone.

### `make repair`

Run the auto-repair script:

- `tools/auto_repair.py`

Use this when validators or CI indicate structural issues that can be auto-fixed.

### `make env-inspect`

Print:

- Python version
- Installed packages (`pip list`)
- Git status (short format)

Good for quick environment diagnostics.

### `make deps`

Generate a dependency graph via:

- `tools/dependency_graph.py`

### `make plugins`

List loaded plugins via:

- `tools/plugin_loader.py --list`

### `make release`

Build a release package via:

- `tools/build_release.py`

---

## Code quality and test targets

### `make format`

Format Python code using:

- `black .`
- `isort .`

### `make lint`

Run static analysis:

- `flake8 .`
- `mypy .`

### `make test`

Run the test suite:

- `pytest -q`

### `make clean`

Remove build artifacts and Python caches:

- `build/`, `dist/`, `*.egg-info`
- `__pycache__` and nested `*/__pycache__`

### `make rebuild`

Full rebuild pipeline:

1. `make clean`
2. `make bootstrap`
3. `make self-check`

---

## uv integration

### `make uv-bootstrap`

Install dependencies using `uv`:

- `uv pip install -r requirements.txt`

### `make uv-sync`

Sync the environment using:

- `uv sync`

### `make uv-run`

Run the application via `uv`:

- `uv run python3 main.py`

---

## Poetry integration

### `make poetry-bootstrap`

Install dependencies using Poetry:

- `poetry install`

### `make poetry-lock`

Regenerate the Poetry lockfile:

- `poetry lock`

### `make poetry-run`

Run the application via Poetry:

- `poetry run python3 main.py`

---

## Docker targets

### `make docker-build`

Build the Docker image:

- Image: `ssrf-console:latest`

### `make docker-run`

Run the container interactively and remove it on exit.

### `make docker-shell`

Open a shell (`/bin/bash`) inside the container.

### `make docker-clean`

Remove:

- All stopped containers
- The `ssrf-console:latest` image (if present)

### `make docker-rebuild`

Clean and rebuild the Docker image:

1. `make docker-clean`
2. `make docker-build`

---

## CI-aware gates

### `make ci-check`

Full CI gate:

- `make format`
- `make lint`
- `make test`
- `make self-check`

### `make ci-fast`

Fast CI gate:

- `make lint`
- `make test`

### `make ci-strict`

Strict CI:

- `flake8 .`
- `mypy .`
- `pytest -q`

### `make ci-security`

Security scan:

- `bandit -r .`

### `make ci-precommit`

Run all pre-commit hooks:

- `pre-commit run --all-files`

---

## Uninstall suite

### `make uninstall-env`

Remove local environments:

- `.venv`, `venv`, `env`
- `.uv`
- All Poetry environments (`poetry env remove --all`)

### `make uninstall-docker`

Remove:

- All containers (`docker rm -f $(docker ps -aq)`)
- The `ssrf-console:latest` image

### `make uninstall-hooks`

Remove all Git hooks:

- `.git/hooks/*`

### `make uninstall-cache`

Remove caches:

- `.pytest_cache`, `.mypy_cache`, `.cache`
- `__pycache__` and nested `*/__pycache__`

### `make uninstall`

Full uninstall pipeline:

1. `make uninstall-env`
2. `make uninstall-docker`
3. `make uninstall-hooks`
4. `make uninstall-cache`

---

## Operator notes

- Treat `make self-check` as your **baseline health check**.
- Use `make ci-check` locally before pushing to avoid CI surprises.
- Use `make uninstall` when you need a **clean slate** without deleting the repo itself.
- This Makefile is intended to be **validated** by a project-root validator to prevent accidental drift.
