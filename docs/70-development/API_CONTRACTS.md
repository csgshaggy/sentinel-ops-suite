# API_CONTRACTS.md

SSRF COMMAND CONSOLE — API CONTRACTS
Stable Interfaces, Deterministic Schemas, Backward‑Compatible Guarantees

---

## 1. PURPOSE OF THIS DOCUMENT

This document defines the **formal API contracts** for the SSRF Command Console backend.
It ensures:

- Predictable request/response schemas
- Backward‑compatible evolution
- Clear error semantics
- Stable integration points
- Deterministic behavior across versions

This is the authoritative source for all API‑level guarantees.

---

## 2. VERSIONING & STABILITY

### 2.1 Contract Versioning

Each API contract is tied to the project’s SemVer version:

MAJOR.MINOR.PATCH

- **MAJOR** — breaking API changes
- **MINOR** — new endpoints or fields (non‑breaking)
- **PATCH** — bug fixes, clarifications, documentation updates

### 2.2 Stability Guarantees

Once an endpoint is marked **stable**, the following rules apply:

- Fields are never removed without a MAJOR version bump
- Field types never change
- Required fields remain required
- Optional fields remain optional
- Error codes remain consistent

### 2.3 Deprecation Policy

Deprecated fields or endpoints must include:

- A deprecation notice in the response
- Documentation in CHANGELOG.md
- Removal only in the next MAJOR release

---

## 3. BASE URL & GENERAL RULES

### 3.1 Base URL

/api/v1

### 3.2 Content Types

All endpoints use:
Content-Type: application/json

### 3.3 Authentication (Future)

Reserved for:

- API keys
- Session tokens
- RBAC roles

Currently **no authentication** is required in local mode.

---

## 4. ENDPOINT CONTRACTS

Below are the canonical schemas for all stable endpoints.

---

# 4.1 `/api/v1/modes` — List Available Modes

### Method

GET

### Request

No parameters.

### Response Schema

```json
{
  "modes": [
    {
      "id": "direct_fetch",
      "name": "Direct Fetch Mode",
      "description": "Raw URL fetch via backend handler.",
      "category": "core",
      "stable": true
    }
  ]
}

## Error Codes
None.

## 4.2  — /api/v1/mode/{mode_id}/execute - Execute a Mode
Method

POST

Request Schema

{
  "target": "http://127.0.0.1",
  "options": {
    "headers": {
      "User-Agent": "SSRF-Console"
    },
    "timeout": 5000
  }
}

## Required Fields
• 	 — string
• 	 — object (may be empty)

## Response Schema
{
  "mode": "direct_fetch",
  "target": "http://127.0.0.1",
  "timestamp": "2026-03-17T14:32:10Z",
  "result": {
    "status_code": 200,
    "response_time_ms": 42,
    "headers": {
      "Server": "nginx"
    },
    "body": "<html>...</html>",
    "classification": "success"
  }
}

## Error Schema
 {
  "error": "InvalidTarget",
  "message": "Target URL is malformed.",
  "details": {}
}

## Error Codes
|Code  		|Meaning
|InvalidTarget  |URL malformed or unsupported  |
|ModeNotFound 	|Invalid mode_id  |
|ExecutionError |Mode crashed or failed  |
|Timeout        |Target did not respond  |

## 4.3 /api/v1/history - List Past Executions

	Method : GET
## Response Schema
{
  "entries": [
    {
      "id": "a1b2c3",
      "mode": "direct_fetch",
      "target": "http://127.0.0.1",
      "timestamp": "2026-03-17T14:32:10Z",
      "classification": "success"
    }
  ]
}

## 4.4 /api/v1/history/{id}  - Retrieve a Specific function

METHOD: GET

### Response Schema

{
  "id": "a1b2c3",
  "mode": "direct_fetch",
  "target": "http://127.0.0.1",
  "timestamp": "2026-03-17T14:32:10Z",
  "result": {
    "status_code": 200,
    "response_time_ms": 42,
    "headers": {},
    "body": "",
    "classification": "success"
  }
}

### Error Codes

CODE 		| MEANING
HistoryNotFound | No entry with that ID

### 4.5 /api/v1/health - Health Check
METHOD: GET


### Response Schema
{
  "status": "ok",
  "timestamp": "2026-03-17T14:32:10Z"
}

## ERROR CONTRACTS

### 5.1 Standard Error Envelope
All errors follow this schema:
{
  "error": "ErrorCode",
  "message": "Human-readable explanation.",
  "details": {}
}

### 5.2 Error Code Registry
Error Code 	| Meaning
InvalidTarget	| Target URL malformed
ModeNotFound	| Unknown mode
ExecutionError	| Mode crashed
Timeout		| Target unresponsive
HistoryNotFound | No matching history entry
InternalError 	| Unexpected backend failure

## 6 FIELD TYPE DEFINITIONS

### 6.1 Classification Types
success
timeout
connection_error
protocol_error
filtered
unknown

### 6.2 Mode Categories
core
advanced
experimental

### 6.3 Timestamp Format
ISO 8601 UTC

## 7 BACKWARD-COMPATIBILITY RULES

### 7.1 Allowed Without Major Version Bump
• 	Adding new optional fields
• 	Adding new endpoints
• 	Adding new classification types
• 	Adding new mode categories
### 7.2 Requires Major Version Bump
• 	Removing fields
• 	Changing field types
• 	Changing required → optional
• 	Changing optional → required
• 	Removing endpoints
• 	Renaming endpoints

## 8. FUTURE CONTRACT EXTENSIONS
Planned additions:
• 	Authentication contract
• 	RBAC contract
• 	Plugin/extension API contract
• 	Streaming response contract
• 	WebSocket event contract

## 9. APPENDIX — ESCAPED FENCING EXAMPLES
### 9.1 Escaped Code Block

json {"example": true}

### 9.2 Escaped Error Example
json {"error": "InvalidTarget"}
```
