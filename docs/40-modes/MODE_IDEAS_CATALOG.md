# MODE Ideas Catalog

## Overview

This catalog provides a curated list of MODE ideas for expanding the SSRF Command Console ecosystem.
Each idea includes:

- Purpose
- Summary
- Required capabilities
- Suggested artifacts
- Potential anomaly logic
- Difficulty level

Use this catalog to plan new MODEs, extend coverage, or build specialized scanning pipelines.

---

# 1. HTTP & Redirect‑Focused MODEs

## 1.1 redirect_chain_analyzer (Advanced)

**Purpose:** Analyze redirect chains for internal hops or metadata endpoints.
**Capabilities:** network, http
**Artifacts:** redirect_chains.json
**Anomalies:** internal IP hops, metadata redirects

## 1.2 http_header_probe (Intermediate)

**Purpose:** Extract SSRF‑relevant headers.
**Artifacts:** header_map.json
**Anomalies:** internal hostnames, proxy headers

## 1.3 http_method_matrix (Advanced)

**Purpose:** Test SSRF behavior across HTTP methods (GET, POST, PUT, DELETE).
**Artifacts:** method_responses/
**Anomalies:** inconsistent behavior across methods

## 1.4 http_protocol_downgrade_test (Advanced)

**Purpose:** Test SSRF behavior when downgrading HTTPS → HTTP.
**Artifacts:** downgrade_results.json
**Anomalies:** insecure fallback behavior

---

# 2. DNS & Network‑Level MODEs

## 2.1 dns_resolution_check (Intermediate)

**Purpose:** Detect internal DNS resolution.
**Artifacts:** dns_resolution.json
**Anomalies:** internal IP resolution

## 2.2 dns_rebinding_detector (Advanced)

**Purpose:** Detect DNS rebinding vulnerabilities.
**Artifacts:** rebinding_results.json
**Anomalies:** IP switching across queries

## 2.3 internal_network_latency_probe (Advanced)

**Purpose:** Infer internal network access via timing.
**Artifacts:** latency_map.json
**Anomalies:** sub‑5ms responses

---

# 3. Cloud Metadata MODEs

## 3.1 metadata_endpoint_detector (Intermediate)

**Purpose:** Detect cloud metadata exposure.
**Artifacts:** metadata_hits.json
**Anomalies:** AWS/GCP/Azure metadata tokens

## 3.2 cloud_provider_fingerprint (Advanced)

**Purpose:** Identify cloud provider via SSRF responses.
**Artifacts:** provider_fingerprint.json
**Anomalies:** provider‑specific headers

## 3.3 imds_v2_token_probe (Advanced)

**Purpose:** Test for AWS IMDSv2 token leakage.
**Artifacts:** imds_token_results.json
**Anomalies:** token exposure

---

# 4. Fuzzing & Payload‑Driven MODEs

## 4.1 ssrf_fuzz (Advanced)

**Purpose:** Fuzz SSRF‑prone parameters.
**Artifacts:** fuzz_results.json
**Anomalies:** internal responses

## 4.2 scheme_fuzzer (Advanced)

**Purpose:** Test SSRF behavior across URL schemes.
**Schemes:** http, https, file, ftp, gopher
**Artifacts:** scheme_responses.json

## 4.3 encoding_bypass_fuzzer (Advanced)

**Purpose:** Test double‑encoding, mixed‑case, and nested payloads.
**Artifacts:** encoding_results.json

## 4.4 redirect_payload_fuzzer (Advanced)

**Purpose:** Fuzz redirect chains using crafted payloads.
**Artifacts:** redirect_fuzz_map.json

---

# 5. File & Protocol Abuse MODEs

## 5.1 file_scheme_probe (Intermediate)

**Purpose:** Test for file:// SSRF behavior.
**Artifacts:** file_access_results.json
**Anomalies:** file read success

## 5.2 gopher_probe (Advanced)

**Purpose:** Test for gopher:// SSRF exploitation.
**Artifacts:** gopher_results.json

## 5.3 ftp_probe (Advanced)

**Purpose:** Test for SSRF via FTP.
**Artifacts:** ftp_results.json

---

# 6. Application‑Specific MODEs

## 6.1 open_redirect_detector (Intermediate)

**Purpose:** Detect open redirects that can chain into SSRF.
**Artifacts:** redirect_map.json

## 6.2 template_injection_probe (Advanced)

**Purpose:** Detect SSRF via template engines (SSTI).
**Artifacts:** template_probe_results.json

## 6.3 webhook_relay_tester (Advanced)

**Purpose:** Test webhook endpoints for SSRF behavior.
**Artifacts:** webhook_results.json

---

# 7. Correlation & Multi‑MODE MODEs

## 7.1 dns_redirect_correlation (Advanced)

**Purpose:** Correlate DNS resolution with redirect chains.
**Artifacts:** correlation_report.json

## 7.2 header_dns_correlation (Advanced)

**Purpose:** Combine header anomalies with DNS results.
**Artifacts:** header_dns_map.json

## 7.3 multi_stage_ssrf_detector (Expert)

**Purpose:** Multi‑stage SSRF detection pipeline.
**Stages:** baseline → redirect → metadata → fuzz
**Artifacts:** multi_stage_report.json

---

# 8. Behavioral & Heuristic MODEs

## 8.1 anomaly_score_engine (Advanced)

**Purpose:** Assign weighted scores to anomalies.
**Artifacts:** anomaly_scores.json

## 8.2 timing_anomaly_detector (Advanced)

**Purpose:** Detect timing‑based SSRF indicators.
**Artifacts:** timing_map.json

## 8.3 error_signature_analyzer (Intermediate)

**Purpose:** Detect SSRF‑relevant error messages.
**Artifacts:** error_signatures.json

---

# 9. Exploitation‑Oriented MODEs (Red Team)

## 9.1 internal_service_mapper (Expert)

**Purpose:** Map internal services via SSRF.
**Artifacts:** service_map.json

## 9.2 internal_port_scanner (Expert)

**Purpose:** Perform SSRF‑based port scanning.
**Artifacts:** port_scan_results.json

## 9.3 metadata_extractor (Expert)

**Purpose:** Extract metadata tokens and credentials.
**Artifacts:** metadata_dump.json

---

# 10. Defensive & Blue‑Team MODEs

## 10.1 ssrf_filter_evaluator (Advanced)

**Purpose:** Evaluate SSRF filters and bypasses.
**Artifacts:** filter_evaluation.json

## 10.2 firewall_behavior_probe (Advanced)

**Purpose:** Detect firewall behavior via SSRF.
**Artifacts:** firewall_behavior.json

## 10.3 anomaly_baseline_builder (Intermediate)

**Purpose:** Build baseline anomaly profiles for drift detection.
**Artifacts:** baseline.json

---

# Conclusion

This catalog provides a broad set of MODE ideas across detection, fuzzing, correlation, cloud analysis, and exploitation.
Use these ideas to expand the SSRF Command Console ecosystem and build increasingly powerful, forensic‑grade MODEs.
