# API_VERSIONING_POLICY.md
SSRF COMMAND CONSOLE — API VERSIONING POLICY  
Stability Guarantees • Deprecation Rules • Version Evolution • Compatibility Strategy

---

## 1. PURPOSE OF THIS DOCUMENT
This document defines how the SSRF Command Console API evolves over time.  
It ensures:

- Predictable API changes  
- Backward‑compatible evolution  
- Safe deprecations  
- Clear upgrade paths  
- Stable integration for operators, extensions, and automation  

This is the authoritative reference for API versioning.

---

## 2. VERSIONING MODEL

### 2.1 Semantic Versioning
The API follows SemVer:

MAJOR.MINOR.PATCH


- **MAJOR** — breaking changes  
- **MINOR** — new features, backward‑compatible  
- **PATCH** — bug fixes, no behavior changes  

### 2.2 API Namespace Versioning
All API routes live under a versioned namespace:

/api/v1 
/api/v2 ...


Each namespace is **immutable** once released.

---

## 3. STABILITY GUARANTEES

### 3.1 Backward Compatibility
Within a major version:
- No fields are removed  
- No response formats change  
- No error envelopes change  
- No endpoints are renamed  
- No required fields become optional or vice‑versa  

### 3.2 Additive Changes Only (MINOR/PATCH)
Allowed changes:
- Adding new optional fields  
- Adding new endpoints  
- Adding new classification types (with fallback behavior)  
- Adding new metadata fields  

### 3.3 Forbidden Changes (MINOR/PATCH)
Not allowed:
- Removing fields  
- Changing field types  
- Changing endpoint behavior  
- Changing error codes  
- Changing required fields  

---

## 4. DEPRECATION POLICY

### 4.1 Deprecation Lifecycle
Deprecation follows a strict lifecycle:

1. **Mark as deprecated**  
   - Documented in CHANGELOG.md  
   - Warning added to API response metadata  
   - Warning added to API docs  

2. **Grace period**  
   - Minimum of **one full MAJOR version**  
   - Deprecated fields remain functional  

3. **Removal**  
   - Only in the next MAJOR release  
   - Documented in RELEASE_PROCESS.md  

### 4.2 Deprecation Warnings
Deprecated fields include:

```json
{
  "deprecated": true,
  "replacement": "new_field"
}

## 5. VERSION NEGOTIATION
### 5.1 Client‑Selected Version
Clients select API version via URL:
/api/v1/modes
/api/v2/modes

### 5.2 Default Version
If no version is specified:
• 	The console defaults to the latest stable version
• 	This behavior is documented and predictable
##$ 5.3 Extension Versioning
Extensions must:
• 	Declare their supported API versions in 
• 	Use namespaced routes under 
• 	Avoid breaking changes within their own version


## 6. BREAKING CHANGE POLICY
### 6.1 What Counts as a Breaking Change
A change is breaking if it:
• 	Removes a field
• 	Renames a field
• 	Changes a field type
• 	Changes response structure
• 	Changes error envelope format
• 	Removes an endpoint
• 	Changes required parameters
### 6.2 Breaking Change Release Rules
Breaking changes:
• 	Only allowed in MAJOR releases
• 	Must be documented in CHANGELOG.md
• 	Must include migration steps in UPGRADE_GUIDE.md
• 	Must include compatibility notes in RELEASE_PROCESS.md

## 7. VERSION EVOLUTION EXAMPLES
### 7.1 Adding a New Optional Field (Allowed)
Old:
{"id": "direct_fetch"}

New:

{"id": "direct_fetch", "category": "core"}


### 7.2 Removing a Field (Breaking)
Old:

{"mode": "direct_fetch", "timeout": 5000}

New:
{"mode": "direct_fetch"}

Requires MAJOR version bump.

## 8. API SUNSET POLICY
### 8.1 Sunset Timeline
When an API version is scheduled for removal:
• 	Announced in CHANGELOG.md
• 	Announced in RELEASE_PROCESS.md
• 	Minimum 12‑month notice
• 	Deprecated version remains functional until removal
### 8.2 Sunset Warnings
Responses include:
{
  "api_version": "v1",
  "sunset": "2027-01-01"
}

##  9. TESTING REQUIREMENTS
### 9.1 Version‑Specific Tests
Each API version must include:
• 	Contract tests
• 	Schema validation tests
• 	Error envelope tests
• 	Regression tests
### 9.2 Compatibility Tests
Before release:
• 	v1 and v2 must be tested side‑by‑side
• 	Extensions must be tested against both versions

## 10. EXTENSION VERSIONING RULES
### 10.1 Extension API Stability
Extensions must:
• 	Maintain backward compatibility within their own MAJOR version
• 	Declare supported API versions
### 10.2 Extension Migration
When a new API version is released:
• 	Extensions may continue using old version
• 	Migration is optional until sunset
• 	Extensions may support multiple versions simultaneously
## 11. APPENDIX — ESCAPED FENCING EXAMPLES
### 11.1 Escaped Code Block

api_version: "v1"

### 11.2 Escaped JSON Block

json {"deprecated": true, "replacement": "new_field"}

