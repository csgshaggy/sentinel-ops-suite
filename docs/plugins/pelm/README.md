# PELM — Privilege Escalation & Lateral Movement Governance Module

PELM is a fully observable, regression‑aware, governance‑grade subsystem designed to detect, score, and visualize privilege‑surface drift across an environment. It integrates tightly with the backend, frontend, CI pipeline, and operator console to provide a complete, end‑to‑end governance experience.

---

## 🔍 What PELM Does

- Tracks privilege‑surface changes over time  
- Detects drift, regressions, and risk acceleration  
- Generates snapshots and diffs for forensic comparison  
- Produces HTML and Markdown governance reports  
- Surfaces alerts, anomalies, and severity indicators  
- Provides a full governance dashboard with trend visualization  
- Enforces CI gates to prevent unsafe releases  

---

## 🧩 Architecture Overview

PELM is composed of:

- **Backend Engines**
  - Status engine  
  - Run engine  
  - Trend engine  
  - Snapshot engine  
  - Diff engine  
  - Regression engine  
  - Governance repair engine  
  - Reporting engine  

- **Frontend Components**
  - Governance Dashboard  
  - Regression Panel  
  - Alerts Block  
  - Trend Graph  
  - Snapshot Diff Viewer  
  - Snapshot Timeline  
  - Severity Badges  

- **CI Enforcement**
  - Regression score thresholds  
  - Drift detection  
  - Risk acceleration checks  

- **Repo Hygiene**
  - Backend structure validator  
  - Frontend structure validator  
  - Import validator  
  - Stray main.py scanner  

---

## 📊 Governance Dashboard

The dashboard provides:

- Current risk  
- Snapshot timeline  
- Regression analytics  
- Alerts  
- Trend visualization  
- Quick diff tools  
- Auto‑refresh  
- Compare‑with‑latest shortcut  
- Exportable reports  

---

## 📦 Reports

PELM generates:

- `pelm_report.html`  
- `pelm_report.md`  

Both include:

- Risk summary  
- Trend graphs  
- Snapshot metadata  
- Regression analysis  
- Drift indicators  

---

## 🧪 Testing

PELM includes backend tests for:

- Status  
- Regression  
- Snapshots  

Run with:

make test-backend


---

## 🚦 CI Enforcement

PELM integrates with CI via:

make ci-pelm-check


This prevents unsafe releases by enforcing:

- No drift  
- No regression spikes  
- No risk acceleration  

---

## 🏁 Status

PELM is **complete**, production‑ready, and fully integrated across backend, frontend, CI, and governance layers.
