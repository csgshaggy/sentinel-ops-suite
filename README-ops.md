# Sentinel Ops Suite — Operator Handbook

This document defines the **operator workflow**, **tooling**, and **lifecycle commands** for the Sentinel Ops Suite.
It is the single source of truth for how operators interact with the system.

---

# 🧭 Operator Workflow Overview

The operator workflow is built around four pillars:

1. **Sync** — keep the repository clean, validated, and up to date
2. **Health** — validate structure, detect drift, and ensure operational integrity
3. **Bootstrap** — initialize or repair the operator environment
4. **Ops Console** — a unified CLI wrapper for all operator actions

---

# 🔄 1. Repository Sync

The sync pipeline is executed via:
make sync


This performs:

- Pre‑sync validation
- Auto‑staging of tracked + untracked files
- Commit (if needed)
- Fetch + rebase
- Push
- Post‑sync health snapshot
- Governance checks

The sync pipeline is defined in:

- `sync.sh`
- `scripts/sync/pre-sync-validate.cjs`
- `scripts/sync/post-sync-health-snapshot.cjs`
- `scripts/sync/post-sync-governance.cjs`

---

# 🩺 2. Ops Health

Run a full operator health check:
make ops-health


This executes:

- `ops/self-heal.sh --dry-run`
- Makefile validator
- Repo structure checksum
- CI‑grade drift detector

This is the operator’s “daily health check.”

---

# 🚀 3. Ops Bootstrap

Initialize or repair the operator environment:
make ops-bootstrap


Bootstrap performs:

- Directory creation
- Repo structure checksum baseline
- Drift baseline creation
- Manifest generation (`.ops/manifest.json`)

This is the first command run on a fresh clone.

---

# 🧰 4. Ops Console (Unified CLI)

The `ops` wrapper provides a single entry point:

./ops <command>


Examples:
./ops sync ./ops health ./ops drift ./ops bootstrap ./ops validate


The wrapper delegates to Make targets and operator scripts.

---

# 📂 Directory Structure
sentinel-ops-suite/ │ ├── backend/ ├── frontend/ │ ├── scripts/ │   ├── sync/ │   └── ops/ │ ├── ops/ │   └── self-heal.sh │ ├── snapshots/ ├── .ops/ │   └── manifest.json │ ├── sync.sh └── Makefile


---

# 🛡 Governance

Governance ensures:

- Required directories exist
- Makefile contains PHONY declarations
- No merge conflict markers
- Repo structure matches baseline

Governance is enforced automatically during `make sync`.

---

# 🛰 Drift Detection

Two layers:

- **Structure drift** — file tree changes
- **Content drift** — file hash changes

Tools:

- `scripts/ops/repo-structure-checksum.cjs`
- `scripts/ops/drift-detector.cjs`

---

# 📝 Manifest

`.ops/manifest.json` is auto‑generated and contains:

- All Make targets
- All operator scripts
- All sync scripts
- All ops utilities

Never edit it manually.

---

# ✔ Operator Summary

| Action | Command |
|--------|---------|
| Sync repo | `make sync` |
| Run health suite | `make ops-health` |
| Bootstrap ops environment | `make ops-bootstrap` |
| Validate Makefile | `make validate-makefile` |
| Check structure checksum | `make repo-structure-checksum` |
| CI drift detection | `make drift-ci` |
| Unified CLI | `./ops <cmd>` |

---

End of Operator Handbook.


