# Drift Detection & Integrity Enforcement  
Sentinel Ops Suite — Operator‑Grade Documentation

---

## Overview

The Sentinel Ops Suite includes a deterministic, plugin‑driven drift detection system designed to:

- Detect unexpected changes in the repository  
- Enforce CI integrity  
- Provide reproducible baselines  
- Generate snapshots and diffs  
- Block commits when drift is detected  

This document explains how drift detection works, how to operate it, and how it integrates with CI and developer workflows.

---

## Architecture

### Components

| Component | Purpose |
|----------|----------|
| `tools/drift_detector.py` | Core drift engine (baseline, snapshot, diff, check) |
| `tools/drift_modules/` | Plugin directory for drift collectors |
| `.drift/` | Storage for baseline, snapshot, and diff artifacts |
| `Makefile.drift` | Make targets for drift operations |
| `.pre-commit-config.yaml` | CI enforcement via pre‑commit hook |

### Plugin System

Drift detection is modular. Each plugin:

- Implements the `DriftPlugin` protocol  
- Exposes a `name` attribute  
- Implements `collect() -> dict`  

Current plugins:

- `filesystem_hash` — SHA256 hashes of all repo files  
- `git_metadata` — branch, commit, working tree status  

Plugins are auto‑discovered via `PLUGINS` in `drift_modules/__init__.py`.

---

## Drift Workflow

### 1. Generate Baseline

Run once after initial setup:

```bash
make drift-baseline

