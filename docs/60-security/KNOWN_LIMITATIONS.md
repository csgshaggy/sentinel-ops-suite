# KNOWN_LIMITATIONS.md

SSRF COMMAND CONSOLE — KNOWN LIMITATIONS
Current Constraints • Edge Cases • Unsupported Features • Future Improvements

---

## 1. PURPOSE OF THIS DOCUMENT

This document provides a transparent overview of the current limitations of the SSRF Command Console.
It helps operators, developers, and contributors understand:

- What the system cannot do yet
- Where behavior is intentionally restricted
- Known edge cases and constraints
- Areas planned for future improvement

This is the authoritative reference for all known limitations.

---

## 2. ARCHITECTURAL LIMITATIONS

### 2.1 No Full Browser Emulation

The console does not emulate:

- JavaScript execution
- DOM rendering
- Cookie persistence
- Browser‑level redirects

**Reason:** Out of scope for SSRF analysis.

---

### 2.2 No Stateful Session Management (Yet)

The system does not maintain:

- Session cookies
- Auth tokens
- Stateful login flows

**Reason:** SSRF payloads are typically stateless.

---

### 2.3 Limited Protocol Coverage

Supported protocols are intentionally restricted.

Unsupported protocols include:

- `smb://`
- `ldap://`
- `nfs://`
- `rtsp://`
- `telnet://`

**Reason:** Security and complexity concerns.

---

### 2.4 No Built‑In Proxy Support

The console does not route requests through:

- HTTP proxies
- SOCKS proxies
- Burp/ZAP

**Reason:** Avoids altering SSRF behavior.

---

## 3. MODE SYSTEM LIMITATIONS

### 3.1 Modes Cannot Modify Global State

Modes are sandboxed and cannot:

- Change configuration
- Modify other modes
- Alter global registries

**Reason:** Ensures safety and determinism.

---

### 3.2 No Cross‑Mode Communication

Modes cannot:

- Share internal state
- Pass data to each other
- Chain execution

**Reason:** Prevents hidden coupling.

---

### 3.3 Limited Parallel Execution

Modes execute sequentially unless explicitly parallelized.

**Reason:** Prevents resource contention and timing noise.

---

## 4. NETWORK LIMITATIONS

### 4.1 DNS Behavior Depends on Host System

DNS resolution may vary due to:

- Local resolver caching
- Split‑horizon DNS
- DNS rebinding protections

**Reason:** Console does not override system DNS.

---

### 4.2 No IPv6‑Only Support

IPv6 is partially supported but not fully validated.

**Reason:** Most SSRF targets are IPv4‑centric.

---

### 4.3 No Raw Socket Access

The console cannot:

- Craft raw TCP packets
- Perform SYN scans
- Manipulate low‑level network flags

**Reason:** Out of scope and unsafe for general users.

---

## 5. OBSERVABILITY LIMITATIONS

### 5.1 No Distributed Tracing

Traces are local only.

**Reason:** Avoids external dependencies.

---

### 5.2 Limited Metrics Export

Metrics are not yet exported to:

- Prometheus
- Grafana
- Cloud monitoring systems

**Reason:** Future enhancement.

---

### 5.3 Log Volume Can Grow Quickly

Verbose logging may produce large log files.

**Reason:** High‑fidelity forensic logging.

---

## 6. DASHBOARD LIMITATIONS

### 6.1 No Real‑Time Streaming

Dashboard updates are not live‑streamed.

**Reason:** Avoids WebSocket complexity.

---

### 6.2 Limited Mobile Support

Dashboard is optimized for desktop use.

**Reason:** Operator workflows require large displays.

---

### 6.3 No Built‑In Dark Mode (Yet)

UI theme is static.

**Reason:** Planned for future UI overhaul.

---

## 7. API LIMITATIONS

### 7.1 No API Authentication (Local Mode)

The API is unauthenticated in local mode.

**Reason:** Simplifies development and training.

---

### 7.2 No Rate Limiting

API does not enforce:

- Per‑client limits
- Burst throttling

**Reason:** Local‑only design assumption.

---

### 7.3 No Streaming Responses

All responses are buffered.

**Reason:** Simplifies mode execution pipeline.

---

## 8. EXTENSION SYSTEM LIMITATIONS

### 8.1 No Hot Reloading

Extensions require a restart to load.

**Reason:** Ensures clean state and predictable behavior.

---

### 8.2 Limited UI Extension API

Dashboard extensions cannot:

- Modify core panels
- Override built‑in components

**Reason:** Prevents UI instability.

---

### 8.3 No Extension Sandboxing Beyond Python

Extensions run in Python sandbox only.

**Reason:** Avoids multi‑language complexity.

---

## 9. TESTING LIMITATIONS

### 9.1 No Full Network Simulation

Tests rely on:

- Mocks
- Fixtures
- Simulated responses

**Reason:** Prevents accidental real‑world scanning.

---

### 9.2 Limited Performance Testing in CI

CI does not run full performance benchmarks.

**Reason:** Performance tests require stable hardware.

---

## 10. FUTURE IMPROVEMENTS (PLANNED)

### 10.1 Planned Enhancements

- Full IPv6 support
- Prometheus metrics export
- WebSocket‑based live dashboard updates
- Dark mode UI
- Proxy support
- Advanced protocol handlers
- Mode chaining
- Distributed tracing

---

## 11. APPENDIX — ESCAPED FENCING EXAMPLES

### 11.1 Escaped Code Block

```markdown
limitation: "no proxy support"

### 11.2 Escaped JSON Block

json {"known_limitation": "no_ipv6_only_support"}
```
