# Modular Makefile System

The SSRF Command Console uses a fully modular, deterministic Makefile architecture designed for clarity, maintainability, and CI enforcement. Each subsystem lives in its own `mk/*.mk` module, and the root `Makefile` simply includes them.

## Modules

### `mk/core.mk`
Core operational targets:
- `bootstrap`
- `clean`
- `env.inspect`
- `deps.graph`

### `mk/docs.mk`
Documentation utilities:
- `self-check`
- `plugins.load`

### `mk/validate.mk`
Validation pipeline:
- `validate`
- `validate.python`
- `validate.js`
- `validate.structure`
- `validate.drift`

### `mk/util.mk`
Utility functions:
- `print.green`
- `print.red`
- `print.yellow`

### `mk/audit.mk`
Makefile integrity checks:
- `self.audit`  
Ensures:
- no unexpected mk files  
- no duplicate targets  

### `mk/release.mk`
Release pipeline:
- `release`
- `release.version`
- `release.tag`

### `mk/env.mk`
Environment snapshot + diff:
- `env.snapshot`
- `env.diff`
- `env.validate`

## CI Integration

GitHub Actions runs:

make validate


This ensures:
- no drift  
- no structural issues  
- no broken Makefile modules  

## Release Integration

Releases are created via:

make release


This:
- writes/initializes `VERSION`
- creates a Git tag
- triggers the GitHub Release workflow
