# SSRF Command Console — Full Manual

## Overview

This manual provides a complete, unified reference for operators, developers, MODE authors, and system administrators working with the SSRF Command Console.

It consolidates the entire documentation suite into a single, structured guide covering:

- Installation
- Architecture
- MODE authoring
- Operation
- API usage
- Security
- Testing
- Deployment
- Hardening
- Roadmap

This is the authoritative manual for the project.

---

# 1. Introduction

## 1.1 What is the SSRF Command Console?

A deterministic, artifact‑driven framework for executing SSRF‑focused MODEs, analyzing results, and visualizing output through a dashboard.

## 1.2 Key Features

- Deterministic MODE lifecycle
- Immutable run directories
- Structured artifacts
- Snapshot & diff engine
- Dashboard visualization
- Strict MODE isolation
- Operator‑grade logging

---

# 2. Installation & Setup

## 2.1 Requirements

- Python 3.10+
- Git
- Linux, macOS, or Windows (native or WSL2)

## 2.2 Installation Steps

\`\`\`
git clone https://github.com/<your-org>/ssrf-console.git
cd ssrf-console
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

## 2.3 Verify Installation

\`\`\`
python -m console
python -m dashboard
\`\`\`

---

# 3. Architecture Overview

## 3.1 High-Level Components

- **MODE Engine** — Executes MODEs deterministically
- **API Server** — Exposes MODE execution and run retrieval
- **Dashboard** — Read‑only visualization layer
- **Storage Layer** — Immutable run directories + snapshots
- **MODEs** — Modular execution units

## 3.2 Data Flow

\`\`\`
Operator → API → MODE Engine → Artifacts → Dashboard
\`\`\`

## 3.3 MODE Lifecycle

\`\`\`
Load → Preflight → Execute → Postprocess → Emit
\`\`\`

---

# 4. MODE Authoring

## 4.1 Directory Structure

\`\`\`
console/modes/<mode_name>/
├── mode.yaml
├── main.py
├── config.py
├── handlers/
├── schemas/
└── tests/
\`\`\`

## 4.2 Manifest Example

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

## 4.3 Input Schema Example

\`\`\`
class Input(BaseModel):
targets: List[str]
\`\`\`

## 4.4 Output Schema Example

\`\`\`
class Output(BaseModel):
raw_responses: Dict[str, str]
anomalies: List[str]
\`\`\`

## 4.5 Handler Responsibilities

- **preflight.py** — Validate inputs
- **executor.py** — Perform core logic
- **postprocess.py** — Normalize output

---

# 5. Operator Guide

## 5.1 Listing MODEs

\`\`\`
console modes list
\`\`\`

## 5.2 Running a MODE

\`\`\`
console run ssrf_basic_scan --targets example.com
\`\`\`

## 5.3 Run Directory Structure

\`\`\`
runs/<timestamp>\_<mode_name>/
├── input.json
├── output.json
├── anomalies.json
├── artifacts/
└── logs/
\`\`\`

## 5.4 Dashboard

\`\`\`
python -m dashboard
\`\`\`

Panels include:

- Run history
- Anomalies
- Artifacts
- Logs
- Diff viewer

---

# 6. API Reference

## 6.1 Base URL

\`\`\`
http://localhost:5000
\`\`\`

## 6.2 Key Endpoints

### List MODEs

\`\`\`
GET /modes
\`\`\`

### Run a MODE

\`\`\`
POST /modes/<mode_name>/run
\`\`\`

### Get run output

\`\`\`
GET /runs/<run_id>/output
\`\`\`

### Get artifacts

\`\`\`
GET /runs/<run_id>/artifacts
\`\`\`

### Diff

\`\`\`
POST /diff
\`\`\`

---

# 7. Security Model

## 7.1 Principles

- Least privilege
- Deterministic execution
- MODE isolation
- Immutable artifacts
- Transparent logging

## 7.2 Trust Boundaries

\`\`\`
Operator → API → MODE Engine → Filesystem
\`\`\`

## 7.3 MODE Isolation Rules

MODEs cannot:

- Access other MODEs
- Write outside run directories
- Read environment variables
- Spawn subprocesses
- Import arbitrary modules

---

# 8. Configuration Reference

## 8.1 Global Config (config.yaml)

\`\`\`
backend:
port: 5000
dashboard:
port: 5001
storage:
runs_dir: runs/
\`\`\`

## 8.2 Environment Variables

| Variable             | Description             |
| -------------------- | ----------------------- |
| SSRFC_BACKEND_PORT   | Override backend port   |
| SSRFC_DASHBOARD_PORT | Override dashboard port |
| LOG_LEVEL            | Logging level           |

## 8.3 Configuration Precedence

1. MODE defaults
2. MODE manifest
3. Global config
4. Environment variables
5. CLI overrides
6. API overrides

---

# 9. Testing Guide

## 9.1 Test Categories

- Unit tests
- Integration tests
- Schema tests
- Snapshot regression tests

## 9.2 Running Tests

\`\`\`
pytest -q
pytest --cov=console
\`\`\`

## 9.3 Coverage Requirement

Minimum **85%** for new code.

---

# 10. Deployment Guide

## 10.1 systemd Services

Backend:

\`\`\`
ExecStart=/usr/bin/python3 -m console.api
\`\`\`

Dashboard:

\`\`\`
ExecStart=/usr/bin/python3 -m dashboard
\`\`\`

## 10.2 Install Services

\`\`\`
sudo systemctl enable ssrf-backend
sudo systemctl enable ssrf-dashboard
\`\`\`

---

# 11. Service Hardening

## 11.1 systemd Hardening Options

\`\`\`
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true
MemoryDenyWriteExecute=true
\`\`\`

## 11.2 Filesystem Hardening

\`\`\`
sudo chattr +i runs/
sudo chattr +i snapshots/
\`\`\`

## 11.3 Network Hardening

Bind to localhost:

\`\`\`
SSRFC_BACKEND_BIND=127.0.0.1
\`\`\`

---

# 12. MODE Catalog

## 12.1 ssrf_basic_scan

- Basic SSRF detection
- HTTP request execution
- Raw response capture
- Anomaly detection

Manifest:

\`\`\`
name: ssrf_basic_scan
version: 1.0.0
\`\`\`

---

# 13. FAQ

## Common Questions

### “Where do run results go?”

\`\`\`
runs/<run_id>/
\`\`\`

### “How do I diff two runs?”

\`\`\`
console diff <run1> <run2>
\`\`\`

### “Is the dashboard read‑only?”

Yes — always.

---

# 14. Roadmap

## Near‑Term

- RBAC
- MODE SDK improvements
- Dashboard enhancements

## Mid‑Term

- Distributed execution
- Plugin marketplace
- Advanced anomaly detection

## Long‑Term

- Full web console
- Multi‑tenant model
- Execution sandbox

---

# Conclusion

This manual consolidates the entire SSRF Command Console documentation suite into a single, authoritative reference.
It is designed for operators, developers, MODE authors, and administrators who require clarity, determinism, and professional‑grade documentation.
