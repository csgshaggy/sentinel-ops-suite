# Developer Guide

## Overview
This guide explains the internal architecture and development workflows for contributors and maintainers of the SSRF Command Console.

---

# 1. Project Structure

\`\`\`
console/
├── api/
├── core/
├── modes/
├── dashboard/
├── services/
└── runs/
\`\`\`

Each directory has a clear responsibility:

- **api/** — FastAPI endpoints  
- **core/** — MODE engine, logging, artifacts, lifecycle  
- **modes/** — Built‑in and user‑authored MODEs  
- **dashboard/** — UI for run browsing and analysis  
- **services/** — Optional systemd services  
- **runs/** — Immutable run output directories  

---

# 2. MODE Engine Internals

The MODE engine enforces a deterministic lifecycle:

\`\`\`
Load → Preflight → Execute → Postprocess → Emit
\`\`\`

### Component Responsibilities

| Component | Responsibility |
|----------|----------------|
| Loader | Loads MODE manifest, config, and code |
| Preflight | Validates inputs, overrides, and environment |
| Executor | Runs the MODE’s core logic |
| Postprocess | Normalizes output and detects anomalies |
| Emitter | Writes artifacts, logs, and structured output |

This strict lifecycle ensures reproducibility, isolation, and forensic clarity.

---

# 3. Development Environment

### Install Dev Dependencies

\`\`\`
pip install -r requirements-dev.txt
\`\`\`

### Run Tests

\`\`\`
pytest -q
\`\`\`

### Linting (if enabled)

\`\`\`
flake8
black --check .
\`\`\`

---

# 4. Logging

The console uses structured logging with fields such as:

- timestamp  
- event  
- target  
- duration  
- correlation_id  

Example:

\`\`\`
context.log(event="request_sent", target=url, duration_ms=120)
\`\`\`

Logs are written to:

\`\`\`
runs/<run_id>/logs/execution.log
\`\`\`

---

# 5. Adding New Features

When adding new features:

- Follow coding standards  
- Use type hints  
- Update documentation  
- Add tests  
- Avoid global state  
- Keep functions deterministic  

---

# 6. Directory Conventions

### Core modules must:

- Avoid side effects  
- Avoid environment‑dependent behavior  
- Use dependency injection where possible  

### MODEs must:

- Be self‑contained  
- Use schemas for input/output  
- Use handlers for lifecycle stages  
- Never import from other MODEs  

---

# 7. Testing Strategy

The project uses:

- **Unit tests** for core logic  
- **Integration tests** for MODE execution  
- **Schema validation tests**  
- **Regression tests** for snapshots/diffs  

Run all tests:

\`\`\`
pytest -q
\`\`\`

---

# 8. Adding a New MODE (Developer Workflow)

1. Create directory:

\`\`\`
console/modes/<mode_name>/
\`\`\`

2. Add required files:

\`\`\`
mode.yaml
main.py
config.py
handlers/
schemas/
tests/
\`\`\`

3. Validate:

\`\`\`
console modes validate <mode_name>
\`\`\`

4. Test:

\`\`\`
pytest -q
\`\`\`

5. Document in:

- MODE_CATALOG.md  
- DOCS_INDEX.md  

---

# 9. API Development

API endpoints live in:

\`\`\`
console/api/
\`\`\`

Follow these rules:

- Use Pydantic models  
- Validate all inputs  
- Return structured errors  
- Never expose filesystem paths directly  

---

# 10. Dashboard Development

Dashboard code lives in:

\`\`\`
dashboard/
\`\`\`

Panels include:

- Run history  
- Anomaly viewer  
- Artifact browser  
- Logs viewer  
- Diff viewer  

Dashboard reads from the filesystem only — no write operations.

---

# 11. Extensibility Guidelines

When extending the system:

- Prefer composition over inheritance  
- Keep MODEs isolated  
- Keep core modules generic  
- Avoid hard‑coding MODE names  
- Use schemas for all structured data  

---

# 12. Security Considerations

Developers must ensure:

- No arbitrary code execution  
- No unvalidated input  
- No external dependencies inside MODEs  
- No cross‑MODE access  
- No writes outside run directories  

---

# 13. Release Workflow

1. Update CHANGELOG.md  
2. Bump version  
3. Run full test suite  
4. Tag release  
5. Merge to main  

---

# Conclusion

The SSRF Command Console is designed for clarity, determinism, and extensibility.  
Following this guide ensures consistent, high‑quality contributions across the entire project.
