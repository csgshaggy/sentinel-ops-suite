# REAL_ORLD_EXAMPLES.md
SSRF CMMAND CONSOLE — REAL‑WORLD EXAMPLES  
Practical Payloads • Bypass Patterns • Misconfigurations • Operator Workflows

---

## 1. PURPOSE OF THIS DOCUMENT
This document provides practical, real‑world SSRF scenarios that operators can use to understand:

- How SSRF vulnerabilities manifest in real systems  
- How the SSRF Command Console analyzes and classifies responses  
- How bypasses and misconfigurations behave  
- How to interpret results in realistic environments  

All examples are **sanitized**, **safe**, and **non‑targeted**.

---

## 2. CLOUD METADATA SERVICE EXAMPLES

### 2.1 AWS Metadata (IMDSv1)
**Target:**

http://169.254.169.254/latest/meta-data


**Expected Behavior:**
- IMDSv1 responds without authentication  
- Many SSRF vulnerabilities historically exposed this endpoint  

**Console Classification:**

success


**Operator Insight:**
A `success` classification with a small, plaintext body often indicates metadata exposure.

---

### 2.2 AWS IMDSv2 (Token Required)
**Target:**
http://169.254.169.254/latest/meta-data


**Expected Behavior:**
- IMDSv2 requires a session token  
- Requests without token return 401 or 403  

**Console Classification:**

filtered


**Operator Insight:**
A `filtered` classification with a 401/403 suggests IMDSv2 is enabled — a good sign.

---

### 2.3 GCP Metadata
**Target:**
http://169.254.169.254/computeMetadata/v1/


**Expected Behavior:**
- Requires header: `Metadata-Flavor: Google`  
- Without header → 403  

**Console Classification:**

filtered


**Operator Insight:**
Consistent 403 responses indicate GCP metadata protection is working.

---

## 3. INTERNAL ADMIN PANEL EXAMPLES

### 3.1 Internal Dashboard
**Target:**

http://127.0.0.1:8080/admin


**Expected Behavior:**
- Internal admin panels often run on localhost  
- SSRF may expose them  

**Console Classification:**

success


**Operator Insight:**
A `success` classification with HTML content is a strong indicator of internal admin exposure.

---

### 3.2 Internal Service with Authentication
**Target:**
http://127.0.0.1:5000/internal-api


**Expected Behavior:**
- Returns 401 or 403  
- May leak headers or error messages  

**Console Classification:**

filtered


**Operator Insight:**
Authentication barriers reduce SSRF impact but still reveal internal topology.

---

## 4. DNS REBINDING EXAMPLES

### 4.1 Hostname That Rebinds to Internal IP
**Target:**

http://rebind.example.test


**Expected Behavior:**
- First DNS response → external IP  
- Second DNS response → internal IP  

**Console Classification:**

success


**Operator Insight:**
If the console logs show:
- First request → external  
- Second request → internal  
…then DNS rebinding is occurring.

---

### 4.2 Rebinding Protection Enabled
**Expected Behavior:**
- Server rejects mismatched Host headers  
- Server validates IP ranges  

**Console Classification:**

filtered


**Operator Insight:**
A `filtered` classification with a mismatch error indicates rebinding protection.

---

## 5. PROTOCOL ABUSE EXAMPLES

### 5.1 Gopher Protocol Injection
**Target:**

gopher://127.0.0.1:11211/_stats



**Expected Behavior:**
- Memcached responds with plaintext stats  
- SSRF can leak internal service info  

**Console Classification:**

success


**Operator Insight:**
A plaintext response with `STAT` lines indicates memcached exposure.

---

### 5.2 File Protocol Access
**Target:**

file:///etc/passwd



**Expected Behavior:**
- Many servers block file://  
- Some SSRF vectors allow local file reads  

**Console Classification:**

filtered


**Operator Insight:**
A `filtered` classification often means the backend fetcher blocks file:// access.

---

## 6. FIREWALL & WAF BEHAVIOR EXAMPLES

### 6.1 Firewall Blocking Internal Ranges
**Target:**

http://10.0.0.5


**Expected Behavior:**
- Firewall drops packets  
- No response  

**Console Classification:**
timeout


**Operator Insight:**
A `timeout` classification is typical for firewalled internal hosts.

---

### 6.2 WAF Blocking Suspicious Payloads
**Target:**

http://example.com/?url=http://127.0.0.1


**Expected Behavior:**
- WAF returns 403  
- May include block page  

**Console Classification:**

filtered


**Operator Insight:**
Consistent 403 responses with HTML block pages indicate WAF filtering.

---

## 7. REDIRECT BEHAVIOR EXAMPLES

### 7.1 Open Redirect to Internal Host
**Target:**

http://example.com/redirect?to=http://127.0.0.1


**Expected Behavior:**
- Server follows redirect  
- Internal host accessed indirectly  

**Console Classification:**

success


**Operator Insight:**
Redirect chains in trace logs confirm open redirect exploitation.

---

### 7.2 Redirect Blocked by Backend
**Expected Behavior:**
- Backend refuses to follow redirects to private IPs  

**Console Classification:**

filtered


**Operator Insight:**
This is a common SSRF mitigation.

---

## 8. PAYLOAD ENCODING EXAMPLES

### 8.1 Double‑Encoded Internal IP
**Target:**

http://example.com/?u=http:%253A%252F%252F127.0.0.1%252F%252F


**Expected Behavior:**
- Some servers decode twice  
- Internal IP accessed  

**Console Classification:**

success


**Operator Insight:**
Double‑decoding is a classic SSRF bypass.

---

### 8.2 Encoded Blocked Payload
**Expected Behavior:**
- Server decodes once  
- Blocks internal IP  

**Console Classification:**

filtered


---

## 9. OPERATOR WORKFLOW EXAMPLES

### 9.1 Identifying Internal Exposure
Steps:
1. Run `direct_fetch`  
2. Check classification  
3. Inspect response body  
4. Review trace events  
5. Compare with known patterns  

### 9.2 Detecting Firewall Behavior
Steps:
1. Run `port_sweep`  
2. Look for `timeout` patterns  
3. Compare timing anomalies  
4. Identify blocked ranges  

### 9.3 Detecting WAF Filtering
Steps:
1. Run encoded payload modes  
2. Compare `filtered` vs `success`  
3. Inspect HTML block pages  

---

## 10. APPENDIX — ESCAPED FENCING EXAMPLES

### 10.1 Escaped Code Block
```markdown

classification: success

### 10.2 Escaped JSON Block

json {"example": "metadata_service_access"}
