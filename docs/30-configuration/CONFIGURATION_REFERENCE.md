# Configuration Reference

## Overview

This document provides a complete reference for all configuration surfaces in the SSRF Command Console, including:

- Global configuration
- MODE configuration
- Environment variables
- CLI overrides
- API configuration
- Dashboard configuration
- Filesystem paths

This is the authoritative source for operators, developers, and integrators.

---

# 1. Global Configuration

Global configuration lives in:

\`\`\`
config.yaml
\`\`\`

This file defines system‑wide defaults used by the backend, dashboard, and MODE engine.

### Example

\`\`\`
backend:
port: 5000
log_level: info

dashboard:
port: 5001

storage:
runs_dir: runs/
snapshots_dir: snapshots/

security:
allow_unauthenticated: true
\`\`\`

### Global Keys

| Key                            | Type | Description                                         |
| ------------------------------ | ---- | --------------------------------------------------- |
| backend.port                   | int  | API server port                                     |
| backend.log_level              | str  | Logging level (`debug`, `info`, `warning`, `error`) |
| dashboard.port                 | int  | Dashboard port                                      |
| storage.runs_dir               | str  | Directory for run output                            |
| storage.snapshots_dir          | str  | Directory for snapshots                             |
| security.allow_unauthenticated | bool | Enables/disables auth                               |

---

# 2. MODE Configuration

Each MODE has its own configuration file:

\`\`\`
console/modes/<mode_name>/config.py
\`\`\`

### Example

\`\`\`
DEFAULT_CONFIG = {
"timeout": 5,
"retries": 2,
"max_redirects": 3
}
\`\`\`

### Rules

- MODE config keys must be documented in `mode.yaml`
- Defaults must be deterministic
- All values must be validated in preflight

---

# 3. MODE Manifest Configuration (mode.yaml)

Each MODE includes a manifest:

\`\`\`
name: ssrf_basic_scan
version: 1.0.0
entrypoint: main:run
requires:

- network
  config:
  timeout: 5
  retries: 2
  outputs:
- raw_responses
- anomalies
  \`\`\`

### Manifest Keys

| Key        | Type | Description                           |
| ---------- | ---- | ------------------------------------- |
| name       | str  | MODE name                             |
| version    | str  | MODE version                          |
| entrypoint | str  | Python entrypoint (`module:function`) |
| requires   | list | Capabilities required by the MODE     |
| config     | dict | Default configuration values          |
| outputs    | list | Expected output artifacts             |

---

# 4. Environment Variables

Environment variables are loaded from:

\`\`\`
ssrf.env
\`\`\`

### Common Variables

| Variable             | Description             |
| -------------------- | ----------------------- |
| PYTHONPATH           | Path to console code    |
| SSRFC_BACKEND_PORT   | Backend port override   |
| SSRFC_DASHBOARD_PORT | Dashboard port override |
| LOG_LEVEL            | Global log level        |

### Rules

- Environment variables override global config
- Must not contain secrets
- Must be explicitly documented

---

# 5. CLI Overrides

CLI overrides allow operators to modify MODE configuration at runtime.

### Example

\`\`\`
console run ssrf_basic_scan --timeout 10 --retries 5
\`\`\`

### Rules

- Overrides must match keys in MODE config
- Overrides must be validated in preflight
- Overrides must be recorded in `input.json`

---

# 6. API Configuration

The API accepts configuration overrides via JSON payloads.

### Example

\`\`\`
POST /modes/ssrf_basic_scan/run
{
"targets": ["example.com"],
"config": {
"timeout": 10
}
}
\`\`\`

### Rules

- API overrides follow the same validation rules as CLI overrides
- Invalid keys must produce a structured error

---

# 7. Dashboard Configuration

Dashboard configuration is read from:

\`\`\`
config.yaml
\`\`\`

### Keys

| Key                 | Description               |
| ------------------- | ------------------------- |
| dashboard.port      | Port for dashboard server |
| dashboard.theme     | Optional UI theme         |
| dashboard.read_only | Must always be true       |

### Notes

- Dashboard is strictly read‑only
- Dashboard never writes to the filesystem

---

# 8. Filesystem Configuration

### Default Paths

\`\`\`
runs/ # Run output directories
snapshots/ # Snapshot storage
console/modes/ # MODE definitions
console/core/ # Engine internals
console/api/ # API server
dashboard/ # Dashboard UI
\`\`\`

### Rules

- All paths must be relative or absolute, never mixed
- Run directories must be immutable
- Snapshots must be immutable
- MODEs must not write outside run directories

---

# 9. Logging Configuration

Logging is controlled by:

- `LOG_LEVEL` environment variable
- `backend.log_level` in config.yaml

### Levels

- debug
- info
- warning
- error

### Log Output

\`\`\`
runs/<run_id>/logs/execution.log
\`\`\`

---

# 10. Configuration Precedence

From lowest to highest priority:

1. MODE defaults (`config.py`)
2. MODE manifest (`mode.yaml`)
3. Global config (`config.yaml`)
4. Environment variables (`ssrf.env`)
5. CLI overrides
6. API overrides

### Rule

**Higher‑priority sources always override lower‑priority ones.**

---

# 11. Validation Rules

All configuration values must be:

- Type‑checked
- Range‑checked
- Schema‑validated
- Deterministic
- Recorded in `input.json`

Invalid configuration must:

- Fail preflight
- Produce a structured error
- Never allow execution to continue

---

# Conclusion

This reference defines every configuration surface in the SSRF Command Console.
By following these rules, operators and developers ensure deterministic behavior, safe overrides, and reproducible execution across all environments.
