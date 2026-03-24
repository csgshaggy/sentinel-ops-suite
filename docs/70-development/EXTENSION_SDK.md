# EXTENSION_SDK.md

SSRF COMMAND CONSOLE — EXTENSION SDK
Plugin Architecture • Mode Extensions • Protocol Handlers • Dashboard Integrations

---

## 1. PURPOSE OF THIS DOCUMENT

This SDK defines how developers can extend the SSRF Command Console with:

- New scanning modes
- New protocol handlers
- New payload generators
- New classification engines
- New dashboard panels
- New API extensions

This document is the authoritative reference for building safe, stable, modular extensions.

---

## 2. EXTENSION PRINCIPLES

### 2.1 Stability

Extensions must remain compatible across MINOR and PATCH releases.

### 2.2 Isolation

Extensions must not:

- Modify core modules
- Override built‑in modes
- Patch global state

### 2.3 Determinism

Extensions must:

- Produce deterministic results
- Emit consistent logs
- Follow classification rules

### 2.4 Security

Extensions must:

- Never leak secrets
- Never bypass sandboxing
- Never perform unauthorized network calls

---

## 3. EXTENSION TYPES

### 3.1 Mode Extensions

Add new SSRF scanning modes.

### 3.2 Protocol Handlers

Add support for new protocols:

gopher:// dict:// file:// ftp:// custom://

### 3.3 Payload Generators

Add new payload construction logic.

### 3.4 Classification Engines

Add new response classification logic.

### 3.5 Dashboard Extensions

Add new UI panels or visualizations.

### 3.6 API Extensions

Add new endpoints under:

/api/ext/<extension_id>

---

## 4. DIRECTORY STRUCTURE FOR EXTENSIONS

Extensions must follow this structure:

extensions/ <extension_id>/ init.py manifest.json mode.py (optional) protocol.py (optional) payloads.py (optional) classifier.py (optional) api.py (optional) dashboard/ panel.json (optional) panel.js (optional)

---

## 5. MANIFEST FORMAT

Each extension must include a `manifest.json`:

```json
{
  "id": "custom_mode_pack",
  "name": "Custom Mode Pack",
  "version": "1.0.0",
  "author": "Your Name",
  "description": "Adds custom SSRF scanning modes.",
  "entrypoints": {
    "modes": ["mode.CustomMode"],
    "protocols": ["protocol.CustomProtocol"],
    "classifiers": ["classifier.CustomClassifier"],
    "api": ["api.router"],
    "dashboard": ["dashboard/panel.json"]
  }
}

## 6. CREATING A NEW MODE

### 6.1 Mode Class Template
from app.core.base_mode import BaseMode

class CustomMode(BaseMode):
    id = "custom_mode"
    name = "Custom Mode"
    description = "A custom SSRF scanning mode."
    category = "advanced"

    async def build_payload(self, target: str) -> dict:
        return {"url": target + "?custom=1"}

    async def execute(self, payload: dict) -> dict:
        return await self.http.fetch(payload["url"])

    def classify_response(self, response) -> str:
        if response.status_code == 200:
            return "success"
        return "unknown"

### 6.2 Registration
Modes are auto‑registered via the manifest.

## 7. CREATING A NEW PROTOCOL HANDLER

### 7.1 Protocol Template
class CustomProtocol:
    scheme = "custom"

    async def fetch(self, url: str):
        # Implement protocol logic here
        return {
            "status_code": 200,
            "body": "custom protocol response"
        }

### 7.2 Registration
Add to manifest under protocols

## 8. CREATING A CUSTOM CLASSIFIER

### 8.1 Classifier Template

class CustomClassifier:
    id = "custom_classifier"

    def classify(self, response) -> str:
        if "forbidden" in response.body.lower():
            return "filtered"
        return "unknown"

### 8.2 Registration
Add to manifest under classifiers

##9. EXTENDING the API
### 9.1 API Router Template
from fastapi import APIRouter

router = APIRouter(prefix="/api/ext/custom")

@router.get("/ping")
async def ping():
    return {"status": "ok"}

### 9.2 Registration
Add to manifest under api.

## 10. EXTENDING THE DASHBOARD

### 10.1 Panel Manifest
{
  "id": "custom_panel",
  "name": "Custom Panel",
  "component": "custom-panel.js",
  "route": "/dashboard/custom"
}

### 10.2 Panel Script (Example)
export default {
  mounted() {
    console.log("Custom panel loaded");
  }
}

## 11. SECURITY REQUIREMENTS FOR EXTENSIONS
### 11.1 Forbidden Behaviors
Extensions must NOT:
• 	Execute shell commands
• 	Access local filesystem without permission
• 	Perform unrestricted outbound network calls
• 	Modify core application state
### 11.2 Required Behaviors
Extensions MUST:
• 	Sanitize all inputs
• 	Validate all URLs
• 	Use built‑in HTTP client wrappers
• 	Emit logs using the core logger

## 12. TESTING EXTENSIONS
### 12.1 Required Tests
Each extension must include:
• 	Mode tests
• 	Protocol tests
• 	Classifier tests
• 	API tests
• 	Dashboard tests (if applicable)

###12.2 Test Directory Structure
extensions/<id>/tests/
    test_mode.py
    test_protocol.py
    test_classifier.py
    test_api.py

## 13. VERSIONING & COMPATIBILITY
### 13.1 Extension Versioning
Extensions must use SemVer:

MAJOR.MINOR.PATCH

### 13.2 Compatibility Rules
• 	MINOR/PATCH updates must remain backward‑compatible
• 	MAJOR updates may break compatibility

## 14. APPENDIX — ESCAPED FENCING EXAMPLES

### 14.1 Escaped Code Block

python print("extension loaded")

### 14.2 Escaped JSON Block

json {"extension": "custom_mode_pack"}
```
