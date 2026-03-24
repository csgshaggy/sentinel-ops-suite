# Frequently Asked Questions (FAQ)

## Overview

This FAQ provides quick answers to common questions about installing, running, developing, and troubleshooting the SSRF Command Console.
It is intended for operators, analysts, and developers.

---

# 1. General Questions

### **What is the SSRF Command Console?**

A modular, deterministic framework for executing SSRF‑focused MODEs, generating structured artifacts, and analyzing results through a dashboard.

### **Who is it for?**

- Security researchers
- Operators
- Analysts
- Developers authoring custom MODEs

### **What makes it different?**

- Deterministic lifecycle
- Immutable run directories
- Structured artifacts
- Strong isolation
- Dashboard visualization
- Snapshot & diff engine

---

# 2. Installation & Setup

### **What are the system requirements?**

- Python 3.10+
- Git
- Linux, macOS, or Windows (native or WSL2)

### **How do I install it?**

Clone the repo, create a virtual environment, install dependencies:

\`\`\`
git clone https://github.com/<your-org>/ssrf-console.git
cd ssrf-console
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

### **How do I start the console?**

\`\`\`
python -m console
\`\`\`

### **How do I start the dashboard?**

\`\`\`
python -m dashboard
\`\`\`

---

# 3. Running MODEs

### **How do I list available MODEs?**

\`\`\`
console modes list
\`\`\`

### **How do I run a MODE?**

\`\`\`
console run ssrf_basic_scan --targets example.com
\`\`\`

### **Can I override configuration values?**

Yes:

\`\`\`
console run ssrf_basic_scan --timeout 10
\`\`\`

### **Where do run results go?**

\`\`\`
runs/<timestamp>\_<mode_name>/
\`\`\`

---

# 4. Understanding Output

### **What is inside a run directory?**

\`\`\`
input.json
output.json
anomalies.json
artifacts/
logs/
\`\`\`

### **Are run directories immutable?**

Yes — they cannot be modified after creation.

### **Where are logs stored?**

\`\`\`
runs/<run_id>/logs/execution.log
\`\`\`

---

# 5. Dashboard

### **What can I do in the dashboard?**

- View run history
- Inspect anomalies
- Browse artifacts
- View logs
- Compare runs

### **Is the dashboard read‑only?**

Yes — it never mutates data.

---

# 6. Snapshots & Diffs

### **What is a snapshot?**

A frozen copy of a run used for long‑term comparison.

### **How do I create a snapshot?**

\`\`\`
console snapshot create <run_id>
\`\`\`

### **How do I diff two runs?**

\`\`\`
console diff <run_id_1> <run_id_2>
\`\`\`

---

# 7. MODE Development

### **How do I create a new MODE?**

Create a directory:

\`\`\`
console/modes/<mode_name>/
\`\`\`

Add:

- mode.yaml
- main.py
- config.py
- handlers/
- schemas/
- tests/

### **How do I validate a MODE?**

\`\`\`
console modes validate <mode_name>
\`\`\`

### **Where can I learn more?**

See `MODE_AUTHORING.md`.

---

# 8. Troubleshooting

### **The console won’t start. What should I check?**

- Python version
- Virtual environment activation
- Missing dependencies

### **A MODE fails during preflight. Why?**

Common causes:

- Invalid targets
- Invalid overrides
- Missing configuration

### **Dashboard won’t load. What should I check?**

- Port conflicts
- Missing dependencies
- Service logs (if running as systemd service)

### **A MODE isn’t showing up. Why?**

Ensure:

\`\`\`
console/modes/<mode_name>/mode.yaml
\`\`\`

Then validate:

\`\`\`
console modes validate <mode_name>
\`\`\`

---

# 9. Security

### **Are MODEs isolated?**

Yes — MODEs cannot:

- Access other MODEs
- Modify global config
- Write outside run directories
- Read environment variables
- Spawn subprocesses

### **Does the dashboard modify data?**

No — it is strictly read‑only.

### **Are artifacts immutable?**

Yes — they are write‑once and never modified.

---

# 10. Contributing

### **How do I contribute?**

See `CONTRIBUTING.md`.

### **What standards must I follow?**

- Conventional Commits
- PEP 8
- Type hints
- Deterministic behavior
- Tests required for all changes

---

# Conclusion

This FAQ provides quick answers to common questions about the SSRF Command Console.
For deeper details, refer to the full documentation suite.
