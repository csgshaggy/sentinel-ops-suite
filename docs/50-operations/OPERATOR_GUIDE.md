# Operator Guide

## Overview

This guide explains how operators and analysts use the SSRF Command Console to run MODEs, analyze results, and navigate the dashboard.
It focuses on practical workflows, deterministic execution, and artifact‑driven analysis.

---

# 1. Running MODEs

### List all MODEs

\`\`\`
console modes list
\`\`\`

### Run a MODE

\`\`\`
console run ssrf_basic_scan --targets example.com
\`\`\`

### Override configuration values

\`\`\`
console run ssrf_basic_scan --timeout 10
\`\`\`

Overrides are validated during **preflight**.

---

# 2. Understanding Run Output

Each run creates an immutable directory:

\`\`\`
runs/<timestamp>\_<mode_name>/
├── input.json
├── output.json
├── anomalies.json
├── artifacts/
└── logs/
\`\`\`

### Key Files

| File               | Purpose                     |
| ------------------ | --------------------------- |
| **input.json**     | Inputs used for the run     |
| **output.json**    | Final structured output     |
| **anomalies.json** | Detected anomalies          |
| **artifacts/**     | Raw and processed artifacts |
| **logs/**          | Execution logs              |

### Immutability Rules

- Runs cannot be modified after creation
- Artifacts are write‑once
- Logs are append‑only

This ensures forensic clarity and reproducibility.

---

# 3. Dashboard Usage

Start the dashboard:

\`\`\`
python -m dashboard
\`\`\`

### Dashboard Panels

- **Run History** — list of all runs
- **Run Summary** — high‑level overview
- **Anomalies** — severity, evidence, affected targets
- **Artifacts** — raw and processed outputs
- **Logs** — structured execution logs
- **Diff Viewer** — compare runs or snapshots

The dashboard is read‑only and safe for analysts.

---

# 4. Snapshots & Diffs

Snapshots allow long‑term comparison and regression detection.

### Create a snapshot

\`\`\`
console snapshot create <run_id>
\`\`\`

### Diff two runs

\`\`\`
console diff <run_id_1> <run_id_2>
\`\`\`

### Diff Use Cases

- Detect regressions
- Compare environments
- Track changes over time
- Identify drift in anomalies or artifacts

---

# 5. Troubleshooting

### MODE fails during preflight

Check:

\`\`\`
runs/<run_id>/logs/execution.log
\`\`\`

Common causes:

- Invalid targets
- Invalid overrides
- Missing configuration

---

### Dashboard not loading

Check:

- Port conflicts
- Missing dependencies
- Service logs (if running as systemd service)

---

### MODE not detected

Ensure the directory exists:

\`\`\`
console/modes/<mode_name>/mode.yaml
\`\`\`

And validate:

\`\`\`
console modes validate <mode_name>
\`\`\`

---

# 6. Operator Best Practices

- Validate targets before running
- Use snapshots for long‑term comparisons
- Review anomalies before raw artifacts
- Keep run directories immutable
- Use dashboard for visual analysis
- Prefer structured output over raw logs
- Run MODEs with minimal overrides for reproducibility

---

# 7. Workflow Example

### Step 1 — Run a MODE

\`\`\`
console run ssrf_basic_scan --targets example.com
\`\`\`

### Step 2 — Open the dashboard

\`\`\`
python -m dashboard
\`\`\`

### Step 3 — Review anomalies

Look for:

- Unexpected redirects
- Internal IP exposure
- Protocol mismatches
- Timing anomalies

### Step 4 — Review artifacts

Artifacts may include:

- Raw HTTP responses
- Normalized summaries
- Extracted metadata

### Step 5 — Create a snapshot

\`\`\`
console snapshot create <run_id>
\`\`\`

### Step 6 — Compare with future runs

\`\`\`
console diff <old_run> <new_run>
\`\`\`

---

# Conclusion

Operators use the SSRF Command Console to run MODEs, analyze results, and maintain a deterministic, artifact‑driven workflow.
Following this guide ensures consistent, repeatable, and forensic‑grade operation across all environments.
