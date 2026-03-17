# Installation and Setup Guide

## Overview
This guide walks you through installing, configuring, and verifying the SSRF Command Console.

---

## System Requirements

### Supported OS
- Linux  
- macOS  
- Windows (native or WSL2)

### Required Software
- Python 3.10+  
- Git  
- pip or pipx  

---

## 1. Clone the Repository

\`\`\`
git clone https://github.com/<your-org>/ssrf-console.git
cd ssrf-console
\`\`\`

---

## 2. Create a Virtual Environment

### Linux/macOS

\`\`\`
python3 -m venv venv
source venv/bin/activate
\`\`\`

### Windows

\`\`\`
python -m venv venv
venv\\Scripts\\activate
\`\`\`

---

## 3. Install Dependencies

\`\`\`
pip install -r requirements.txt
\`\`\`

---

## 4. Initialize Directory Structure

\`\`\`
python scripts/init_structure.py
\`\`\`

This creates:

- `runs/`  
- Default MODEs  
- Dashboard scaffolding  

---

## 5. Configure Environment Variables

Create a `.env` file:

\`\`\`
CONSOLE_ENV=production
LOG_LEVEL=INFO
RUNS_DIR=./runs
\`\`\`

---

## 6. Start the Console

### CLI

\`\`\`
python -m console
\`\`\`

### Dashboard

\`\`\`
python -m dashboard
\`\`\`

### API

\`\`\`
uvicorn console.api:app --host 0.0.0.0 --port 5000
\`\`\`

---

## 7. Optional: Install as Services

\`\`\`
sudo cp services/dashboard.service /etc/systemd/system/
sudo systemctl enable dashboard.service
sudo systemctl start dashboard.service
\`\`\`

---

## 8. Verify Installation

\`\`\`
console --version
console run ssrf_basic_scan --targets example.com
\`\`\`
