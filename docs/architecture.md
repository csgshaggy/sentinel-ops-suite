# Architecture — SSRF Command Console

This document provides a high‑level and operator‑grade overview of the SSRF Command Console architecture.
It explains how the system is structured, how components interact, and how the console maintains deterministic, observable behavior.

---

# 1. System Overview

The SSRF Command Console is built around four core pillars:

1. **Backend Engine** — FastAPI‑based SSRF execution and analysis pipeline
2. **Operator Tooling** — Scripts, TUI, and unified wrappers for cross‑platform operations
3. **Build + CI System** — Deterministic Makefile with validators and CI gates
4. **Documentation + Observability** — Full docs suite and structural integrity checks

The architecture is intentionally modular, allowing each layer to evolve independently while maintaining strict boundaries.

---

# 2. High‑Level Architecture Diagram

+-------------------------------------------------------------+
| SSRF Command Console |
+-------------------------------------------------------------+
| |
| +------------------+ +------------------------------+ |
| | Backend Engine | | Operator Tooling | |
| | (FastAPI App) | | scripts/, windows/, ops, TUI| |
| +------------------+ +------------------------------+ |
| |
| +-------------------------------------------------------+ |
| | Build + CI System (Makefile) | |
| | bootstrap, lint, test, docker, validators, CI gates | |
| +-------------------------------------------------------+ |
| |
| +-------------------------------------------------------+ |
| | Documentation + Structural Validators | |
| | docs/, validators/, onboarding, contributing, etc. | |
| +-------------------------------------------------------+ |
| |
+-------------------------------------------------------------+
