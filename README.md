# Operator‑Grade Makefile System

![Makefile Integrity](https://github.com/csgshaggy/ssrf-command-console/actions/workflows/makefile-ci.yml/badge.svg)

![Lint & Validate](https://github.com/csgshaggy/ssrf-command-console/actions/workflows/lint.yml/badge.svg)

A fully modular, deterministic, drift‑proof Makefile architecture designed for operator consoles, CI enforcement, and reproducible workflows.  
This repository uses a clean separation of responsibilities across `mk/` modules, with strict validation, auditing, documentation governance, and release automation.

---

## 🔧 Features

- Modular Makefile system (`mk/*.mk`)
- Deterministic module loading
- Environment validation + snapshots + diffs
- Repo hygiene + drift detection
- Documentation governance + drift hashing
- Release automation with versioning + packaging
- CI workflows enforcing integrity
- Pre‑commit hooks mirroring CI behavior
- Colorized, operator‑grade output

---

## 📁 Repository Structure
Makefile mk/ util.mk core.mk env.mk validate.mk audit.mk docs.mk release.mk test.mk (optional) docs/ MAKEFILE_ARCHITECTURE.md build/ dist/ VERSION .github/ workflows/ makefile-ci.yml release.yml

---

## 🧱 Makefile Architecture Overview

The root `Makefile` contains **no business logic**.  
It delegates to modules in a deterministic order:

1. `util.mk` — shared helpers, colors, paths  
2. `core.mk` — init, clean, dependency checks  
3. `env.mk` — environment validation, snapshots, diffs  
4. `validate.mk` — structural validation, module integrity  
5. `audit.mk` — repo hygiene, drift detection, git cleanliness  
6. `docs.mk` — documentation build + drift hashing  
7. `release.mk` — versioning, packaging, artifacts  
8. `test.mk` — Makefile self‑tests (optional)

A full architecture explanation lives in:
docs/MAKEFILE_ARCHITECTURE.md


---

## 🚀 Quick Start

### Initialize the environment
```sh
make init
