# Architecture Overview

## Purpose
This document provides a high-level architectural overview of the SSRF Command Console.

---

# 1. System Architecture Summary

The system is composed of four major subsystems:

1. **Backend Core**  
2. **MODE Ecosystem**  
3. **Dashboard**  
4. **Services Layer**

Each subsystem is isolated, deterministic, and designed for forensic clarity.

---

# 2. Component Diagram

\`\`\`
Dashboard → Backend API → MODE Engine → Runs Directory
\`\`\`

This represents the primary data and control flow through the system.

---

# 3. Backend Architecture

The backend is responsible for:

- MODE execution  
- Logging  
- Artifact management  
- Snapshot creation  
- Diffing  
- API exposure  

It is intentionally stateless and relies entirely on the filesystem for persistence.

---

# 4. MODE Engine Architecture

The MODE engine enforces a strict, deterministic lifecycle:

\`\`\`
Load → Preflight → Execute → Postprocess → Emit
\`\`\`

### MODE Directory Structure

\`\`\`
<mode_name>/
├── mode.yaml
├── main.py
├── config.py
├── handlers/
└── schemas/
\`\`\`

### Lifecycle Responsibilities

- **Load** — Parse manifest, load config, import code  
- **Preflight** — Validate inputs, overrides, environment  
- **Execute** — Perform core logic  
- **Postprocess** — Normalize output, detect anomalies  
- **Emit** — Write artifacts, logs, structured output  

---

# 5. Dashboard Architecture

The dashboard provides:

- Run history  
- Run summaries  
- Anomaly visualization  
- Artifact browsing  
- Log viewing  
- Diff viewer  

It reads from the filesystem and never mutates data.

---

# 6. Data Flow

\`\`\`
Operator → MODE Engine → Artifacts → Dashboard → Operator
\`\`\`

This loop ensures transparency and reproducibility.

---

# 7. Storage Architecture

Each run is stored in an immutable directory:

\`\`\`
runs/<timestamp>_<mode_name>/
├── input.json
├── output.json
├── anomalies.json
├── artifacts/
└── logs/
\`\`\`

### Storage Guarantees

- Write-once  
- Immutable  
- Deterministic  
- Human-readable  

---

# 8. Logging & Observability

Logs include:

- Timestamp  
- Event  
- Target  
- Duration  
- Correlation ID  

Logs are stored per run:

\`\`\`
runs/<run_id>/logs/execution.log
\`\`\`

---

# 9. API Layer

The API exposes:

- MODE execution  
- Run retrieval  
- Artifact access  
- Snapshot creation  
- Diffing  

It is built on FastAPI and uses Pydantic for validation.

---

# 10. Extensibility Model

The system supports:

- New MODEs  
- New dashboard panels  
- New API endpoints  
- New services  

Extensibility is achieved through strict boundaries and deterministic behavior.

---

# 11. Security Considerations

Security is enforced through:

- Input validation  
- MODE isolation  
- Filesystem restrictions  
- Authentication (optional)  
- No cross-MODE access  
- No environment variable access inside MODEs  

The architecture prioritizes safety, determinism, and forensic clarity.
