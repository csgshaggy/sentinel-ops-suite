# CI Governance Overview

This repository uses a deterministic, Makefile-driven CI governance model with four major components:

---

## 1. Makefile Drift Check
Ensures the Makefile and mk/ modules remain canonical and drift-free.

- Trigger: PR only  
- Output: `runtime/drift_ci_comment.md`  
- Controlled by: `DRIFT_FAIL` toggle  
- Runner: `scripts/ci/drift_ci_runner.py`

---

## 2. Drift Dashboard
Generates a full drift visualization for maintainers.

- Trigger: PR only  
- Output: `runtime/drift_dashboard.md`  
- Runner: `make drift-dashboard`

---

## 3. Repository Validation
Runs structure checks, formatting checks, and hygiene enforcement.

- Trigger: PR only  
- Output: `runtime/validate_report.md`  
- Runner: `make validate`

---

## 4. Drift History Archive
Maintains a timestamped archive of drift snapshots.

- Trigger: Daily + manual  
- Output: `runtime/drift-history/YYYYMMDD-HHMM.md`  
- Runner: `make drift-snapshot`

---

## Sticky PR Comments
All CI workflows use `marocchino/sticky-pull-request-comment` to ensure:

- One comment per workflow  
- Automatic updates  
- Zero comment spam  

---

## Deterministic CI Philosophy
- No silent failures  
- No ambiguous paths  
- All workflows call Makefile targets  
- All outputs stored in `runtime/`  
- All drift is visible, archived, and auditable  
