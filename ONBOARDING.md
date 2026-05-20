# Onboarding Guide — SSRF Command Console

Welcome to the SSRF Command Console.
This guide walks you from zero to fully operational with clear, operator‑grade steps.

---

## 1. Prerequisites

Before starting, ensure you have:

- Git
- Python 3.10+ or 3.11
- Make
- pip, uv, or Poetry (choose one)
- Docker (recommended for isolation)

---

## 2. Clone and Bootstrap

Clone the repository:

```bash
git clone <REPO_URL>
cd <REPO_DIR>

## Bootstrap the environment:
make bootstrap
make self-check

 ## If using uv:
	make uv-bootstrap

 ## If using Poetry:
	make poetry-bootstrap

### 3. Quick Health Check
Run the operator console:

./ops

or run the doctor script directly:

scripts/doctor.sh

This verifies:
- Python environment
- Git status
- Common dev ports
- Basic system health


### 4. Running the Application
Choose one of the supported execution paths:
Direct Python

python3 main.py

## uv
make uv-run

## Poetry
make poetry-run

## Docker
make docker-build
make docker-run

### Development Workflow
Format Code
make format

## Lint + Type Check
make lint

## Run Tests
make test

## Full CI Gate
make ci-check

This ensures:
• 	Formatting
• 	Linting
• 	Typing
• 	Tests
• 	Structural validation


### 6. Understanding the Project Structure
Key directories:

Makefile                     # Operator-grade build system
validators/                 # Structural + integrity validators
scripts/                    # Operator utilities (Linux/macOS)
scripts/windows/            # Operator utilities (Windows)
docs/                       # Documentation suite
tools/                      # Bootstrap wizard and internal tools


### 7. Resetting / Cleaning
If your environment becomes inconsistent:

make uninstall
make bootstrap
make self-check

This resets:

Virtual environments
Dockeer artifacts
Git hooks
Caches

### 8. Next Steps
Recommended reading:

docs/architecture.md
docs/operations.md
docs/development.md
CONTRIBUTING.md
```
