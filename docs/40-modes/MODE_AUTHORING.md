# MODE Authoring Guide

## Overview

This guide explains how to build new MODEs for the SSRF Command Console.
MODEs are modular, deterministic, isolated execution units that follow a strict lifecycle and produce structured, reproducible artifacts.

---

# 1. MODE Structure

Each MODE lives in:

\`\`\`
console/modes/<mode_name>/
\`\`\`

### Required Files

\`\`\`
mode.yaml
main.py
config.py
handlers/
schemas/
tests/
\`\`\`

---

# 2. MODE Manifest (mode.yaml)

The manifest defines metadata, configuration, capabilities, and outputs.

### Example Manifest

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
  outputs:
- raw_responses
- anomalies
  \`\`\`

---

# 3. MODE Lifecycle

All MODEs follow the deterministic lifecycle:

\`\`\`
Load → Preflight → Execute → Postprocess → Emit
\`\`\`

### Lifecycle Responsibilities

- **Load** — Parse manifest, load config, import code
- **Preflight** — Validate inputs, overrides, environment
- **Execute** — Perform core logic
- **Postprocess** — Normalize output, detect anomalies
- **Emit** — Write artifacts, logs, structured output

This ensures reproducibility and forensic clarity.

---

# 4. Input Schema

Input schemas are defined using Pydantic in:

\`\`\`
schemas/input.py
\`\`\`

### Example

\`\`\`
class Input(BaseModel):
targets: List[str]
\`\`\`

---

# 5. Output Schema

Output schemas are defined in:

\`\`\`
schemas/output.py
\`\`\`

### Example

\`\`\`
class Output(BaseModel):
raw_responses: Dict[str, str]
anomalies: List[str]
\`\`\`

---

# 6. Handlers

Handlers implement each lifecycle stage and live in:

\`\`\`
handlers/
├── preflight.py
├── executor.py
└── postprocess.py
\`\`\`

Each handler exposes:

\`\`\`
def run(context):
...
\`\`\`

### Handler Responsibilities

- **preflight.py** — Validate inputs, environment, config
- **executor.py** — Perform core logic
- **postprocess.py** — Normalize output, detect anomalies

---

# 7. Logging

MODEs use structured logging via the execution context:

\`\`\`
context.log(event="request_sent", target=url, duration_ms=120)
\`\`\`

Logs are written to:

\`\`\`
runs/<run_id>/logs/execution.log
\`\`\`

---

# 8. Artifacts

Artifacts are written using:

\`\`\`
context.artifacts.write("raw/response_1.txt", data)
\`\`\`

### Artifact Rules

- Write-once
- Immutable
- Stored under the run directory
- Organized by category (raw, processed, etc.)

---

# 9. Testing

MODEs must include:

- Unit tests
- Integration tests
- Schema validation tests

Run tests with:

\`\`\`
pytest -q
\`\`\`

---

# 10. Validation

Validate a MODE before running it:

\`\`\`
console modes validate <mode_name>
\`\`\`

Validation checks:

- Manifest correctness
- Schema correctness
- Handler presence
- Entrypoint validity

---

# 11. Best Practices

- Keep logic deterministic
- Avoid external dependencies
- Avoid environment variables
- Avoid global state
- Keep handlers small and focused
- Use schemas for all structured data
- Write artifacts early and consistently
- Never read or write outside the run directory
- Never import from other MODEs

---

# 12. Example MODE Layout

\`\`\`
ssrf_basic_scan/
├── mode.yaml
├── main.py
├── config.py
├── handlers/
│ ├── preflight.py
│ ├── executor.py
│ └── postprocess.py
├── schemas/
│ ├── input.py
│ └── output.py
└── tests/
\`\`\`

---

# 13. Example Entrypoint (main.py)

\`\`\`
def run(context):
targets = context.input.targets
results = {}

    for t in targets:
        response = context.http.get(t)
        results[t] = response.text
        context.log(event="request_sent", target=t)

    return {
        "raw_responses": results,
        "anomalies": []
    }

\`\`\`

---

# Conclusion

MODEs are the core execution units of the SSRF Command Console.
By following this guide, you ensure your MODEs remain deterministic, isolated, testable, and fully compatible with the console’s lifecycle and dashboard.
