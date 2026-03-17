# Advanced SSRF Techniques (Educational & Defensive Reference)

## Overview
This document provides a high‑level, defensive, and academically oriented overview of advanced SSRF (Server‑Side Request Forgery) techniques.  
It is designed to help security teams, developers, and operators understand how SSRF manifests in complex systems so they can build better detection, monitoring, and mitigation strategies.

This guide does **not** provide exploit payloads or actionable attack instructions.  
Instead, it focuses on concepts, patterns, and behaviors relevant to detection and defense.

---

# 1. SSRF Fundamentals (High‑Level)

## 1.1 Core Idea
SSRF occurs when a server makes a request on behalf of a user and the user can influence the destination.

## 1.2 Why It Matters
- Access to internal services  
- Cloud metadata exposure  
- Firewall bypass  
- Privilege escalation  
- Lateral movement  

## 1.3 Common SSRF Surfaces
- URL parameters  
- Webhooks  
- Redirects  
- File fetchers  
- Image processors  
- PDF generators  
- Proxying services  

---

# 2. Advanced SSRF Behaviors (Conceptual)

## 2.1 Protocol Confusion
Systems may treat different URL schemes inconsistently, leading to unexpected behavior.

Examples (conceptual only):
- HTTP vs HTTPS  
- File‑based schemes  
- Legacy protocols  

## 2.2 Redirect‑Based SSRF
Servers may follow redirects automatically, sometimes into internal networks.

Key defensive indicators:
- Long redirect chains  
- Redirects to internal IP ranges  
- Redirect loops  

## 2.3 DNS‑Based SSRF
DNS resolution can reveal internal infrastructure or allow indirect access.

Defensive indicators:
- Internal IP resolution  
- DNS rebinding behavior  
- Wildcard DNS responses  

## 2.4 Timing‑Based Inference
Latency differences can reveal whether a server is accessing internal or external resources.

Defensive indicators:
- Sub‑millisecond responses  
- Consistent timing patterns across internal hosts  

---

# 3. Cloud‑Specific SSRF Concepts

## 3.1 Cloud Metadata Services
Most cloud providers expose metadata endpoints for instance configuration.

High‑level examples:
- AWS IMDS  
- GCP Metadata Server  
- Azure IMDS  

Defensive indicators:
- Metadata‑related headers  
- Unexpected metadata keywords in responses  
- Token‑based metadata access attempts  

## 3.2 Cloud Provider Fingerprinting
Servers may reveal cloud provider details through:
- Response headers  
- Error messages  
- Redirect patterns  

## 3.3 Token‑Based Metadata Access
Some metadata services require session tokens.  
Unexpected token‑related errors can indicate SSRF attempts.

---

# 4. Filter Evasion Concepts (Defensive Awareness)

This section describes **patterns**, not payloads.

## 4.1 Encoding Variants
Attackers may use:
- Double encoding  
- Mixed‑case schemes  
- Nested encodings  

Defensive takeaway:
Filters must normalize input before validation.

## 4.2 Scheme Obfuscation
Servers may incorrectly parse:
- Alternate schemes  
- Mixed‑case schemes  
- Scheme‑less URLs  

Defensive takeaway:
Use strict allowlists, not blocklists.

## 4.3 Redirect Abuse
Filters may validate only the initial URL, not the final destination.

Defensive takeaway:
Validate the entire redirect chain.

---

# 5. Internal Service Interaction (High‑Level)

## 5.1 Internal IP Ranges
Common internal ranges:
- 10.0.0.0/8  
- 172.16.0.0/12  
- 192.168.0.0/16  

Defensive takeaway:
Block server‑side requests to internal ranges unless explicitly required.

## 5.2 Service Fingerprinting
Internal services may reveal:
- Hostnames  
- Stack traces  
- Service banners  

Defensive takeaway:
Sanitize error messages and enforce strict outbound rules.

---

# 6. Behavioral Detection Techniques

## 6.1 Anomaly Scoring
Combine multiple weak signals into a strong indicator.

Example signals:
- Internal IP references  
- Metadata keywords  
- Redirect loops  
- Timing anomalies  

## 6.2 Cross‑Signal Correlation
Correlate:
- DNS results  
- Redirect chains  
- Header anomalies  
- Error signatures  

## 6.3 Baseline Drift Detection
Track normal behavior and detect deviations.

Useful for:
- Regression testing  
- Environment changes  
- Firewall rule updates  

---

# 7. Defensive Architecture Patterns

## 7.1 Outbound Request Proxying
Route all server‑side requests through a controlled proxy.

Benefits:
- Logging  
- Filtering  
- Rate limiting  
- Policy enforcement  

## 7.2 Strict Allowlisting
Allow only:
- Known hosts  
- Known protocols  
- Known ports  

## 7.3 Metadata Protection
Cloud providers offer:
- IMDSv2 (AWS)  
- Metadata request headers  
- Token‑based access  

Enable these features whenever possible.

---

# 8. Testing & Validation Strategies

## 8.1 MODE‑Based Testing
Use deterministic MODEs to:
- Probe redirect behavior  
- Analyze headers  
- Inspect DNS resolution  
- Detect timing anomalies  

## 8.2 Snapshot‑Based Regression Testing
Detect drift in:
- Redirect chains  
- Response bodies  
- Header structures  

## 8.3 Multi‑Stage Analysis
Combine:
- Baseline scans  
- Redirect analysis  
- Metadata detection  
- Fuzzing (conceptual)  

---

# 9. Summary

This document provides a high‑level, defensive, and academically appropriate overview of advanced SSRF concepts.  
It is designed to help teams understand SSRF behavior deeply so they can build stronger detection, monitoring, and mitigation strategies.

For implementation guidance, refer to:
- `MODE_TEMPLATES.md`  
- `ADVANCED_MODE_PATTERNS.md`  
- `MODE_EXAMPLES.md`  
- `OPERATOR_TRAINING.md`  
