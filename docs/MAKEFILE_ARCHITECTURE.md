# Makefile Architecture

This project uses a modular, operator-grade Makefile layout.

## Files

- `Makefile` — root entrypoint, delegates to modules only
- `mk/util.mk` — shared colors, helpers, paths (no targets)
- `mk/core.mk` — init, clean, dependency checks
- `mk/env.mk` — environment validation, snapshots, diffs
- `mk/validate.mk` — structure validation, module integrity, duplicate targets
- `mk/audit.mk` — repo hygiene, mk/ drift, git cleanliness, orphaned files
- `mk/docs.mk` — docs build, docs drift detection, docs governance
- `mk/release.mk` — versioning, packaging, artifacts
- `mk/test.mk` — Makefile self-test suite (if present)

## Key Targets

- `make help` — list high-level targets
- `make init` — bootstrap environment
- `make env.check` — validate environment
- `make validate` — run validation suite
- `make self.audit` — run repo hygiene checks
- `make docs` — run documentation suite
- `make release` — run release pipeline
- `make test.all` — run Makefile self-tests

## Design Principles

- Root Makefile contains no business logic
- Each module has a single responsibility
- `util.mk` is the only shared dependency
- Validation and audit are separate concerns
- CI enforces integrity via `validate.all` and `test.all`
