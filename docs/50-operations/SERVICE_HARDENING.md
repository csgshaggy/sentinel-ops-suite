# Service Hardening Guide

## Overview

This guide provides a comprehensive hardening strategy for deploying the SSRF Command Console in production environments.
It focuses on reducing attack surface, enforcing isolation, securing the filesystem, and ensuring deterministic, observable service behavior.

This document complements `SERVICE_DEPLOYMENT.md` by adding security‑focused controls.

---

# 1. Hardening Goals

The hardening model is built around:

- **Isolation** — services run with minimal privileges
- **Integrity** — code, artifacts, and logs cannot be tampered with
- **Determinism** — services behave predictably under all conditions
- **Observability** — all actions are logged and auditable
- **Resilience** — services restart safely and consistently

---

# 2. System User Hardening

Create a dedicated system user:

\`\`\`
sudo useradd --system --no-create-home --shell /usr/sbin/nologin ssrf
\`\`\`

### User Restrictions

- No login shell
- No home directory
- No sudo privileges
- No access outside `/opt/ssrf-console` and `/var/log/ssrf`

### Directory Ownership

\`\`\`
sudo chown -R ssrf:ssrf /opt/ssrf-console
sudo chown -R ssrf:ssrf /var/log/ssrf
\`\`\`

---

# 3. Filesystem Hardening

### Recommended Directory Permissions

| Directory           | Permissions | Owner     | Notes                |
| ------------------- | ----------- | --------- | -------------------- |
| `/opt/ssrf-console` | 750         | ssrf:ssrf | Code + MODEs         |
| `/var/log/ssrf`     | 750         | ssrf:ssrf | Logs                 |
| `runs/`             | 750         | ssrf:ssrf | Immutable run output |
| `snapshots/`        | 750         | ssrf:ssrf | Immutable snapshots  |

### Immutability Enforcement

Use `chattr` to protect run directories:

\`\`\`
sudo chattr +i runs/
sudo chattr +i snapshots/
\`\`\`

This prevents accidental or malicious modification.

---

# 4. systemd Hardening Options

Add these to both backend and dashboard services for maximum isolation:

\`\`\`
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true
PrivateDevices=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictSUIDSGID=true
LockPersonality=true
MemoryDenyWriteExecute=true
\`\`\`

### Explanation of Key Directives

- **ProtectSystem=full** — root filesystem becomes read‑only
- **PrivateTmp=true** — isolates `/tmp`
- **NoNewPrivileges=true** — prevents privilege escalation
- **MemoryDenyWriteExecute=true** — blocks W+X memory regions
- **PrivateDevices=true** — hides `/dev` except essentials

These dramatically reduce attack surface.

---

# 5. Network Hardening

### Restrict Listening Interfaces

In `ssrf.env`:

\`\`\`
SSRFC_BACKEND_BIND=127.0.0.1
SSRFC_DASHBOARD_BIND=127.0.0.1
\`\`\`

### Use a Reverse Proxy

Terminate TLS at:

- Nginx
- Caddy
- Traefik

### Firewall Rules (UFW Example)

\`\`\`
sudo ufw allow 443/tcp
sudo ufw allow from 127.0.0.1 to any port 5000
sudo ufw allow from 127.0.0.1 to any port 5001
sudo ufw deny 5000
sudo ufw deny 5001
\`\`\`

---

# 6. Python Environment Hardening

### Use a dedicated virtual environment

\`\`\`
/opt/ssrf-console/venv/bin/python3 -m console.api
\`\`\`

### Freeze dependencies

\`\`\`
pip freeze > requirements.lock
\`\`\`

### Disable pip installation at runtime

Remove write permissions from:

\`\`\`
/opt/ssrf-console/venv/lib/python3.x/site-packages
\`\`\`

---

# 7. Logging Hardening

### Log Directory Permissions

\`\`\`
sudo chmod 750 /var/log/ssrf
sudo chown ssrf:ssrf /var/log/ssrf
\`\`\`

### Log Rotation

Add `/etc/logrotate.d/ssrf`:

\`\`\`
/var/log/ssrf/\*.log {
daily
rotate 14
compress
missingok
notifempty
copytruncate
}
\`\`\`

### Audit Logging

Enable journald persistence:

\`\`\`
sudo mkdir -p /var/log/journal
sudo systemctl restart systemd-journald
\`\`\`

---

# 8. API Hardening

### Disable unauthenticated access

In `config.yaml`:

\`\`\`
security:
allow_unauthenticated: false
\`\`\`

### Enforce token authentication

- Use long, random tokens
- Store tokens outside repo
- Rotate tokens regularly

### Rate Limiting (via reverse proxy)

Example (Nginx):

\`\`\`
limit_req_zone $binary_remote_addr zone=api:10m rate=5r/s;
\`\`\`

---

# 9. Dashboard Hardening

The dashboard must remain **read‑only**.

Enforce:

\`\`\`
dashboard:
read_only: true
\`\`\`

### Disable file downloads if required

Add a proxy rule to block:

- `/artifacts/*`
- `/logs/*`

---

# 10. MODE Hardening

### MODEs must not:

- Spawn subprocesses
- Access environment variables
- Write outside run directories
- Import arbitrary modules
- Access other MODEs
- Perform network operations unless declared

### Enforce capability checks

MODE manifest:

\`\`\`
requires:

- network
- http
  \`\`\`

The engine must reject undeclared capabilities.

---

# 11. Snapshot & Diff Hardening

Snapshots must be:

- Immutable
- Signed (optional future feature)
- Stored in restricted directories

### Protect snapshots

\`\`\`
sudo chattr +i snapshots/
\`\`\`

---

# 12. Reverse Proxy Hardening

### TLS Configuration (Nginx Example)

\`\`\`
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
ssl_prefer_server_ciphers on;
\`\`\`

### Security Headers

\`\`\`
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Referrer-Policy strict-origin;
\`\`\`

---

# 13. Monitoring & Health Checks

### systemd Watchdog

\`\`\`
WatchdogSec=10
\`\`\`

### External Monitoring

- Prometheus exporters
- UptimeRobot
- Grafana dashboards

---

# 14. Backup Strategy

### Backup Directories

- `runs/`
- `snapshots/`
- `config.yaml`
- `mode.yaml` files

### Recommended Backup Frequency

- Snapshots: daily
- Runs: hourly or per‑run
- Config: on change

---

# Conclusion

This hardening guide provides a complete, production‑grade security posture for the SSRF Command Console.
By applying these controls, operators ensure isolation, integrity, and resilience across all deployed services.
