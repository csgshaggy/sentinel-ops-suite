# MODE Examples

## Overview
This document provides practical, real‑world examples of MODEs for the SSRF Command Console.  
Each example includes:

- Purpose  
- Manifest  
- Configuration  
- Input/Output schemas  
- Handler logic  
- Example run commands  

These examples help MODE authors understand patterns, best practices, and common use cases.

---

# 1. Example MODE: ssrf_basic_scan

## Purpose
Perform a simple SSRF scan by sending HTTP requests to targets and capturing responses.

## Manifest
\`\`\`yaml
name: ssrf_basic_scan
version: 1.0.0
entrypoint: main:run
summary: Basic SSRF scanning routine
requires:
  - network
  - http
config:
  timeout: 5
  retries: 2
outputs:
  - raw_responses
  - anomalies
\`\`\`

## Input Schema
\`\`\`python
targets: List[str]
\`\`\`

## Output Schema
\`\`\`python
raw_responses: Dict[str, str]
anomalies: List[str]
\`\`\`

## Example Run
\`\`\`bash
console run ssrf_basic_scan --targets example.com
\`\`\`

---

# 2. Example MODE: header_probe

## Purpose
Probe targets for SSRF‑relevant HTTP headers such as `X-Forwarded-For`, `Via`, and `Host`.

## Manifest
\`\`\`yaml
name: header_probe
version: 1.0.0
entrypoint: main:run
summary: Extracts SSRF-relevant HTTP headers from responses
requires:
  - network
  - http
config:
  timeout: 3
outputs:
  - headers
  - anomalies
\`\`\`

## Input Schema
\`\`\`python
targets: List[str]
\`\`\`

## Output Schema
\`\`\`python
headers: Dict[str, Dict[str, str]]
anomalies: List[str]
\`\`\`

## Example Run
\`\`\`bash
console run header_probe --targets internal.local
\`\`\`

---

# 3. Example MODE: dns_resolution_check

## Purpose
Check whether the server resolves internal DNS names, a common SSRF vector.

## Manifest
\`\`\`yaml
name: dns_resolution_check
version: 1.0.0
entrypoint: main:run
summary: Tests DNS resolution behavior for SSRF detection
requires:
  - dns
config:
  timeout: 2
outputs:
  - resolutions
  - anomalies
\`\`\`

## Input Schema
\`\`\`python
domains: List[str]
\`\`\`

## Output Schema
\`\`\`python
resolutions: Dict[str, str]
anomalies: List[str]
\`\`\`

## Example Run
\`\`\`bash
console run dns_resolution_check --domains metadata.google.internal
\`\`\`

---

# 4. Example MODE: redirect_chain_analyzer

## Purpose
Analyze redirect chains to detect SSRF‑related behavior such as internal hops.

## Manifest
\`\`\`yaml
name: redirect_chain_analyzer
version: 1.0.0
entrypoint: main:run
summary: Analyzes redirect chains for SSRF indicators
requires:
  - network
  - http
config:
  max_redirects: 10
outputs:
  - redirect_chains
  - anomalies
\`\`\`

## Input Schema
\`\`\`python
targets: List[str]
\`\`\`

## Output Schema
\`\`\`python
redirect_chains: Dict[str, List[str]]
anomalies: List[str]
\`\`\`

## Example Run
\`\`\`bash
console run redirect_chain_analyzer --targets example.com
\`\`\`

---

# 5. Example MODE: metadata_endpoint_detector

## Purpose
Detect whether a target leaks or proxies cloud metadata endpoints.

## Manifest
\`\`\`yaml
name: metadata_endpoint_detector
version: 1.0.0
entrypoint: main:run
summary: Detects cloud metadata endpoint exposure
requires:
  - network
  - http
config:
  timeout: 5
outputs:
  - metadata_hits
  - anomalies
\`\`\`

## Input Schema
\`\`\`python
targets: List[str]
\`\`\`

## Output Schema
\`\`\`python
metadata_hits: Dict[str, bool]
anomalies: List[str]
\`\`\`

## Example Run
\`\`\`bash
console run metadata_endpoint_detector --targets example.com
\`\`\`

---

# 6. Example MODE: internal_ip_discovery

## Purpose
Detect whether the target reveals internal IPs in headers, body, or redirects.

## Manifest
\`\`\`yaml
name: internal_ip_discovery
version: 1.0.0
entrypoint: main:run
summary: Detects internal IP leakage
requires:
  - network
  - http
config:
  timeout: 5
outputs:
  - findings
  - anomalies
\`\`\`

## Input Schema
\`\`\`python
targets: List[str]
\`\`\`

## Output Schema
\`\`\`python
findings: Dict[str, List[str]]
anomalies: List[str]
\`\`\`

## Example Run
\`\`\`bash
console run internal_ip_discovery --targets example.com
\`\`\`

---

# 7. Example MODE: ssrf_fuzz

## Purpose
Fuzz SSRF‑prone parameters using a curated payload list.

## Manifest
\`\`\`yaml
name: ssrf_fuzz
version: 1.0.0
entrypoint: main:run
summary: Fuzzes SSRF parameters using curated payloads
requires:
  - network
  - http
config:
  timeout: 5
  payload_set: default
outputs:
  - fuzz_results
  - anomalies
\`\`\`

## Input Schema
\`\`\`python
url: str
parameters: List[str]
\`\`\`

## Output Schema
\`\`\`python
fuzz_results: Dict[str, Dict[str, str]]
anomalies: List[str]
\`\`\`

## Example Run
\`\`\`bash
console run ssrf_fuzz --url https://example.com --parameters url,redirect
\`\`\`

---

# Conclusion

These examples demonstrate common MODE patterns, from simple HTTP probes to advanced SSRF fuzzing.  
Use them as references when designing new MODEs or extending the SSRF Command Console ecosystem.
