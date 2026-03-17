# Quickstart Guide

## Overview
This quickstart provides the fastest path to installing, running, and using the SSRF Command Console.  
It is designed for new users, operators, and developers who want to get hands‑on immediately with minimal setup.

You will learn how to:

- Install the console  
- Run your first MODE  
- Explore run output  
- Use the dashboard  
- Perform snapshots and diffs  

---

# 1. Install the Console

## 1.1 Clone the Repository

\`\`\`
git clone https://github.com/<your-org>/ssrf-console.git
cd ssrf-console
\`\`\`

## 1.2 Create a Virtual Environment

\`\`\`
python -m venv venv
source venv/bin/activate
\`\`\`

## 1.3 Install Dependencies

\`\`\`
pip install -r requirements.txt
\`\`\`

---

# 2. Run Your First MODE

## 2.1 List Available MODEs

\`\`\`
console modes list
\`\`\`

## 2.2 Run a MODE

\`\`\`
console run ssrf_basic_scan --targets example.com
\`\`\`

## 2.3 Override Configuration (Optional)

\`\`\`
console run ssrf_basic_scan --targets example.com --timeout 10
\`\`\`

---

# 3. Explore Run Output

Each run creates a directory:

\`\`\`
runs/<timestamp>_<mode_name>/
\`\`\`

Inside:

\`\`\`
input.json
output.json
anomalies.json
artifacts/
logs/
\`\`\`

### Key Files

- **input.json** — What was executed  
- **output.json** — Final structured output  
- **anomalies.json** — Detected anomalies  
- **artifacts/** — Raw and processed data  
- **logs/** — Execution logs  

---

# 4. Use the Dashboard

## 4.1 Start the Dashboard

\`\`\`
python -m dashboard
\`\`\`

## 4.2 Open in Browser

\`\`\`
http://localhost:5001
\`\`\`

### Dashboard Features

- Run history  
- Artifact viewer  
- Anomaly viewer  
- Log viewer  
- Diff viewer  

---

# 5. Create Snapshots

Snapshots preserve run output for long‑term comparison.

\`\`\`
console snapshot create <run_id>
\`\`\`

Snapshots are stored in:

\`\`\`
snapshots/
\`\`\`

---

# 6. Diff Two Runs

Compare two runs or snapshots:

\`\`\`
console diff <run1> <run2>
\`\`\`

Use cases:

- Detect drift  
- Validate changes  
- Compare environments  

---

# 7. Common Commands

| Task | Command |
|------|---------|
| List MODEs | `console modes list` |
| Run a MODE | `console run <mode>` |
| Override config | `console run <mode> --key value` |
| Start dashboard | `python -m dashboard` |
| Create snapshot | `console snapshot create <run_id>` |
| Diff runs | `console diff <run1> <run2>` |

---

# 8. Troubleshooting

### MODE not found
- Check `console/modes/`  
- Validate with:  
  \`\`\`
  console modes validate <mode_name>
  \`\`\`

### Dashboard not loading
- Check port conflicts  
- Ensure dependencies installed  

### Run directory missing
- Ensure MODE executed successfully  
- Check logs in `runs/<run_id>/logs/`  

---

# 9. Next Steps

After completing this quickstart, explore:

- `OPERATOR_GUIDE.md`  
- `MODE_AUTHORING.md`  
- `API_REFERENCE.md`  
- `SERVICE_DEPLOYMENT.md`  
- `TESTING_GUIDE.md`  

---

# Conclusion

You are now ready to run MODEs, explore artifacts, use the dashboard, and perform snapshot/diff analysis.  
This quickstart gives you everything needed to begin using the SSRF Command Console effectively.
