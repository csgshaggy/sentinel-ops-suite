# PERFORMANCE_GUIDE.md
SSRF COMMAND CONSOLE — PERFORMANCE GUIDE  
Latency • Throughput • Benchmarks • Optimization • Regression Detection

---

## 1. PURPOSE OF THIS DOCUMENT
This guide defines the performance expectations, benchmarking methodology, tuning strategies, and regression‑detection workflows for the SSRF Command Console.

It ensures:
- Predictable performance across releases  
- Repeatable benchmarking  
- Clear expectations for mode latency  
- Identification of bottlenecks  
- Consistent operator experience  
- Early detection of performance regressions  

---

## 2. PERFORMANCE PRINCIPLES

### 2.1 Deterministic Behavior
Performance should be:
- Stable  
- Predictable  
- Measurable  
- Reproducible  

### 2.2 No Hidden Work
Modes must not:
- Perform unnecessary retries  
- Perform redundant DNS lookups  
- Perform hidden network calls  

### 2.3 Fail Fast
Timeouts must be enforced consistently to avoid blocking operators.

### 2.4 Lightweight Execution
Modes should minimize:
- Memory usage  
- CPU spikes  
- Large response buffers  

---

## 3. PERFORMANCE TARGETS

### 3.1 Mode Execution Targets
| Mode Type | Expected Latency | Notes |
|-----------|------------------|-------|
| Direct Fetch | < 50 ms (local) | No redirects |
| Header Injection | < 70 ms | Slight overhead |
| DNS Discovery | < 100 ms | Depends on resolver |
| Port Sweep | < 150 ms per port | Parallelizable |
| Protocol Abuse | < 120 ms | Depends on handler |

### 3.2 Dashboard Performance Targets
- Initial load: **< 200 ms**  
- History panel load: **< 150 ms**  
- Mode execution timeline render: **< 100 ms**  

### 3.3 API Performance Targets
- All API endpoints: **< 50 ms** under normal load  
- History retrieval: **< 80 ms**  

---

## 4. BENCHMARKING METHODOLOGY

### 4.1 Tools

pytest-benchmark locust (optional) custom timing decorators


### 4.2 Benchmark Environment
Benchmarks must run on:
- Local machine  
- Stable network conditions  
- No background load  
- Fixed timeout values  

### 4.3 Benchmark Command

pytest --benchmark-only


### 4.4 Benchmark Output
Benchmarks must record:
- Mean latency  
- Median latency  
- Standard deviation  
- Min/max  
- Outliers  

### 4.5 Benchmark Storage
Store results under:
benchmarks/results/<version>.json


---

## 5. PERFORMANCE REGRESSION DETECTION

### 5.1 Regression Thresholds
A regression is flagged when:
- Latency increases by > 20%  
- Standard deviation increases by > 30%  
- Error rate increases by any amount  
- Timeout rate increases by > 10%  

### 5.2 Regression Workflow
1. Run benchmarks  
2. Compare with previous version  
3. Identify anomalies  
4. Reproduce under controlled conditions  
5. File regression report  
6. Patch or optimize  

### 5.3 Required Regression Tests
- Mode execution latency  
- API endpoint latency  
- Dashboard render time  
- DNS resolution time  
- Response classification time  

---

## 6. BOTTLENECK ANALYSIS

### 6.1 Common Bottlenecks
- Slow DNS resolution  
- Large response bodies  
- Excessive logging  
- Inefficient classification logic  
- Blocking I/O in async paths  

### 6.2 How to Identify Bottlenecks
Use:
- Timing decorators  
- DEBUG logs  
- Trace events  
- Benchmark comparisons  
- Profiling tools  

### 6.3 Profiling Tools

py-spy cProfile yappi


---

## 7. OPTIMIZATION STRATEGIES

### 7.1 Reduce Response Size
- Truncate large bodies  
- Avoid storing full responses in history  
- Stream instead of buffer  

### 7.2 Improve DNS Performance
- Cache DNS results  
- Use async resolvers  
- Avoid repeated lookups  

### 7.3 Optimize Classification Logic
- Precompile regex patterns  
- Avoid unnecessary parsing  
- Use early exits  

### 7.4 Optimize Mode Execution
- Use async I/O  
- Avoid blocking calls  
- Use connection pooling  

### 7.5 Optimize API Performance
- Cache static responses  
- Avoid heavy computation in handlers  
- Use lightweight serialization  

---

## 8. RESOURCE USAGE GUIDELINES

### 8.1 Memory Usage
Targets:
- < 200 MB total  
- < 5 MB per mode execution  

### 8.2 CPU Usage
Targets:
- < 20% sustained load  
- < 50% during bursts  

### 8.3 Disk Usage
- History entries must be compact  
- Logs must rotate automatically  

---

## 9. PERFORMANCE TESTING FOR MODE AUTHORS

### 9.1 Required Tests
Each mode must include:
- Payload generation timing  
- Execution timing  
- Classification timing  
- Error‑path timing  

### 9.2 Forbidden Patterns
- Blocking I/O  
- Excessive retries  
- Large in‑memory buffers  
- Hidden network calls  

### 9.3 Recommended Patterns
- Async execution  
- Early classification  
- Minimal payloads  
- Efficient parsing  

---

## 10. APPENDIX — ESCAPED FENCING EXAMPLES

### 10.1 Escaped Benchmark Example
```markdown

Benchmark: direct_fetch Mean: 42.1 ms Stddev: 3.2 ms

### 10.2 Escaped JSON Example

json {"latency_ms": 42, "mode": "direct_fetch"}


