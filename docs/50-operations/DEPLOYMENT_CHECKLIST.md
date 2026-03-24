# Deployment Checklist

## Overview

This checklist provides a step‑by‑step, operator‑grade verification workflow for deploying the SSRF Command Console in any environment.
It ensures correctness, security, reproducibility, and service reliability.

Use this checklist during:

- First‑time deployments
- Server rebuilds
- Environment migrations
- Production rollouts

---

# 1. Pre‑Deployment Validation

### System Requirements

- [ ] Python 3.10+ installed
- [ ] Git installed
- [ ] Systemd available (Linux)
- [ ] 2 GB RAM minimum
- [ ] 1 GB free disk space

### User & Permissions

- [ ] Dedicated `ssrf` system user created
- [ ] No login shell assigned
- [ ] No sudo privileges
- [ ] Ownership of `/opt/ssrf-console` assigned to `ssrf:ssrf`
- [ ] Ownership of `/var/log/ssrf` assigned to `ssrf:ssrf`

---

# 2. Application Deployment

### Code Installation

- [ ] Repository cloned or copied to `/opt/ssrf-console`
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Permissions set to `750` for all directories
- [ ] `requirements.lock` generated (optional)

### Directory Structure

- [ ] `runs/` directory exists
- [ ] `snapshots/` directory exists
- [ ] `console/modes/` contains MODEs
- [ ] `config.yaml` present and valid

---

# 3. Configuration Validation

### Global Config

- [ ] `backend.port` set correctly
- [ ] `dashboard.port` set correctly
- [ ] `storage.runs_dir` correct
- [ ] `security.allow_unauthenticated` set appropriately

### Environment Variables

- [ ] `ssrf.env` created
- [ ] Backend bind address correct
- [ ] Dashboard bind address correct
- [ ] Logging level set

### MODE Validation

- [ ] All MODEs pass `console modes validate`
- [ ] All MODE manifests valid
- [ ] All MODE schemas load correctly

---

# 4. Service Deployment

### systemd Files

- [ ] `ssrf-backend.service` installed
- [ ] `ssrf-dashboard.service` installed
- [ ] `ssrf.env` copied to `/etc/ssrf/`
- [ ] `systemctl daemon-reload` executed

### Service Enablement

- [ ] Backend enabled
- [ ] Dashboard enabled

### Service Startup

- [ ] Backend started successfully
- [ ] Dashboard started successfully
- [ ] No errors in `journalctl -u ssrf-backend`
- [ ] No errors in `journalctl -u ssrf-dashboard`

---

# 5. Hardening Checklist

### systemd Hardening

- [ ] `ProtectSystem=full` enabled
- [ ] `ProtectHome=true` enabled
- [ ] `NoNewPrivileges=true` enabled
- [ ] `PrivateTmp=true` enabled
- [ ] `MemoryDenyWriteExecute=true` enabled

### Filesystem Hardening

- [ ] `runs/` marked immutable (optional)
- [ ] `snapshots/` marked immutable (optional)
- [ ] `/opt/ssrf-console` permissions correct
- [ ] `/var/log/ssrf` permissions correct

### Network Hardening

- [ ] Backend bound to localhost
- [ ] Dashboard bound to localhost
- [ ] Reverse proxy configured (optional)
- [ ] TLS enabled (optional)
- [ ] Firewall rules applied

---

# 6. Functional Verification

### Backend API

- [ ] `/modes` endpoint returns list
- [ ] `/health` endpoint returns OK (if enabled)
- [ ] MODE execution works via API

### CLI

- [ ] `console modes list` works
- [ ] `console run <mode>` works
- [ ] Artifacts generated correctly

### Dashboard

- [ ] Dashboard loads
- [ ] Run history visible
- [ ] Artifacts viewable
- [ ] Logs viewable
- [ ] Diff viewer functional

---

# 7. Snapshot & Diff Verification

### Snapshot

- [ ] Snapshot creation works
- [ ] Snapshot stored in correct directory

### Diff

- [ ] Diff between two runs works
- [ ] Diff output deterministic

---

# 8. Logging & Monitoring

### Logging

- [ ] Backend logs writing to `/var/log/ssrf`
- [ ] Dashboard logs writing to `/var/log/ssrf`
- [ ] Log rotation configured

### Monitoring (Optional)

- [ ] systemd watchdog enabled
- [ ] External uptime monitoring configured
- [ ] Reverse proxy access logs enabled

---

# 9. Backup Checklist

### Backup Targets

- [ ] `runs/`
- [ ] `snapshots/`
- [ ] `config.yaml`
- [ ] MODE directories
- [ ] systemd service files

### Backup Frequency

- [ ] Snapshots daily
- [ ] Runs hourly or per‑run
- [ ] Config on change

---

# 10. Final Deployment Sign‑Off

- [ ] All services running
- [ ] All MODEs validated
- [ ] Dashboard operational
- [ ] Hardening applied
- [ ] Backups configured
- [ ] Monitoring active
- [ ] Documentation updated

---

# Conclusion

This checklist ensures a complete, secure, and deterministic deployment of the SSRF Command Console.
Use it for every installation, rebuild, or migration to guarantee operational consistency and forensic‑grade reliability.
