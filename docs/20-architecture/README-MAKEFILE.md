# Makefile System — README

## Overview

This project uses a **hybrid Makefile architecture** designed for:

- Deterministic builds
- Modular maintainability
- Validator‑friendly structure
- Operator‑grade clarity
- Extensibility through module files

The root `Makefile` acts as a **dispatcher**, while all operational logic lives inside `mk/*.mk` modules.

This README documents the structure, purpose, and usage of the Makefile system.

---

# Directory Layout

```
Makefile
mk/
  core.mk
  docs.mk
  env.mk
  release.mk
  validate.mk
scripts/
  bootstrap.py
  validate_makefile.py
  deps/
    generate_graph.py
  env/
    inspect.py
    validate_env.py
    snapshot.py
    diff_snapshots.py
  docs/
    health_score.py
    generate_index.py
    diff_docs.py
  plugins/
    load_plugins.py
docs/
  MAKEFILE.md (this file)
```

---

# Architecture Summary

### Root Makefile

- Contains help banner
- Defines high‑level phony targets
- Includes module files
- Contains _no operational logic_

### Module Files (`mk/*.mk`)

Each module contains a logically grouped set of targets:

| Module        | Purpose                                                                              |
| ------------- | ------------------------------------------------------------------------------------ |
| `core.mk`     | Bootstrap, clean, self‑check, environment inspector, dependency graph, plugin loader |
| `docs.mk`     | Documentation governance (health, index, drift)                                      |
| `env.mk`      | Environment validation, snapshots, diffs                                             |
| `release.mk`  | Release packaging and version stamping                                               |
| `validate.mk` | Makefile structure validation and ordering enforcement                               |

---

# Core Targets

### bootstrap

Initializes environment and dependencies.

### clean

Removes build artifacts.

### self-check

Runs Makefile structure validation.

### env.inspect

Prints environment details.

### deps.graph

Generates dependency graph.

### plugins.load

Loads and validates plugins.

---

# Documentation Targets

### docs.all

Runs all documentation governance tasks.

### docs.health

Scores documentation health.

### docs.index

Generates documentation index.

### docs.diff

Shows documentation drift.

---

# Environment Targets

### env.validate

Validates environment configuration.

### env.snapshot

Captures baseline environment snapshot.

### env.diff

Compares environment snapshots.

---

# Release Targets

### release

Builds release artifacts.

### release.version

Stamps version metadata.

---

# Validation Targets

### validate.structure

Runs strict Makefile structure validator.

### validate.order

Checks deterministic ordering.

### validate.all

Runs full validation suite.

---

# Design Principles

### 1. Deterministic

All targets are grouped and ordered consistently to satisfy your validator.

### 2. Modular

Logic is separated into modules for clarity and maintainability.

### 3. Observable

Every target prints clear operator‑grade output.

### 4. Extensible

New modules can be added without modifying existing ones.

### 5. Drift‑Resistant

Documentation and Makefile validators ensure long‑term consistency.

---

# Validation Workflow

To validate the entire Makefile system:

```
make validate.all
```

To validate structure only:

```
make validate.structure
```

To validate ordering:

```
make validate.order
```

---

# Usage Examples

Initialize environment:

```
make bootstrap
```

Generate documentation index:

```
make docs.index
```

Build release artifacts:

```
make release
```

Inspect environment:

```
make env.inspect
```

---

# Extending the System

To add a new module:

1. Create a new file under `mk/` (e.g., `mk/security.mk`)
2. Add your targets
3. Add an include line to the root `Makefile`:

```
include mk/security.mk
```

4. Update your validator rules if needed

---

# Summary

This Makefile system is:

- Modular
- Deterministic
- Validator‑aligned
- Operator‑grade
- Easy to extend
- Easy to maintain

It provides a clean, predictable workflow for building, validating, documenting, and releasing your project.
