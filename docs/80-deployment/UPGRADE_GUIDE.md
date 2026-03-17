# UPGRADE_GUIDE.md
SSRF COMMAND CONSOLE — UPGRADE GUIDE  
Version Migration • Breaking Changes • Deprecation • Safe Rollouts

---

## 1. PURPOSE OF THIS DOCUMENT
This guide explains how to safely upgrade the SSRF Command Console between versions.  
It ensures:

- Predictable upgrades  
- Zero‑downtime transitions  
- Clear handling of breaking changes  
- Safe migration of configuration, modes, and extensions  
- Backward‑compatible evolution of the API and dashboard  

This is the authoritative reference for all upgrade procedures.

---

## 2. VERSIONING MODEL

### 2.1 Semantic Versioning
The project uses SemVer:

MAJOR.MINOR.PATCH


- **MAJOR** — breaking changes  
- **MINOR** — new features, backward‑compatible  
- **PATCH** — bug fixes, no behavior changes  

### 2.2 Stability Guarantees
- MINOR and PATCH upgrades must not break existing modes  
- API fields are never removed except in MAJOR releases  
- Extensions remain compatible across MINOR/PATCH releases  

---

## 3. PRE‑UPGRADE CHECKLIST

Before upgrading, verify:

### 3.1 Environment

Python version matches required version Dependencies are compatible Virtual environment is clean


### 3.2 Configuration
- Backup `config/` directory  
- Validate JSON/YAML syntax  
- Check for deprecated fields  

### 3.3 Modes
- Ensure custom modes follow the latest BaseMode API  
- Validate mode manifests  
- Run mode tests  

### 3.4 Extensions
- Validate extension manifests  
- Check for deprecated entrypoints  
- Run extension tests  

### 3.5 Database / History
If persistent history is enabled:
- Backup history storage  
- Validate schema compatibility  

---

## 4. UPGRADE PROCEDURE

### 4.1 Step 1 — Pull Latest Version

git pull origin main


### 4.2 Step 2 — Reinstall Dependencies


### 4.2 Step 2 — Reinstall Dependencies


pip install -r requirements.txt

### 4.3 Step 3 — Run Preflight Checks
python scripts/preflight_check.py



Checks include:
- Dependency mismatches  
- Deprecated config fields  
- Mode compatibility  
- Extension compatibility  

### 4.4 Step 4 — Run Tests

pytest -q


### 4.5 Step 5 — Start Console in Safe Mode

python main.py --safe


Safe mode:
- Loads core modes only  
- Skips extensions  
- Skips custom protocol handlers  

### 4.6 Step 6 — Re‑enable Extensions
Enable one extension at a time to detect compatibility issues.

### 4.7 Step 7 — Validate Dashboard
Verify:
- Mode execution  
- History panel  
- Logs  
- Metrics  
- Traces  

---

## 5. HANDLING BREAKING CHANGES

### 5.1 Identifying Breaking Changes
Breaking changes are documented in:
- CHANGELOG.md  
- RELEASE_PROCESS.md  
- API_CONTRACTS.md  

### 5.2 Migration Steps
For each breaking change:
- Update configuration fields  
- Update mode definitions  
- Update extension manifests  
- Update API clients  

### 5.3 Deprecated Fields
Deprecated fields remain functional for **one MAJOR version** before removal.

---

## 6. MIGRATING MODES

### 6.1 Required Updates
Check for:
- New BaseMode methods  
- Changed method signatures  
- New classification rules  
- New payload requirements  

### 6.2 Migration Example
Old:
```python
async def execute(self, url): ...

New: 

async def execute(self, payload: dict): ...

### 6.3 Validation

run pytest tests/modes -q

##7. MIGRATING EXTENSIONS
### 7.1 Manifest Changes
Check for:
• 	New entrypoints
• 	Renamed fields
• 	Deprecated fields
### 7.2 API Extensions
Ensure routers still mount under:
/api/ext/<id>

### 7.3 Dashboard Extensions
Validate:
• 	Panel manifest
• 	Component loading
• 	Route registration

## 8. ROLLBACK PROCEDURE
### 8.1 Rollback Steps
1. 	Restore previous commit
2. 	Reinstall previous dependencies
3. 	Restore config backup
4. 	Restore history backup
5. 	Restart console
### 8.2 Rollback Safety
• 	History entries are backward‑compatible
• 	Mode definitions remain stable
• 	Extensions remain stable unless MAJOR version changed

##9. POST‑UPGRADE VERIFICATION
### 9.1 Functional Checks
• 	Execute all core modes
• 	Execute custom modes
• 	Validate classifications
• 	Validate response timing
### 9.2 Observability Checks
• 	Logs
• 	Metrics
• 	Traces
• 	Dashboard panels
### 9.3 Regression Checks

Run: pytest tests/regression -q


## 10. AUTOMATED UPGRADE TESTING
### 10.1 CI Pipeline
CI must test:
• 	Fresh install
• 	Upgrade from previous version
• 	Extension compatibility
• 	Mode compatibility
### 10.2 Upgrade Simulation Script
scripts/simulate_upgrade.py

Simulates:
• 	Config migration
• 	Mode migration
• 	Extension migration

## 11. APPENDIX — ESCAPED FENCING EXAMPLES

### 11.1 Escaped Shell Block
bash git pull origin main

### 11.2 Escaped JSON Block
json {"deprecated": true, "replacement": "new_field"}
