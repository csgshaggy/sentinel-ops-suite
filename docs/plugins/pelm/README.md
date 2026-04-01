# PELM Module Documentation

## Overview
The PELM module provides a cohesive set of API routes, streaming endpoints,
plugin logic, and validation tests designed to extend the SSRF Command Console
with a clean, modular subsystem. It follows the project's operator-grade
standards for determinism, observability, and maintainability.

PELM integrates with:
- FastAPI router layer
- Plugin execution framework
- Test suite
- Makefile task system
- Documentation and governance structure

This document describes the architecture, components, workflows, and operational
usage of the PELM module.

## Architecture

### Components
| Component | Purpose |
|----------|---------|
| PELM Router | Exposes synchronous API endpoints under /pelm |
| PELM Stream Router | Provides streaming output under /pelm/stream |
| PELM Plugin | Implements a standalone plugin with a simple execution contract |
| PELM Tests | Validates plugin behavior and ensures deterministic execution |
| Makefile Tasks | Provides CLI entrypoints for PELM operations |
| Documentation | Centralized reference for architecture, usage, and extension |

### Directory Layout

app/routers/pelm.py app/routers/pelm_stream.py tools/plugins/pelm.py tests/pelm/test_pelm_plugin.py docs/plugins/pelm/README.md Makefile


## API Layer

### PELM Router (/pelm)
The primary router exposes a simple health endpoint used for validation,
monitoring, and integration testing.

#### GET /pelm/health
Returns a JSON payload confirming module availability.

Example response:

{ "status": "ok", "module": "pelm" }

### Streaming Router (/pelm/stream)
The streaming router provides a minimal streaming response suitable for:
- SSE-style integrations
- Long-running operations
- Progressive output testing

#### GET /pelm/stream
Returns a streaming text response:

pelm-stream-start pelm-stream-end


## Plugin Layer

### PELM Plugin (tools/plugins/pelm.py)
The plugin implements a simple, deterministic execution contract:

class PELMPlugin: name = "pelm"

def run(self):
    return {"plugin": "pelm", "status": "executed"}

    
Characteristics:
- Zero side effects
- Fully deterministic
- CI-safe
- Serves as a template for more advanced plugin behavior

Use cases:
- Demonstrating plugin discovery
- Validating plugin execution pipelines
- Providing a baseline for future PELM functionality

## Test Suite

### Location

tests/pelm/test_pelm_plugin.py


### Purpose
Ensures:
- Plugin importability
- Deterministic return values
- Correct execution contract

Example test:

def test_pelm_plugin_runs(): plugin = PELMPlugin() result = plugin.run() assert result["status"] == "executed"


## Makefile Integration

The Makefile includes a complete set of PELM-specific tasks:

pelm-health:     Validate router health pelm-stream:     Validate streaming router pelm-plugin:     Execute plugin pelm-test:       Run PELM test suite pelm-docs:       Placeholder for future doc generation


These tasks ensure:
- Consistent developer workflows
- CI-friendly execution
- Operator-grade repeatability

## Running PELM

### Start the application

uvicorn app.main:app --reload


### Validate the module

make pelm-health make pelm-stream make pelm-plugin make pelm-test


Manual validation:
- http://localhost:8000/pelm/health
- http://localhost:8000/pelm/stream

## Extending PELM

You can extend:

### Routers
Add new endpoints under:

app/routers/pelm.py


### Streaming
Enhance the generator in:

app/routers/pelm_stream.py


### Plugin Logic
Extend or replace:

tools/plugins/pelm.py


### Tests
Add new test files under:

tests/pelm/


### Makefile Tasks
Add new operator-grade tasks under the PELM section.

## Summary
The PELM module includes:
- API router
- Streaming router
- Plugin
- Test suite
- Makefile tasks
- Documentation
- Correct directory alignment
- Linux-native workflows
- Deterministic, operator-grade behavior

This README serves as the authoritative reference for the module and reflects
all work completed during the recent development cycle.


+-------------------------------------------------------------+
|                     SSRF Command Console                    |
+---------------------------+---------------------------------+
                            |
                            v
                    +---------------+
                    |   FastAPI     |
                    |   app.main    |
                    +-------+-------+
                            |
            +---------------+-------------------+
            |                                   |
            v                                   v
+-------------------------+        +-------------------------+
|   app/routers/pelm.py   |        | app/routers/pelm_      |
|                         |        | stream.py              |
|  /pelm/health           |        |  /pelm/stream          |
+------------+------------+        +------------+-----------+
             |                                      |
             |                                      |
             v                                      v
   Health check JSON                      Streaming text response
   status: ok, module: pelm              "pelm-stream-start/end"


+-------------------------------------------------------------+
|                    Plugin and Test Layer                    |
+-------------------------+-----------------+-----------------+
                          |                 |
                          v                 v
               +-----------------+   +------------------------+
               | tools/plugins/  |   | tests/pelm/            |
               | pelm.py         |   | test_pelm_plugin.py    |
               +--------+--------+   +-----------+------------+
                        |                        |
                        v                        v
               PELMPlugin.run()          Asserts deterministic
               returns {status:          plugin behavior
               "executed"}               ("executed")


+-------------------------------------------------------------+
|                        Makefile Layer                       |
+-------------------------------------------------------------+
| pelm-health | pelm-stream | pelm-plugin | pelm-test |       |
+-------------+-------------+-------------+-----------+-------+
        |             |             |             |
        v             v             v             v
   Calls app/    Calls app/    Calls tools/   Runs tests/
   routers/      routers/      plugins/      pelm/
   pelm.py       pelm_stream   pelm.py
                 .py


                 Legend:
