# CONTRIBUTOR_TROUBLESHOOTING.md

SSRF COMMAND CONSOLE — CONTRIBUTOR TROUBLESHOOTING GUIDE
Environment Issues • Dependency Conflicts • Mode Failures • Extension Errors

---

## 1. PURPOSE OF THIS DOCUMENT

This guide helps contributors diagnose and resolve common issues encountered while developing, extending, or testing the SSRF Command Console.

It covers:

- Environment setup failures
- Dependency conflicts
- Mode registration issues
- Extension loading errors
- Test failures
- Debugging workflows

This is the authoritative troubleshooting reference for contributors.

---

## 2. ENVIRONMENT SETUP ISSUES

### 2.1 Virtual Environment Not Activated

**Symptoms:**

- `ModuleNotFoundError`
- Wrong Python version
- Dependencies missing

**Fix:**

python -m venv venv source venv/bin/activate # Linux/macOS venv\Scripts\activate # Windows pip install -r requirements.txt

---

### 2.2 Wrong Python Version

**Symptoms:**

- Syntax errors
- Async errors
- Dependency installation failures

**Fix:**
Use the required Python version listed in `INSTALLATION_AND_SETUP.md`.

---

### 2.3 Dependency Conflicts

**Symptoms:**

- Import errors
- Version mismatch errors
- Unexpected runtime behavior

**Fix:**

pip install --upgrade --force-reinstall -r requirements.txt

---

## 3. MODE DEVELOPMENT ISSUES

### 3.1 Mode Not Appearing in Catalog

**Symptoms:**

- Mode missing from `/modes` endpoint
- Dashboard does not list mode

**Causes & Fixes:**

- **Missing `id` field** → Add `id = "my_mode"`
- **Missing manifest entry** → Add mode to `manifest.json`
- **Syntax error in mode file** → Run `pytest` to locate error
- **Incorrect class name** → Must match manifest entrypoint

---

### 3.2 Mode Crashes on Execution

**Symptoms:**

- 500 errors
- Unhandled exceptions
- Missing attributes

**Fix:**
Check:

- `build_payload()` returns a dict
- `execute()` uses async I/O
- `classify_response()` returns a string
- No raw exceptions are raised

---

### 3.3 Classification Not Working

**Symptoms:**

- Always returns `unknown`
- Incorrect classification

**Fix:**

- Verify response patterns
- Precompile regex
- Log raw response in DEBUG mode
- Compare with known patterns

---

## 4. EXTENSION DEVELOPMENT ISSUES

### 4.1 Extension Not Loading

**Symptoms:**

- Missing API routes
- Missing modes
- Missing dashboard panels

**Fix:**
Check `manifest.json`:

- Correct `id`
- Correct entrypoint paths
- Valid JSON syntax

---

### 4.2 Extension Crashes on Startup

**Symptoms:**

- Import errors
- Attribute errors
- Missing modules

**Fix:**

- Ensure extension directory has `__init__.py`
- Ensure entrypoints exist
- Run `pytest extensions/<id>`

---

### 4.3 Dashboard Panel Not Rendering

**Symptoms:**

- Blank panel
- JS errors in console

**Fix:**

- Validate `panel.json`
- Ensure component file exists
- Check browser console for JS errors

---

## 5. API & ROUTING ISSUES

### 5.1 API Route Not Found

**Symptoms:**

- 404 errors
- Missing endpoints

**Fix:**

- Ensure router is included in manifest
- Ensure prefix matches `/api/ext/<id>`
- Restart console after changes

---

### 5.2 API Returns 500 Errors

**Symptoms:**

- Unhandled exceptions
- Missing fields

**Fix:**

- Validate request schema
- Validate response schema
- Check logs for stack traces

---

## 6. TEST FAILURES

### 6.1 Unit Tests Failing

**Symptoms:**

- Assertion errors
- Import errors

**Fix:**

- Run tests with `pytest -q`
- Check for missing mocks
- Ensure no real network calls

---

### 6.2 Mode Tests Failing

**Symptoms:**

- Incorrect classification
- Unexpected payloads

**Fix:**

- Compare expected vs actual payload
- Validate classification logic
- Enable DEBUG logs

---

### 6.3 Regression Tests Failing

**Symptoms:**

- Snapshot mismatches

**Fix:**
If change is intentional:

pytest --snapshot-update

If not:

- Investigate behavioral drift
- Compare with previous version

---

## 7. COMMON PITFALLS

### 7.1 Forgetting `async` in Mode Methods

**Fix:** All mode methods must be async.

---

### 7.2 Returning Non‑Serializable Data

**Fix:** Ensure payloads and results are JSON‑serializable.

---

### 7.3 Logging Secrets

**Fix:** Never log:

- Tokens
- Credentials
- Internal URLs

---

### 7.4 Using Blocking I/O

**Fix:** Replace with async equivalents.

---

## 8. DEBUGGING WORKFLOWS

### 8.1 Enable DEBUG Logging

export LOG_LEVEL=DEBUG

### 8.2 Inspect Trace Events

Check:

- `mode.start`
- `mode.payload_built`
- `mode.request_sent`
- `mode.response_received`
- `mode.classified`

### 8.3 Use Safe Mode

python main.py --safe

Loads:

- Core modes only
- No extensions

---

## 9. WHEN TO ASK FOR HELP

Ask for help when:

- You cannot reproduce an issue
- A mode behaves inconsistently
- Classification logic seems incorrect
- Extension loading fails silently
- Tests pass locally but fail in CI

Include:

- Logs
- Trace ID
- Steps to reproduce
- Environment details

---

## 10. APPENDIX — ESCAPED FENCING EXAMPLES

### 10.1 Escaped Code Block

```markdown
error: "ModeNotRegistered"

### 10.2 Escaped JSON Block

json {"troubleshooting": "missing_manifest_entry"}
```
