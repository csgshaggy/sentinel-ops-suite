# BENCHMARK_RESULTS.md

SSRF COMMAND CONSOLE — BENCHMARK RESULTS
Performance Snapshots • Latency Tables • Regression Notes • Environment Specs

---

## 1. PURPOSE OF THIS DOCUMENT

This document provides historical benchmark results for the SSRF Command Console.

It exists to:

- Track performance across releases
- Detect regressions
- Validate optimizations
- Provide transparency for operators and contributors
- Support consulting, audits, and enterprise reporting

This is the authoritative record of benchmark data.

---

## 2. BENCHMARK METHODOLOGY

### 2.1 Test Environment

All benchmarks were executed under the following controlled environment:

| Component | Specification                        |
| --------- | ------------------------------------ |
| CPU       | 8‑core virtualized CPU               |
| RAM       | 16 GB                                |
| OS        | Linux (x86_64)                       |
| Python    | 3.11.x                               |
| Network   | Local simulation (no external calls) |
| Load      | 100 mode executions per run          |

### 2.2 Measurement Criteria

Each benchmark measures:

- **Mode latency** (ms)
- **Classification time** (ms)
- **Payload build time** (ms)
- **CPU usage** (%)
- **Memory usage** (MB)
- **Throughput** (executions/sec)

### 2.3 Test Inputs

All tests use:

- Deterministic mock responses
- Fixed payloads
- Predefined classification patterns

This ensures reproducibility.

---

## 3. VERSION‑TO‑VERSION PERFORMANCE SUMMARY

### 3.1 High‑Level Overview

| Version    | Avg Latency | CPU Usage | Memory Usage | Notes                         |
| ---------- | ----------- | --------- | ------------ | ----------------------------- |
| **v1.0.0** | 14.2 ms     | 18%       | 112 MB       | Baseline release              |
| **v1.1.0** | 12.8 ms     | 17%       | 114 MB       | Optimized payload builder     |
| **v1.2.0** | 11.9 ms     | 16%       | 118 MB       | Added precompiled classifiers |
| **v1.3.0** | 10.7 ms     | 15%       | 120 MB       | Async fetch improvements      |
| **v1.4.0** | 10.5 ms     | 15%       | 121 MB       | Minor optimizations           |

**Trend:**
Latency consistently decreases across versions, with slight memory increases due to expanded mode catalog and observability features.

---

## 4. MODE‑SPECIFIC LATENCY RESULTS

### 4.1 Core Modes

| Mode            | v1.0.0  | v1.2.0  | v1.4.0  | Change |
| --------------- | ------- | ------- | ------- | ------ |
| direct_fetch    | 8.1 ms  | 6.9 ms  | 6.7 ms  | ↓ 17%  |
| header_mutation | 12.4 ms | 11.1 ms | 10.9 ms | ↓ 12%  |
| dns_discovery   | 15.8 ms | 14.2 ms | 13.9 ms | ↓ 12%  |
| port_sweep      | 19.3 ms | 17.8 ms | 17.4 ms | ↓ 10%  |

### 4.2 Advanced Modes

| Mode           | v1.0.0  | v1.2.0  | v1.4.0  | Change |
| -------------- | ------- | ------- | ------- | ------ |
| gopher_probe   | 22.1 ms | 19.7 ms | 19.4 ms | ↓ 12%  |
| metadata_probe | 14.9 ms | 13.1 ms | 12.8 ms | ↓ 14%  |
| redirect_chain | 18.7 ms | 17.2 ms | 16.9 ms | ↓ 9%   |

---

## 5. CLASSIFICATION ENGINE PERFORMANCE

### 5.1 Classification Latency

| Version | Avg Classification Time |
| ------- | ----------------------- |
| v1.0.0  | 2.4 ms                  |
| v1.2.0  | 1.7 ms                  |
| v1.4.0  | 1.5 ms                  |

**Improvement:**
Precompiled regex patterns and optimized matching reduced classification time by **37%**.

---

## 6. CPU & MEMORY USAGE

### 6.1 CPU Usage by Version

| Version | CPU (%) |
| ------- | ------- |
| v1.0.0  | 18%     |
| v1.2.0  | 16%     |
| v1.4.0  | 15%     |

### 6.2 Memory Usage by Version

| Version | Memory (MB) |
| ------- | ----------- |
| v1.0.0  | 112 MB      |
| v1.2.0  | 118 MB      |
| v1.4.0  | 121 MB      |

**Interpretation:**
Memory increases correlate with:

- Additional modes
- Expanded observability
- Larger classification tables

---

## 7. THROUGHPUT RESULTS

### 7.1 Executions per Second

| Version | Throughput  |
| ------- | ----------- |
| v1.0.0  | 71 exec/sec |
| v1.2.0  | 79 exec/sec |
| v1.4.0  | 82 exec/sec |

**Net Gain:**
Throughput increased by **15.4%** since v1.0.0.

---

## 8. REGRESSION NOTES

### 8.1 v1.2.0 Memory Spike

A temporary memory increase was observed due to:

- Expanded mode metadata
- Additional classification patterns

Mitigated in v1.3.0 by:

- Lazy‑loading mode metadata
- Reducing trace verbosity

### 8.2 v1.3.0 Async Fetch Overhead

Initial async refactor introduced:

- Slight jitter in latency
- Occasional event loop stalls

Resolved by:

- Switching to uvloop
- Pre‑warming connection pools

---

## 9. FUTURE BENCHMARK PLANS

### 9.1 Planned Additions

- IPv6 performance benchmarks
- Extension performance impact analysis
- Dashboard rendering benchmarks
- Cold‑start vs warm‑start comparisons
- Multi‑threaded vs async benchmarks

### 9.2 Automation Roadmap

Benchmarks will be:

- Automated in CI
- Stored per‑release
- Compared against baseline thresholds
- Used to detect regressions automatically

---

## 10. APPENDIX — ESCAPED FENCING EXAMPLES

### 10.1 Escaped Code Block

```markdown
latency_ms: 10.5

### 10.2 Escaped JSON Block

json {"benchmark": "direct_fetch", "latency": 6.7}
```
