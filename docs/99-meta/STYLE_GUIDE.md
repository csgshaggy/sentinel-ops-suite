# STYLE_GUIDE.md
SSRF COMMAND CONSOLE — STYLE GUIDE  
Consistent Conventions, Predictable Structure, Operator‑Grade Clarity

---

## 1. PURPOSE OF THIS DOCUMENT
This guide defines the **coding, documentation, naming, and structural conventions** used across the SSRF Command Console project.

Its goals:
- Ensure consistency across all modules  
- Reduce cognitive load for contributors  
- Maintain predictable patterns for operators  
- Support long‑term maintainability  
- Enable clean, modular extension of modes and features  

This is the authoritative reference for all style decisions.

---

## 2. PYTHON CODE STYLE

### 2.1 Formatting
The project uses:

ruff black (optional) mypy


### 2.2 General Rules
- 4‑space indentation  
- No trailing whitespace  
- Max line length: 100 characters  
- Use type hints everywhere  
- Prefer explicit imports over wildcard imports  
- Avoid deeply nested logic; refactor into helpers  

### 2.3 Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Modules | snake_case | `mode_registry.py` |
| Classes | PascalCase | `DirectFetchMode` |
| Functions | snake_case | `build_payload()` |
| Variables | snake_case | `response_time_ms` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_TIMEOUT_MS` |

### 2.4 Error Handling
- Never swallow exceptions silently  
- Use structured error classes  
- Wrap external calls with explicit error boundaries  
- Return consistent error envelopes to the API layer  

---

## 3. MODE AUTHORING STYLE

### 3.1 Required Structure
Each mode must define:

class ModeName(BaseMode): id = "mode_id" name = "Human‑Readable Name" description = "Short description." category = "core|advanced|experimental"


### 3.2 Required Methods

build_payload() execute() classify_response()


### 3.3 Mode Behavior Rules
- Never raise raw exceptions  
- Always return structured results  
- Always classify responses deterministically  
- Never perform real external network calls in tests  

---

## 4. LOGGING STYLE

### 4.1 Log Levels

DEBUG — internal details 
INFO — mode execution events 
WARNING — recoverable issues 
ERROR — failures 
CRITICAL — unrecoverable failures

### 4.2 Log Format
 [LEVEL] [timestamp] [module] message

### 4.3 Logging Rules
- Never log secrets  
- Never log full response bodies unless in DEBUG mode  
- Always log classification results  
- Always log mode execution start/end  

---

## 5. API STYLE

### 5.1 JSON Field Naming
Use snake_case for all API fields:

response_time_ms status_code classification


### 5.2 Response Envelope
All responses must follow:

{ "error": "ErrorCode", "message": "Human-readable explanation.", "details": {} }



---

## 6. DIRECTORY STRUCTURE STYLE

### 6.1 Core Layout
app/ modes/ api/ utils/ core/ tests/ docs/ scripts/


### 6.2 Mode Directory Rules
- One file per mode  
- Name matches mode ID  
- No cross‑mode imports unless explicitly shared  

---

## 7. DOCUMENTATION STYLE

### 7.1 Markdown Rules
- Use `#` for top‑level headers  
- Use fenced code blocks for all examples  
- Avoid inline HTML  
- Keep line length under 100 chars  
- Use consistent section ordering  

### 7.2 Required Sections for Docs
Each doc should include:
- Purpose  
- Usage  
- Examples  
- Notes  
- Appendix (if needed)  

---

## 8. COMMENTING STYLE

### 8.1 When to Comment
Comment when:
- Logic is non‑obvious  
- A workaround is required  
- A design decision needs justification  

### 8.2 When NOT to Comment
Do not comment:
- Obvious code  
- Style violations  
- Dead code (remove instead)  

### 8.3 Docstring Format
Use triple‑quoted docstrings:
```python
def build_payload(url: str) -> dict:
    """
    Build the payload for the mode.

    Args:
        url: Target URL.

    Returns:
        A dictionary representing the payload.
    """

## 9. TEST STYLE

### 9.1 Naming
test_<functionality>.py

### 9.2 Assertions
Prefer explicit assertions
• 	Avoid asserting on side effects unless necessary

### 9.3 Test Structure
arrange
act
assert

## 10. PERFORMANCE & RESOURCE STYLE

### 10.1 Timeouts
• 	Default timeout: 5000 ms
• 	Never block indefinitely

### 10.2 Memory Rules
• 	Avoid large in‑memory buffers
• 	Stream large responses when possible

## 11. APPENDIX - ESCAPED FENCING EXAMPLES

### 11.1 Escaped Code Block
python def example(): pass

### 11.2 Escaped JSON
json {"style": "guide"}

