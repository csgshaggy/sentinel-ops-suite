# Advanced MODE Patterns

## Overview

This document provides advanced architectural and behavioral patterns for building sophisticated MODEs in the SSRF Command Console.
These patterns go beyond basic MODE authoring and focus on:

- High‑complexity workflows
- Multi‑stage execution
- Adaptive scanning
- Heuristic and signature‑based anomaly detection
- Artifact‑driven pipelines
- Parallel execution
- Stateful MODEs
- Cross‑MODE correlation
- Advanced SSRF exploitation logic

These patterns help MODE authors design powerful, extensible, and forensic‑grade MODEs.

---

# 1. Multi‑Stage MODE Pattern

## Purpose

Split execution into multiple deterministic phases, each producing artifacts consumed by the next stage.

## Structure

\`\`\`text
preflight → stage1 → stage2 → stage3 → postprocess
\`\`\`

## Example Use Case

- Stage 1: Fetch baseline response
- Stage 2: Probe redirect behavior
- Stage 3: Analyze internal service exposure

## Pattern Snippet

\`\`\`python
def run(preflight_data):
s1 = stage1.run(preflight_data)
s2 = stage2.run(s1)
s3 = stage3.run(s2)
return postprocess.run(s3)
\`\`\`

---

# 2. Adaptive Scanning Pattern

## Purpose

MODE adjusts behavior based on intermediate results.

## Example Logic

- If response contains internal IP → enable deeper probing
- If metadata endpoint detected → trigger metadata extraction subroutine

## Pattern Snippet

\`\`\`python
if "169.254" in body:
results["deep_scan"] = deep_probe(target)
\`\`\`

---

# 3. Heuristic + Signature Hybrid Detection

## Purpose

Combine rule‑based signatures with heuristic anomaly scoring.

## Example

- Signature: `X-aws-ec2-metadata-token` header
- Heuristic: unusual redirect chain length

## Pattern Snippet

\`\`\`python
score = 0
if "metadata" in body.lower():
score += 5
if len(redirects) > 3:
score += 2
if score >= 5:
anomalies.append("High-confidence SSRF indicator")
\`\`\`

---

# 4. Artifact‑Driven MODE Pattern

## Purpose

MODEs generate structured artifacts that feed into dashboards, diffs, and downstream MODEs.

## Example Artifacts

- `raw_responses/`
- `redirect_chains.json`
- `header_map.json`
- `dns_resolution.json`

## Pattern Snippet

\`\`\`python
artifact_writer.write_json("redirect_chains.json", chains)
\`\`\`

---

# 5. Parallel Execution Pattern

## Purpose

Speed up MODE execution by parallelizing independent tasks.

## Example Use Case

- Fuzzing multiple parameters
- Probing multiple endpoints
- DNS resolution across many domains

## Pattern Snippet

\`\`\`python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=10) as pool:
results = list(pool.map(fetch, targets))
\`\`\`

---

# 6. Stateful MODE Pattern

## Purpose

MODE maintains state across stages or across targets.

## Example Use Case

- Track redirect loops
- Track internal IP exposure frequency
- Track metadata endpoint hits

## Pattern Snippet

\`\`\`python
state = {"internal_hits": 0}

for t in targets:
body = fetch(t)
if "169.254" in body:
state["internal_hits"] += 1
\`\`\`

---

# 7. Cross‑MODE Correlation Pattern

## Purpose

MODE consumes artifacts from previous runs or other MODEs.

## Example Use Case

- Combine DNS resolution results with redirect analysis
- Combine header anomalies with fuzzing results

## Pattern Snippet

\`\`\`python
dns_data = load_artifact("dns_resolution.json")
redirects = load_artifact("redirect_chains.json")

if dns_data[target] in redirects[target]:
anomalies.append("DNS → Redirect correlation detected")
\`\`\`

---

# 8. Payload‑Driven Fuzzing Pattern

## Purpose

MODE uses curated payload sets to probe SSRF‑prone parameters.

## Example Payload Set

\`\`\`yaml
payloads:

- http://127.0.0.1
- http://169.254.169.254/latest/meta-data
- http://[::1]
- file:///etc/passwd
  \`\`\`

## Pattern Snippet

\`\`\`python
for param in parameters:
for payload in payloads:
url = f"{base_url}?{param}={payload}"
responses[param][payload] = fetch(url)
\`\`\`

---

# 9. Redirect Chain Intelligence Pattern

## Purpose

MODE analyzes redirect chains for SSRF indicators.

## Example Logic

- Detect internal hops
- Detect cloud metadata endpoints
- Detect infinite loops

## Pattern Snippet

\`\`\`python
if any("169.254" in hop for hop in chain):
anomalies.append("Redirect to metadata endpoint detected")
\`\`\`

---

# 10. Timing‑Based Detection Pattern

## Purpose

Use timing differences to infer internal network access.

## Example Logic

- Internal IPs respond faster
- External IPs respond slower

## Pattern Snippet

\`\`\`python
start = time.time()
fetch(target)
latency = time.time() - start

if latency < 0.05:
anomalies.append("Possible internal network access")
\`\`\`

---

# 11. Error‑Signature Pattern

## Purpose

Detect SSRF indicators based on error messages.

## Example Signatures

- “connection refused”
- “no route to host”
- “EC2 metadata token required”

## Pattern Snippet

\`\`\`python
if "connection refused" in error.lower():
anomalies.append("Internal service refused connection")
\`\`\`

---

# 12. Multi‑Protocol MODE Pattern

## Purpose

MODE probes multiple protocols:

- HTTP
- HTTPS
- DNS
- FTP (if allowed)
- Gopher (legacy SSRF vector)

## Pattern Snippet

\`\`\`python
results["http"] = http_probe(target)
results["dns"] = dns_probe(target)
\`\`\`

---

# 13. Chained Payload Pattern

## Purpose

MODE chains payloads to bypass filters.

## Example Payloads

- Double URL encoding
- Mixed‑case schemes
- Nested redirects

## Pattern Snippet

\`\`\`python
payload = urllib.parse.quote(urllib.parse.quote("http://169.254.169.254"))
\`\`\`

---

# 14. Advanced Anomaly Scoring Pattern

## Purpose

MODE assigns weighted scores to anomalies.

## Example

\`\`\`python
score = (
5 _ int("metadata" in body.lower()) +
3 _ int("169.254" in body) +
2 \* int(len(redirects) > 3)
)

if score >= 5:
anomalies.append("High-confidence SSRF indicator")
\`\`\`

---

# 15. MODE Composition Pattern

## Purpose

MODEs call other MODEs as subroutines.

## Example

- Run `dns_resolution_check` before `redirect_chain_analyzer`
- Combine results in postprocess

## Pattern Snippet

\`\`\`python
dns = run_mode("dns_resolution_check", {"domains": targets})
redirects = run_mode("redirect_chain_analyzer", {"targets": targets})
\`\`\`

---

# Conclusion

These advanced patterns enable MODE authors to build powerful, extensible, and forensic‑grade MODEs.
Use these patterns to design MODEs that adapt, correlate, analyze deeply, and produce high‑value artifacts for operators and analysts.
