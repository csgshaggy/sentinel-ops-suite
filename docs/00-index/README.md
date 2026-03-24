# SSRF Command Console

## Overview

The SSRF Command Console is a modular, operator‑grade framework for executing SSRF and network‑focused MODEs with deterministic behavior, structured artifacts, and a dashboard for analysis.

It is designed for:

- Security researchers
- Operators
- Analysts
- Developers building custom MODEs

The system emphasizes:

- Deterministic execution
- Strong isolation
- Structured outputs
- Forensic clarity
- Extensibility

---

## Features

- Modular MODE architecture
- Deterministic lifecycle (Preflight → Execute → Postprocess → Emit)
- Structured run directories
- Dashboard for visualization
- Snapshot & diff engine
- API for automation
- Strong security model
- Operator‑friendly CLI

---

## Quickstart

\`\`\`
git clone https://github.com/<your-org>/ssrf-console.git
cd ssrf-console
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m console
\`\`\`

---

## Documentation

See `DOCS_INDEX.md` for the full documentation suite.
