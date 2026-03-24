# TESTING_GUIDE.md

SSRF COMMAND CONSOLE — TESTING GUIDE
Operator‑Grade, Forensic, Repeatable Testing Framework

---

## 1. PURPOSE OF THIS DOCUMENT

This guide defines the complete testing strategy for the SSRF Command Console.
It ensures that all contributors follow a consistent, auditable, and deterministic testing workflow.

This document covers:

- Test environment setup
- Unit tests
- Integration tests
- Mode validation tests
- Regression testing
- Performance and stability checks
- Testing conventions and directory structure

---

## 2. TEST ENVIRONMENT SETUP

### 2.1 Install Test Dependencies

pip install -r requirements-dev.txt

### 2.2 Recommended Tools

- pytest
- pytest-asyncio
- httpx
- coverage.py
- ruff (linting)
- mypy (type checking)

### 2.3 Environment Variables

Testing should never rely on production credentials.

Use: TESTING=1

Optional: MOCK_NETWORK=1 MOCK_DNS=1

---

## 3. TEST DIRECTORY STRUCTURE

tests/ unit/ test_utils.py test_validators.py test_mode_registry.py integration/ test_api_endpoints.py test_dashboard_routes.py test_history_persistence.py modes/ test_direct_fetch.py test_header_injection.py test_dns_discovery.py test_port_sweep.py test_protocol_abuse.py regression/ snapshots/ test_regressions.py

This structure ensures clean separation between:

- **Unit tests** — pure logic, no I/O
- **Integration tests** — API + dashboard + persistence
- **Mode tests** — each scanning mode validated independently
- **Regression tests** — snapshot‑based, preventing reintroduced bugs

---

## 4. UNIT TESTING

### 4.1 Purpose

Validate isolated logic without touching:

- Network
- Filesystem
- Database
- External services

### 4.2 Running Unit Tests

pytest tests/unit -q

### 4.3 What to Test

- Input validation
- URL normalization
- Mode registration
- Error handling
- Utility functions
- Response classification logic

### 4.4 Example Unit Test

```python
def test_normalize_url():
    assert normalize_url("127.0.0.1") == "http://127.0.0.1"

##5. INTEGRATION TESTING

5.1 Purpose
Validate the system as a whole:
• 	API endpoints
• 	Dashboard routes
• 	History logging
• 	Mode execution pipeline

## RUNNING INTEGRATION TESTS

pytest tests/integration -q

##5.3 Mocking Strategy
Use:
• 	Mocked HTTP servers
• 	Mocked DNS resolvers
• 	Mocked internal services
Avoid:
• 	Real network calls
• 	Real DNS lookups
• 	Real SSRF targets

##5.4 Example Integration Test
async def test_console_loads(async_client):
    response = await async_client.get("/console")
    assert response.status_code == 200

## 6. MODE VALIDATION TESTING
## 6.1 Purpose
Ensure each scanning mode:
• 	Loads correctly
• 	Executes without crashing
• 	Produces expected response patterns
• 	Handles invalid input gracefully

## 6.2 Running Mode Tests
pytest tests/modes -q

##6.3 Required Tests Per Mode

Each mode must include:
• 	Initialization test
• 	Payload generation test
• 	Response classification test
• 	Error handling test
• 	Timeout behavior test

## 7. REGRESSION TESTING

## 7.1 Purpose

Prevent previously fixed bugs from returning.

## 7.2 Snapshot Testing
Store snapshots in:
tests/regression/snapshots/

## 7.3 Running Regression Tests

pytest tests/regression -q

## 7.4 When to Add a Regression Test
• 	A bug is fixed
• 	A mode is refactored
• 	A new protocol handler is added
• 	A breaking change is discovered

## 8. PERFORMANCE TESTING (OPTIONAL)

## 8.1 Purpose
Measure:
• 	Latency
• 	Mode execution time
• 	Dashboard load time
• 	API throughput
## 8.2 Tools
• 	Locust
• 	pytest-benchmark

## 8.3 Running Benchmarks
pytest --benchmark-only

## 9. STABILITY & FAULT-INJECTION TESTING (OPTIONAL)

## 9.1 Purpose
Ensure the console behaves correctly under:
• 	Timeouts
• 	Slow responses
• 	Malformed responses
• 	Redirect loops
• 	DNS failures
## 9.2 Fault Injection Examples
• 	Simulated DNS NXDOMAIN
• 	Simulated TCP timeout
• 	Simulated HTTP 500/502/504
• 	Simulated infinite redirect

## 10. COVERAGE REQUIREMENTS

## 10.1 Minimum Coverage
85% total coverage
90% for core modules

## 10.2 Running Coverage

coverage run -m pytest
coverage report -m

## 10.3 Generating HTML Report
coverage html

## 11. LINTING & TYPE CHECKING

## 11.1 Linting
ruff check .

## 11.2 Type Checking
mypy app/

## 11.3 Required Before Merge
 	No lint errors
• 	No type errors

## 12. CI/CD TESTING PIPELINE
## 12.1 Required Stages
• 	Lint
• 	Type check
• 	Unit tests
• 	Integration tests
• 	Mode validation tests
• 	Coverage enforcement
## 12.2 Optional Stages
• 	Performance benchmarks
• 	Fault‑injection suite
• 	Documentation link checker

## 13. APPENDIX — ESCAPED FENCING EXAMPLES

## 13.1 Escaped Code Block
bash pytest -q

## 13.2 Escaped JSON
json {"test": "value"}
```
