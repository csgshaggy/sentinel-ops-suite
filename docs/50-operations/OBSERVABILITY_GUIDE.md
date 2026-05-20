# OBSERVABILITY_GUIDE.md

SSRF COMMAND CONSOLE — OBSERVABILITY GUIDE
Logging • Metrics • Tracing • Debugging • Forensic Insight

---

## 1. PURPOSE OF THIS DOCUMENT

This guide defines the **observability model** for the SSRF Command Console.
It ensures that operators, developers, and incident responders can:

- Understand system behavior
- Trace mode execution
- Debug anomalies
- Monitor performance
- Detect regressions
- Maintain forensic visibility

This is the authoritative reference for logs, metrics, tracing, and diagnostic workflows.

---

## 2. OBSERVABILITY PRINCIPLES

### 2.1 Deterministic

Observability output must be:

- Predictable
- Structured
- Machine‑parsable

### 2.2 Minimal but Sufficient

Logs must contain enough detail for forensic analysis without overwhelming operators.

### 2.3 Secure

- Never log secrets
- Never log full response bodies unless in DEBUG mode
- Never log sensitive internal URLs unless explicitly allowed

### 2.4 Mode‑Aware

Each scanning mode must emit:

- Start event
- End event
- Classification result
- Timing metrics

---

## 3. LOGGING MODEL

### 3.1 Log Levels

DEBUG — internal details, payloads, raw responses
INFO — mode execution lifecycle events
WARNING — recoverable issues or unexpected conditions
ERROR — failures during execution that prevent completion
CRITICAL — unrecoverable failures requiring operator attention

### 3.2 Log Format

[timestamp] [level] [module] message

### 3.3 Required Log Fields

Every log entry must include:

- Timestamp (UTC ISO 8601)
- Log level
- Module name
- Mode ID (if applicable)
- Target (sanitized)
- Classification (if applicable)

### 3.4 Logging Rules

- Do not log secrets
- Do not log full response bodies unless DEBUG
- Always log classification results
- Always log execution start/end
- Always log timeouts and connection errors

---

## 4. METRICS MODEL

### 4.1 Metric Categories

ssrf.mode.execution_time_ms
ssrf.mode.success_count
ssrf.mode.error_count
ssrf.mode.timeout_count
ssrf.api.request_count
ssrf.api.error_count
ssrf.system.memory_usage_mb
ssrf.system.cpu_percent

### 4.2 Metric Dimensions

Each metric should include:

- mode_id
- classification
- status_code (if applicable)
- protocol
- target_type (internal, external, encoded, rebinding, etc.)

### 4.3 Metric Export Formats

Supported:

- JSON
- Prometheus text format (future)
- In‑memory counters

---

## 5. TRACING MODEL

### 5.1 Trace Structure

Each mode execution generates a trace with:
trace_id mode_id
target start_timestamp
end_timestamp
duration_ms
classification error_details (optional)

### 5.2 TRACE Events

mode.start
mode.payload_built
mode.request_sent
mode.response_received
mode.classified
mode.completed

### 5.3 Trace Storage

- In‑memory ring buffer
- Optional persistent storage (future)

---

## 6. DEBUGGING WORKFLOWS

### 6.1 Debugging a Failed Mode Execution

Steps:

1. Enable DEBUG logging
2. Re‑run the mode
3. Inspect payload generation logs
4. Inspect raw response logs
5. Inspect classification logic
6. Compare with known patterns

### 6.2 Debugging Timeouts

Check:

- DNS resolution logs
- TCP handshake logs
- Response timing metrics
- Mode‑specific timeout thresholds

### 6.3 Debugging Unexpected Classifications

Verify:

- Response body patterns
- Status code mapping
- Redirect behavior
- Error envelope structure

---

## 7. ANOMALY DETECTION

### 7.1 Timing Anomalies

Flag when:

- Response time deviates > 3× median
- Mode execution time spikes
- DNS resolution time spikes

### 7.2 Classification Anomalies

Flag when:

- A mode suddenly produces new classifications
- A mode produces inconsistent classifications for identical targets

### 7.3 Response Pattern Anomalies

Flag when:

- Response size changes significantly
- Header sets change unexpectedly
- Protocol behavior changes

---

## 8. HISTORY & FORENSIC RECORDS

### 8.1 History Entry Structure

id mode target timestamp classification result_summary trace_id

### 8.2 Forensic Requirements

History entries must:

- Be immutable
- Include classification
- Include timing
- Include sanitized target
- Link to trace data

---

## 9. OBSERVABILITY FOR MODE AUTHORS

### 9.1 Required Emissions

Each mode must emit:

- mode.start
- mode.payload_built
- mode.request_sent
- mode.response_received
- mode.classified
- mode.completed

### 9.2 Optional Emissions

- Protocol‑specific events
- Retry events
- Redirect events

### 9.3 Forbidden Emissions

- Secrets
- Raw credentials
- Sensitive internal URLs

---

## 10. OPERATOR DASHBOARD OBSERVABILITY

### 10.1 Dashboard Must Display

- Mode execution timeline
- Response time
- Classification
- Status code
- Error details
- Raw response (optional)

### 10.2 Dashboard Should Display

- Trace events
- Metrics summary
- Historical comparison

### 10.3 Dashboard Future Enhancements

- Live metrics
- Prometheus export
- Flamegraph‑style mode tracing

---

## 11. APPENDIX — ESCAPED FENCING EXAMPLES

### 11.1 Escaped Log Example

```markdown
INFO [2026-03-17T14:32:10Z] [direct_fetch] Completed with classification=success

### 11.2 Escaped JSON Example

json {"metric": "ssrf.mode.success_count", "value": 42}
```
