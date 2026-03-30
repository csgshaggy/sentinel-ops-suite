# Developer Onboarding Guide

Welcome to the SSRF Command Console. This guide walks you through setup, validation, environment management, and release workflows.

---

## 1. Prerequisites

Install:

- Python 3.11+
- Node 20+
- npm 10+
- Git
- Virtual environment tools (`python3 -m venv`)

---

## 2. Clone and Bootstrap

```bash
git clone https://github.com/<your-org>/ssrf-command-console.git
cd ssrf-command-console
make bootstrap
