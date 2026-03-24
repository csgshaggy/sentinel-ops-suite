# GLOSSARY.md

SSRF COMMAND CONSOLE — GLOSSARY
Terminology • Concepts • Internal Vocabulary • Mode Semantics

---

## 1. PURPOSE OF THIS DOCUMENT

This glossary defines all key terms used throughout the SSRF Command Console project.
It ensures consistent understanding across:

- Operators
- Developers
- Contributors
- Auditors
- Trainees

This is the authoritative reference for all terminology.

---

## 2. CORE SSRF TERMINOLOGY

### **SSRF (Server-Side Request Forgery)**

A vulnerability where an attacker forces a backend server to make unintended network requests.

### **Target**

The URL or endpoint the console attempts to reach during a mode execution.

### **Payload**

The constructed request sent to the backend fetcher or protocol handler.

### **Response**

The returned data from the target, including:

- Status code
- Headers
- Body
- Timing

### **Classification**

The console’s interpretation of the response:

success timeout connection_error protocol_error filtered unknown

### **Internal Target**

A target that resolves to:

- 127.0.0.0/8
- 10.0.0.0/8
- 172.16.0.0/12
- 192.168.0.0/16
- Link-local or metadata IPs

### **External Target**

Any target outside internal ranges.

---

## 3. MODE TERMINOLOGY

### **Mode**

A modular scanning strategy that defines:

- Payload generation
- Execution logic
- Response classification

### **Mode ID**

A unique identifier for a mode (e.g., `direct_fetch`, `dns_discovery`).

### **Mode Category**

core
advanced
experimental

### **Mode Registry**

The system responsible for:

- Loading modes
- Validating mode definitions
- Exposing mode metadata

### **Mode Execution**

The full lifecycle of:

1. Payload build
2. Request dispatch
3. Response capture
4. Classification
5. Logging & metrics

---

## 4. PROTOCOL TERMINOLOGY

### **Protocol Handler**

A component that implements support for a specific scheme:

http:// https:// gopher:// dict:// file:// custom://

### **Scheme**

The prefix of a URL indicating protocol type.

### **Fetcher**

The internal HTTP client or protocol handler responsible for executing requests.

---

## 5. OBSERVABILITY TERMINOLOGY

### **Log Event**

A structured record of system activity.

### **Trace**

A timeline of events for a single mode execution.

### **Trace ID**

A unique identifier linking logs, metrics, and history entries.

### **Metric**

A numerical measurement of system behavior:

- Latency
- Error count
- Timeout count
- CPU usage

### **History Entry**

A stored record of a past mode execution.

---

## 6. SECURITY TERMINOLOGY

### **Trust Boundary**

A point where data crosses from one security domain to another.

### **Sandbox**

A restricted execution environment for modes or protocol handlers.

### **Filtered Response**

A response indicating:

- Firewall block
- WAF block
- ACL restriction
- Proxy filtering

### **Rebinding**

DNS behavior where a hostname resolves to different IPs over time.

---

## 7. DASHBOARD TERMINOLOGY

### **Execution Timeline**

A visual representation of mode execution events.

### **Panel**

A dashboard component that displays:

- Metrics
- Logs
- History
- Mode details

### **Operator View**

The UI layer designed for real-time SSRF analysis.

---

## 8. API TERMINOLOGY

### **API Contract**

A stable definition of:

- Request schemas
- Response schemas
- Error envelopes

### **Error Envelope**

The standardized error format:

```json
{
  "error": "ErrorCode",
  "message": "Human-readable explanation.",
  "details": {}
}

### Endpoint
A callable API route under /api/v1.

## 9. EXTENSION TERMINOLOGY
Extension
A plugin that adds:
• 	Modes
• 	Protocol handlers
• 	Classifiers
• 	API routes
• 	Dashboard panels

Manifest
A JSON file describing extension metadata and entrypoints.

Entrypoint
A class or module registered by an extension.

## 10. TESTING TERMINOLOGY
### Unit Test
Tests isolated logic with no I/O.

### Integration Test
Tests API, dashboard, and persistence layers.
### Mode Test
Tests mode behavior end-to-end.
### Regression Test
Prevents reintroduction of previously fixed bugs.

### Snapshot
A stored expected output used for regression detection.

##11. APPENDIX — ESCAPED FENCING EXAMPLES
### 11.1 Escaped Code Block

classification: success


### 11.2 Escaped JSON Block


json {"mode": "direct_fetch", "result": "success"}
```
