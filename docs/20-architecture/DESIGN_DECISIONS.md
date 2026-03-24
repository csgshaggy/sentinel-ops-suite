# DESIGN_DECISIONS.md

SSRF COMMAND CONSOLE — DESIGN DECISIONS
Architectural Rationale • Tradeoffs • Constraints • Long‑Term Strategy

---

## 1. PURPOSE OF THIS DOCUMENT

This document explains _why_ the SSRF Command Console is designed the way it is.
It captures the architectural reasoning, tradeoffs, constraints, and long‑term considerations that shaped the system.

This is the authoritative reference for design intent.

---

## 2. HIGH‑LEVEL ARCHITECTURE DECISIONS

### 2.1 FastAPI as the Backend Framework

**Decision:** Use FastAPI for the backend API and mode execution orchestration.

**Reasons:**

- Async‑first architecture
- High performance
- Built‑in validation via Pydantic
- Clean routing model
- Excellent developer ergonomics
- Easy to extend with custom routers (extensions)

**Tradeoffs:**

- Requires async awareness
- Slightly more complex than Flask for beginners

---

### 2.2 Modular Mode Architecture

**Decision:** Each SSRF scanning mode is a self‑contained module implementing a shared BaseMode interface.

**Reasons:**

- Enables plugin‑style extensibility
- Allows independent development and testing
- Supports clean separation of scanning strategies
- Prevents cross‑mode coupling
- Enables dynamic discovery and registration

**Tradeoffs:**

- Requires strict interface discipline
- Slightly more boilerplate per mode

---

### 2.3 Unified Classification Engine

**Decision:** All modes must classify responses using a shared classification vocabulary.

**Reasons:**

- Consistent operator experience
- Enables cross‑mode comparison
- Simplifies dashboard logic
- Supports regression testing
- Prevents ambiguous or mode‑specific classifications

**Tradeoffs:**

- Some modes may need to map nuanced results into broader categories

---

### 2.4 Deterministic Observability Model

**Decision:** Use structured logs, traces, and metrics for every mode execution.

**Reasons:**

- Enables forensic analysis
- Supports debugging and anomaly detection
- Allows operators to understand execution flow
- Enables future Prometheus integration
- Supports regression detection

**Tradeoffs:**

- Slight overhead in logging
- Requires consistent event emission

---

## 3. SECURITY‑DRIVEN DESIGN DECISIONS

### 3.1 Strict Input Validation

**Decision:** All targets and payloads must be validated before execution.

**Reasons:**

- Prevents malformed URLs from crashing modes
- Prevents protocol confusion
- Ensures predictable behavior

---

### 3.2 Sandbox Execution Model

**Decision:** Modes and protocol handlers run in a restricted environment.

**Reasons:**

- Prevents extensions from accessing system resources
- Prevents arbitrary code execution
- Ensures safe plugin ecosystem

---

### 3.3 No Real External Network Calls in Tests

**Decision:** All tests must use mocks or simulated responses.

**Reasons:**

- Ensures deterministic test results
- Prevents accidental scanning of real systems
- Enables offline testing

---

## 4. PERFORMANCE‑DRIVEN DESIGN DECISIONS

### 4.1 Async I/O for All Network Operations

**Decision:** All fetch operations use async HTTP clients or async protocol handlers.

**Reasons:**

- High concurrency
- Low latency
- Efficient resource usage

---

### 4.2 Lightweight Response Handling

**Decision:** Avoid storing full response bodies unless necessary.

**Reasons:**

- Reduces memory usage
- Improves performance
- Prevents dashboard overload

---

### 4.3 Precompiled Patterns for Classification

**Decision:** Regex and pattern matching are precompiled.

**Reasons:**

- Faster classification
- Lower CPU usage
- More predictable performance

---

## 5. EXTENSIBILITY DECISIONS

### 5.1 Manifest‑Based Extension Loading

**Decision:** Extensions declare entrypoints in a JSON manifest.

**Reasons:**

- Predictable loading
- Easy validation
- No dynamic imports or unsafe reflection
- Clear compatibility boundaries

---

### 5.2 Namespaced API Extensions

**Decision:** All extension APIs mount under `/api/ext/<id>`.

**Reasons:**

- Prevents route collisions
- Makes debugging easier
- Keeps core API stable

---

### 5.3 Dashboard Panel Extensions

**Decision:** Dashboard panels are defined via JSON + JS components.

**Reasons:**

- Allows UI extensions without modifying core dashboard
- Supports custom operator workflows
- Enables vendor‑specific panels

---

## 6. TESTING & QUALITY DECISIONS

### 6.1 Strict Test Separation

**Decision:** Tests are separated into:

- unit
- integration
- modes
- regression

**Reasons:**

- Clear test intent
- Faster debugging
- Better CI performance

---

### 6.2 Snapshot‑Based Regression Testing

**Decision:** Use snapshots to detect behavioral drift.

**Reasons:**

- Prevents silent regressions
- Ensures classification stability
- Ensures mode output consistency

---

## 7. USER EXPERIENCE DECISIONS

### 7.1 Operator‑First Dashboard

**Decision:** Dashboard prioritizes clarity, speed, and forensic visibility.

**Reasons:**

- Operators need fast, actionable insights
- SSRF analysis requires timeline‑based visualization
- History and classification must be immediately visible

---

### 7.2 Minimal Configuration Requirements

**Decision:** Console works out‑of‑the‑box with defaults.

**Reasons:**

- Reduces onboarding friction
- Supports training environments
- Prevents misconfiguration

---

## 8. LONG‑TERM STRATEGIC DECISIONS

### 8.1 Treat Modes as a Platform

**Decision:** The mode system is designed for long‑term extensibility.

**Reasons:**

- Supports community contributions
- Enables vendor‑specific mode packs
- Allows rapid experimentation

---

### 8.2 API Stability as a Priority

**Decision:** API contracts evolve slowly and predictably.

**Reasons:**

- Prevents breaking clients
- Supports automation
- Enables third‑party integrations

---

### 8.3 Observability as a First‑Class Feature

**Decision:** Logs, metrics, and traces are core to the system.

**Reasons:**

- SSRF analysis is inherently forensic
- Operators need deep visibility
- Debugging requires full execution context

---

## 9. APPENDIX — ESCAPED FENCING EXAMPLES

### 9.1 Escaped Code Block

```markdown
decision: "async-first architecture"

### 9.2 Escaped JSON Block

json {"design": "modular_modes", "reason": "extensibility"}
```
