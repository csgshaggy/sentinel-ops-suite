# Contributing to SSRF Command Console

Thank you for considering a contribution to the SSRF Command Console.

This project is designed as an operator‑grade toolkit. Contributions should preserve:

- Determinism
- Clear operator workflows
- Strong validation and CI coverage
- Explicit, observable behavior

---

## Getting started

1. Fork the repository.
2. Clone your fork.
3. Run:
   ```bash
   make bootstrap
   make self-check

### If you prefer uv
make uv-bootstrap

### If you prefer Poetry
make poetry-bootstrap

### Development Workflow

## Format Code
make format

## Lint +  Type Checks
make lint

## Run Tests
make test

### Full CI Gate
make ci-check

### Branching and Commits
Use descriptive branch names:
   feature/...
   fix/...
   docs/..

Write clear commit messages in imperative style
Add, Fix, Refactor, Dcoument

### Pull Requests
Before opening a PR:
1. 	Ensure the full CI gate passes:

make ci-check

2.	Ensure validators pass:

make self-check

3. Update documentation if behavior or interfaces change.

### Code Style
• 	Python: , , , 
• 	Shell: POSIX‑compatible where possible
• 	PowerShell: explicit and readable
• 	No silent failures — always echo operator‑grade messages

### Adding New Makefile Targets
• 	Preserve operator‑grade banners.
• 	Add new targets to:

	MAKEFILE.md
	/docs/makefile_reference.md

- Update validators/makefile_integrity_validator.py

### Reporting Issues
When filing an issue, include:
• 	OS and Python version
• 	Exact command(s) run
• 	Relevant logs or stack traces
• 	Output of:
	./ops or scripts/doctor.sh

This helps maintainers reproduce and diagnose issues quickly.