U = User / Operator
A = FastAPI app
R = PELM router
S = PELM stream router
P = PELM plugin
T = Test suite
M = Makefile

1) Health check flow
--------------------

U          M          A          R
|          |          |          |
| make pelm-health    |          |
|-------------------->|          |
|          uv run app/routers/pelm.py
|------------------------------->|
|                     route /pelm/health
|--------------------------------------->|
|                                build JSON {status: "ok", module: "pelm"}
|<--------------------------------------|
|<-------------------------------|
|<--------------------|
User sees health OK


2) Streaming flow
-----------------

U          M          A          S
|          |          |          |
| make pelm-stream    |          |
|-------------------->|          |
|          uv run app/routers/pelm_stream.py
|------------------------------->|
|                     route /pelm/stream
|--------------------------------------->|
|                                start generator
|                                yield "pelm-stream-start"
|                                yield "pelm-stream-end"
|<--------------------------------------|
|<-------------------------------|
|<--------------------|
User sees streaming text


3) Plugin execution flow
------------------------

U          M          P
|          |          |
| make pelm-plugin    |
|-------------------->|
|          uv run tools/plugins/pelm.py
|------------------------------->|
|                     PELMPlugin.run()
|                     returns {"plugin": "pelm", "status": "executed"}
|<-------------------------------|
|<--------------------|
User sees plugin executed


4) Test flow
------------

U          M          T          P
|          |          |          |
| make pelm-test      |          |
|-------------------->|          |
|          pytest tests/pelm     |
|------------------------------->|
|                     import PELMPlugin
|                     call run()
|                     assert status == "executed"
|<-------------------------------|
|<--------------------|
User sees tests passing

## PELM Troubleshooting Guide

### 1. /pelm/health returns 404 or 500

Checks:
- Confirm file exists:
  - app/routers/pelm.py
- Confirm router is included in app.main:
  - The FastAPI app must include the PELM router, for example:
    - app.include_router(pelm.router)
- Confirm server is running:
  - uvicorn app.main:app --reload

If still failing:
- Check logs for import errors or typos in pelm.py.
- Verify prefix="/pelm" and path="/health" are correct.

### 2. /pelm/stream does not stream or hangs

Checks:
- Confirm file exists:
  - app/routers/pelm_stream.py
- Confirm router is included in app.main:
  - app.include_router(pelm_stream.router)
- Ensure the generator function yields strings and not bytes.

If still failing:
- Add temporary logging or print statements inside the generator.
- Hit the endpoint with curl:
  - curl -v http://localhost:8000/pelm/stream

### 3. make pelm-plugin fails

Checks:
- Confirm file exists:
  - tools/plugins/pelm.py
- Confirm PELMPlugin is defined with a run() method.
- Run directly:
  - uv run tools/plugins/pelm.py

If still failing:
- Check for import errors or missing dependencies.
- Ensure the virtual environment is activated.

### 4. make pelm-test fails

Checks:
- Confirm file exists:
  - tests/pelm/test_pelm_plugin.py
- Run tests directly:
  - pytest tests/pelm -q

If still failing:
- Inspect the assertion:
  - Ensure PELMPlugin.run() returns a dict with status == "executed".
- Check for path or import issues:
  - PYTHONPATH may need to include project root.

### 5. Makefile tasks not found

Checks:
- Confirm Makefile exists at repo root.
- Run:
  - make -n pelm-health
- If target not found:
  - Open Makefile and verify PELM section is present and not indented with spaces.
  - Make requires tabs before commands, not spaces.

### 6. General environment issues

Checks:
- Ensure virtual environment is active:
  - source venv/bin/activate
- Ensure dependencies are installed:
  - uv pip install -r requirements.txt (or project equivalent)
- Re-run:
  - make lint
  - make test
  - make pelm-test

  ## PELM Governance

### Ownership
- Logical owner: SSRF Command Console backend and plugin maintainers.
- Scope: API routes, streaming endpoints, plugin behavior, tests, and Makefile tasks
  related to PELM.

### Change Control
- All changes to PELM must:
  - Include updated tests under tests/pelm/.
  - Maintain deterministic behavior of PELMPlugin.run().
  - Preserve or extend existing Makefile tasks for PELM.
  - Update this README when behavior or interfaces change.

### Review Requirements
- At least one reviewer familiar with:
  - FastAPI routing patterns.
  - Plugin architecture under tools/plugins/.
  - Project Makefile conventions.
- Changes that affect external behavior (routes, responses, or plugin contract)
  must be documented in this README.

### Testing Requirements
- Required before merge:
  - make lint
  - make test
  - make pelm-test
- For streaming changes:
  - Manual verification of /pelm/stream using curl or browser.

### Backward Compatibility
- Route paths under /pelm and /pelm/stream should not be changed without:
  - Deprecation notes in this README.
  - Coordination with any consumers that depend on these endpoints.
- PELMPlugin.run() should remain stable or provide a clear migration path.

### Decommissioning
- If PELM is ever deprecated:
  - Mark the module as deprecated in this README.
  - Remove PELM tasks from the Makefile in a controlled change.
  - Remove or archive tests under tests/pelm/.
  - Ensure no external systems depend on PELM routes or plugin behavior.

  
