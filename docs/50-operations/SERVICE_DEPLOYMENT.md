# Service Deployment Guide

## Overview

This guide explains how to deploy the SSRF Command Console backend, dashboard, and supporting components as system services.
It covers systemd service files, environment configuration, logging, lifecycle management, and production‑grade hardening.

The goal: **reliable, restart‑on‑failure, operator‑grade services**.

---

# 1. Deployment Models

The console supports three deployment models:

### **1. Single‑Service Deployment**

- One service runs the backend API + MODE engine
- Dashboard launched manually

### **2. Dual‑Service Deployment**

- Backend API service
- Dashboard service

### **3. Full Multi‑Service Deployment**

- Backend API
- Dashboard
- Worker / scheduler (optional future component)
- Health‑check service
- Watchdog service

This guide covers the **dual‑service** model, which is the recommended baseline.

---

# 2. Directory Layout for Services

Your project should include:

\`\`\`
systemd/
├── ssrf-backend.service
├── ssrf-dashboard.service
├── ssrf.env
└── install_services.sh
\`\`\`

### **ssrf.env**

Stores environment variables shared by all services.

### **install_services.sh**

Copies service files into `/etc/systemd/system/` and reloads systemd.

---

# 3. Environment File (ssrf.env)

Example:

\`\`\`
PYTHONPATH=/opt/ssrf-console
SSRFC_BACKEND_PORT=5000
SSRFC_DASHBOARD_PORT=5001
LOG_LEVEL=info
\`\`\`

Rules:

- Never store secrets here
- Keep values minimal
- Use absolute paths for production

---

# 4. Backend Service (ssrf-backend.service)

\`\`\`
[Unit]
Description=SSRF Console Backend Service
After=network.target

[Service]
Type=simple
EnvironmentFile=/etc/ssrf/ssrf.env
WorkingDirectory=/opt/ssrf-console
ExecStart=/usr/bin/python3 -m console.api
Restart=always
RestartSec=3
User=ssrf
Group=ssrf

[Install]
WantedBy=multi-user.target
\`\`\`

### Key Features

- **Restart on failure**
- **Dedicated user**
- **Environment isolation**
- **Clean working directory**

---

# 5. Dashboard Service (ssrf-dashboard.service)

\`\`\`
[Unit]
Description=SSRF Console Dashboard Service
After=network.target ssrf-backend.service

[Service]
Type=simple
EnvironmentFile=/etc/ssrf/ssrf.env
WorkingDirectory=/opt/ssrf-console
ExecStart=/usr/bin/python3 -m dashboard
Restart=always
RestartSec=3
User=ssrf
Group=ssrf

[Install]
WantedBy=multi-user.target
\`\`\`

---

# 6. Installation Script (install_services.sh)

\`\`\`
#!/bin/bash

set -e

mkdir -p /etc/ssrf
cp ssrf.env /etc/ssrf/ssrf.env

cp ssrf-backend.service /etc/systemd/system/
cp ssrf-dashboard.service /etc/systemd/system/

systemctl daemon-reload
systemctl enable ssrf-backend.service
systemctl enable ssrf-dashboard.service

echo "Services installed. Start them with:"
echo " systemctl start ssrf-backend"
echo " systemctl start ssrf-dashboard"
\`\`\`

---

# 7. Creating the SSRF User

\`\`\`
sudo useradd --system --no-create-home --shell /usr/sbin/nologin ssrf
\`\`\`

This user owns:

- `/opt/ssrf-console`
- `/var/log/ssrf/` (if used)

---

# 8. Deploying the Application

### **1. Copy project to /opt**

\`\`\`
sudo mkdir -p /opt/ssrf-console
sudo cp -r \* /opt/ssrf-console/
sudo chown -R ssrf:ssrf /opt/ssrf-console
\`\`\`

### **2. Install services**

\`\`\`
cd systemd/
sudo ./install_services.sh
\`\`\`

### **3. Start services**

\`\`\`
sudo systemctl start ssrf-backend
sudo systemctl start ssrf-dashboard
\`\`\`

---

# 9. Service Management

### Check status

\`\`\`
systemctl status ssrf-backend
systemctl status ssrf-dashboard
\`\`\`

### View logs

\`\`\`
journalctl -u ssrf-backend -f
journalctl -u ssrf-dashboard -f
\`\`\`

### Restart services

\`\`\`
systemctl restart ssrf-backend
systemctl restart ssrf-dashboard
\`\`\`

---

# 10. Production Hardening

### **1. Use a dedicated virtual environment**

\`\`\`
/opt/ssrf-console/venv/bin/python3 -m console.api
\`\`\`

### **2. Restrict filesystem permissions**

- MODEs must not write outside run directories
- Services must not run as root

### **3. Enable systemd sandboxing (optional)**

\`\`\`
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
\`\`\`

### **4. Use a reverse proxy (optional)**

- Nginx
- Caddy
- Traefik

### **5. Enable HTTPS**

Terminate TLS at the proxy.

---

# 11. Health Checks (Optional)

You may add:

- `/health` endpoint
- systemd watchdog
- periodic curl checks

Example systemd watchdog:

\`\`\`
WatchdogSec=10
\`\`\`

---

# 12. Uninstalling Services

\`\`\`
sudo systemctl stop ssrf-backend ssrf-dashboard
sudo systemctl disable ssrf-backend ssrf-dashboard
sudo rm /etc/systemd/system/ssrf-backend.service
sudo rm /etc/systemd/system/ssrf-dashboard.service
sudo systemctl daemon-reload
\`\`\`

---

# Conclusion

This guide provides a complete, production‑ready deployment model for the SSRF Command Console using systemd.
Following these steps ensures reliable, restart‑on‑failure operation with clean isolation and operator‑grade observability.
