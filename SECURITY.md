# Security Policy — SSRF Command Console

This document outlines the security expectations, reporting process, and hardening recommendations for the SSRF Command Console.

The project is designed with an operator‑grade security posture, emphasizing deterministic behavior, strict validation, and CI‑enforced safety checks.

---

## Supported Versions

Security fixes are applied to the `main` branch.  
Consumers should track `main` or tagged releases.

---

## Reporting a Vulnerability

If you discover a security issue related to:

- SSRF handling  
- Request forwarding  
- Plugin execution  
- Authentication or authorization  
- Misconfiguration that could lead to unsafe behavior  

Please follow these steps:

1. **Do not** open a public issue containing exploit details.  
2. Provide a minimal, reproducible description privately.  
3. Include:
   - Environment details  
   - Sanitized configuration  
   - Steps to reproduce  
   - Expected vs. actual behavior  

Clear, actionable reports help maintainers respond quickly and safely.

---

## Security Posture

The SSRF Command Console is built with:

### **1. Structural Validation**
Validators enforce project integrity:

- `project_structure_validator.py`
- `python_import_validator.py`
- `makefile_integrity_validator.py`

Run manually with:

```bash
make self-check

### CI-Enforce Security Scans
make ci-security

### Dependency Visibility
make deps

This generates a dependency graph for auditing

4. Deterministic Build System
The Makefile enforces:
• 	Explicit targets
• 	No hidden behavior
• 	Reproducible workflows


### Hardening Recommendations
Use Docker for Isolation

make docker-builld
make docker-run

This ensures consistent environment and reduces host exposure

### Restrict Outbound Network Access
Especially when testing SSRF vectors.
### Review Plugins Before Enabling
Plugins run code — treat them as privileged components.

### Run CI Gates Before Deployment
make ci-check

This ensures:
• 	Formatting
• 	Linting
• 	Typing
• 	Testing
• 	Structural validation

### Tools Used
Bandit
Static analysis for Python security issues:

make ci-security

### Docker
Provides isolation and reproducibility.

###Validators
Ensure the project structure remains safe and predictable.

### Responsible Disclosure
We appreciate responsible disclosure and will work with you to validate, patch, and release fixes promptly.
