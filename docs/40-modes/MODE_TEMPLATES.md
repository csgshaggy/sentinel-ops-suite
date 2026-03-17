# MODE Templates

## Overview
This document provides complete, ready‑to‑use templates for building new MODEs in the SSRF Command Console.  
Each template follows the deterministic lifecycle and directory structure defined in `MODE_AUTHORING.md`.

Templates include:

- Directory structure  
- mode.yaml  
- config.py  
- Input/Output schemas  
- Preflight handler  
- Executor handler  
- Postprocess handler  
- main.py entrypoint  
- Test templates  

Use these as starting points for new MODE development.

---

# 1. MODE Directory Template

\`\`\`
console/modes/<mode_name>/
├── mode.yaml
├── main.py
├── config.py
├── handlers/
│   ├── preflight.py
│   ├── executor.py
│   └── postprocess.py
├── schemas/
│   ├── input.py
│   └── output.py
└── tests/
    ├── test_integration.py
    ├── test_schemas.py
    └── test_unit.py
\`\`\`

---

# 2. mode.yaml Template

\`\`\`
name: <mode_name>
version: 1.0.0
entrypoint: main:run
summary: <short description of what this MODE does>

requires:
  - network
  - http

config:
  timeout: 5
  retries: 2

outputs:
  - raw_responses
  - anomalies
\`\`\`

---

# 3. config.py Template

\`\`\`
DEFAULT_CONFIG = {
    "timeout": 5,
    "retries": 2,
    "max_redirects": 3,
    "user_agent": "SSRF-Console/1.0"
}
\`\`\`

---

# 4. Input Schema Template (schemas/input.py)

\`\`\`
from pydantic import BaseModel, HttpUrl
from typing import List

class Input(BaseModel):
    targets: List[str]
\`\`\`

---

# 5. Output Schema Template (schemas/output.py)

\`\`\`
from pydantic import BaseModel
from typing import Dict, List

class Output(BaseModel):
    raw_responses: Dict[str, str]
    anomalies: List[str]
\`\`\`

---

# 6. Preflight Handler Template (handlers/preflight.py)

\`\`\`
def run(input_data, config):
    # Validate targets
    if not input_data.targets:
        raise ValueError("At least one target is required.")

    for t in input_data.targets:
        if not isinstance(t, str):
            raise ValueError(f"Invalid target: {t}")

    # Validate config values
    if config["timeout"] <= 0:
        raise ValueError("Timeout must be positive.")

    return {
        "validated_targets": input_data.targets,
        "config": config
    }
\`\`\`

---

# 7. Executor Handler Template (handlers/executor.py)

\`\`\`
import requests

def run(preflight_data):
    targets = preflight_data["validated_targets"]
    config = preflight_data["config"]

    responses = {}

    for target in targets:
        try:
            r = requests.get(
                f"http://{target}",
                timeout=config["timeout"],
                headers={"User-Agent": config["user_agent"]},
                allow_redirects=True
            )
            responses[target] = r.text
        except Exception as e:
            responses[target] = f"ERROR: {str(e)}"

    return {"raw_responses": responses}
\`\`\`

---

# 8. Postprocess Handler Template (handlers/postprocess.py)

\`\`\`
def run(executor_data):
    raw = executor_data["raw_responses"]
    anomalies = []

    for target, body in raw.items():
        if "metadata" in body.lower():
            anomalies.append(f"Potential SSRF indicator in {target}")

    return {
        "raw_responses": raw,
        "anomalies": anomalies
    }
\`\`\`

---

# 9. main.py Template

\`\`\`
from schemas.input import Input
from schemas.output import Output
from handlers import preflight, executor, postprocess
from config import DEFAULT_CONFIG

def run(input_data: dict, overrides: dict = None):
    # Load input
    parsed_input = Input(**input_data)

    # Merge config
    config = DEFAULT_CONFIG.copy()
    if overrides:
        config.update(overrides)

    # Lifecycle
    pre = preflight.run(parsed_input, config)
    exe = executor.run(pre)
    post = postprocess.run(exe)

    # Validate output
    return Output(**post).dict()
\`\`\`

---

# 10. Test Templates

## 10.1 Unit Test Template (tests/test_unit.py)

\`\`\`
def test_timeout_config():
    from config import DEFAULT_CONFIG
    assert DEFAULT_CONFIG["timeout"] > 0
\`\`\`

---

## 10.2 Schema Test Template (tests/test_schemas.py)

\`\`\`
import pytest
from schemas.input import Input

def test_input_schema_valid():
    i = Input(targets=["example.com"])
    assert i.targets == ["example.com"]

def test_input_schema_invalid():
    with pytest.raises(Exception):
        Input(targets=[123])
\`\`\`

---

## 10.3 Integration Test Template (tests/test_integration.py)

\`\`\`
def test_mode_integration(tmp_path):
    from main import run

    result = run({"targets": ["example.com"]})
    assert "raw_responses" in result
    assert "anomalies" in result
\`\`\`

---

# Conclusion

These templates provide a complete, deterministic starting point for building new MODEs.  
They enforce structure, isolation, and reproducibility across the entire MODE ecosystem.
