# Configuration Examples

## Overview
This document provides practical, ready‑to‑use configuration examples for:

- Global configuration (`config.yaml`)
- MODE configuration (`mode.yaml` + `config.py`)
- Environment variables (`ssrf.env`)
- CLI overrides
- API overrides
- Dashboard configuration
- Deployment configuration

These examples are designed to be deterministic, minimal, and production‑safe.

---

# 1. Global Configuration Examples (config.yaml)

## 1.1 Minimal Configuration

\`\`\`
backend:
  port: 5000

dashboard:
  port: 5001

storage:
  runs_dir: runs/
  snapshots_dir: snapshots/

security:
  allow_unauthenticated: true
\`\`\`

---

## 1.2 Production Configuration

\`\`\`
backend:
  port: 5000
  log_level: info
  bind: 127.0.0.1

dashboard:
  port: 5001
  bind: 127.0.0.1
  read_only: true

storage:
  runs_dir: /var/ssrf/runs/
  snapshots_dir: /var/ssrf/snapshots/

security:
  allow_unauthenticated: false
\`\`\`

---

## 1.3 Debug Configuration

\`\`\`
backend:
  port: 5000
  log_level: debug

dashboard:
  port: 5001

security:
  allow_unauthenticated: true
\`\`\`

---

# 2. MODE Configuration Examples

## 2.1 Example mode.yaml

\`\`\`
name: ssrf_basic_scan
version: 1.0.0
entrypoint: main:run
summary: Basic SSRF scanning routine
requires:
  - network
  - http
config:
  timeout: 5
  retries: 2
  max_redirects: 3
outputs:
  - raw_responses
  - anomalies
\`\`\`

---

## 2.2 Example config.py

\`\`\`
DEFAULT_CONFIG = {
    "timeout": 5,
    "retries": 2,
    "max_redirects": 3,
    "user_agent": "SSRF-Console/1.0"
}
\`\`\`

---

# 3. Environment Variable Examples (ssrf.env)

## 3.1 Minimal

\`\`\`
PYTHONPATH=/opt/ssrf-console
LOG_LEVEL=info
\`\`\`

---

## 3.2 Backend + Dashboard Binding

\`\`\`
PYTHONPATH=/opt/ssrf-console
SSRFC_BACKEND_PORT=5000
SSRFC_BACKEND_BIND=127.0.0.1
SSRFC_DASHBOARD_PORT=5001
SSRFC_DASHBOARD_BIND=127.0.0.1
LOG_LEVEL=info
\`\`\`

---

## 3.3 Debug Mode

\`\`\`
LOG_LEVEL=debug
\`\`\`

---

# 4. CLI Override Examples

## 4.1 Override timeout

\`\`\`
console run ssrf_basic_scan --timeout 10
\`\`\`

## 4.2 Override multiple values

\`\`\`
console run ssrf_basic_scan --timeout 10 --retries 5 --max_redirects 1
\`\`\`

## 4.3 Override targets

\`\`\`
console run ssrf_basic_scan --targets example.com,internal.local
\`\`\`

---

# 5. API Override Examples

## 5.1 Basic Run

\`\`\`
POST /modes/ssrf_basic_scan/run
{
  "targets": ["example.com"]
}
\`\`\`

---

## 5.2 Run with Overrides

\`\`\`
POST /modes/ssrf_basic_scan/run
{
  "targets": ["example.com"],
  "config": {
    "timeout": 10,
    "retries": 4
  }
}
\`\`\`

---

## 5.3 Multi‑Target Run

\`\`\`
POST /modes/ssrf_basic_scan/run
{
  "targets": [
    "example.com",
    "10.0.0.5",
    "metadata.google.internal"
  ]
}
\`\`\`

---

# 6. Dashboard Configuration Examples

## 6.1 Default

\`\`\`
dashboard:
  port: 5001
  read_only: true
\`\`\`

---

## 6.2 Custom Theme (future feature)

\`\`\`
dashboard:
  port: 5001
  theme: dark
  read_only: true
\`\`\`

---

# 7. Deployment Configuration Examples

## 7.1 systemd Backend Service

\`\`\`
[Service]
Type=simple
EnvironmentFile=/etc/ssrf/ssrf.env
WorkingDirectory=/opt/ssrf-console
ExecStart=/usr/bin/python3 -m console.api
Restart=always
User=ssrf
Group=ssrf
\`\`\`

---

## 7.2 systemd Dashboard Service

\`\`\`
[Service]
Type=simple
EnvironmentFile=/etc/ssrf/ssrf.env
WorkingDirectory=/opt/ssrf-console
ExecStart=/usr/bin/python3 -m dashboard
Restart=always
User=ssrf
Group=ssrf
\`\`\`

---

## 7.3 Reverse Proxy (Nginx)

\`\`\`
location /api/ {
    proxy_pass http://127.0.0.1:5000/;
}

location /dashboard/ {
    proxy_pass http://127.0.0.1:5001/;
}
\`\`\`

---

# 8. Snapshot & Diff Examples

## 8.1 Create Snapshot

\`\`\`
console snapshot create 2026-03-17_120001_ssrf_basic_scan
\`\`\`

## 8.2 Diff Two Runs

\`\`\`
console diff runA runB
\`\`\`

---

# 9. Example Full Workflow

## 9.1 Run a MODE

\`\`\`
console run ssrf_basic_scan --targets example.com
\`\`\`

## 9.2 Open Dashboard

\`\`\`
python -m dashboard
\`\`\`

## 9.3 Create Snapshot

\`\`\`
console snapshot create <run_id>
\`\`\`

## 9.4 Compare Runs

\`\`\`
console diff <old_run> <new_run>
\`\`\`

---

# Conclusion

These examples provide a practical reference for configuring the SSRF Command Console across development, testing, and production environments.  
Use them as templates for your own deployments and workflows.
