# FULL_LAB_GUIDE.md
SSRF COMMAND CONSOLE — FULL LAB GUIDE  
Operator‑Grade, Forensic, End‑to‑End Workflow

---

## 1. PURPOSE OF THIS LAB
This lab provides a complete, reproducible, operator‑grade workflow for validating, analyzing, and mastering the SSRF Command Console. It is designed for:

- Backend developers validating SSRF behavior  
- Security engineers performing controlled SSRF testing  
- Operators running forensic analysis of server‑side fetch behavior  
- Learners building intuition around SSRF vectors, filters, and backend response patterns  

This guide walks you through environment setup, scanning modes, analysis workflows, dashboard usage, and structured exercises.

---

## 2. LAB PREREQUISITES

### 2.1 Required Skills
- Basic HTTP request/response understanding  
- Familiarity with FastAPI or similar backend frameworks  
- Comfort with CLI‑based tooling  
- Optional: Docker, Burp Suite, or proxy tooling  

### 2.2 Required Tools
- Python 3.10+  
- FastAPI + Uvicorn  
- SSRF Command Console (local or packaged)  
- A target environment (intentionally vulnerable or simulated)  

### 2.3 Optional Enhancements
- Dockerized vulnerable services  
- DNS logging platform  
- Burp Collaborator or similar callback server  
- Wireshark or tcpdump for packet‑level observation  

---

## 3. LAB ENVIRONMENT SETUP

### 3.1 Clone the Repository
\`\`\`bash
git clone https://github.com/example/ssrf-console
cd ssrf-console
\`\`\`

### 3.2 Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3.3 Start the Backend
\`\`\`bash
uvicorn app.main:app --reload --port 8000
\`\`\`

### 3.4 Verify the Console Loads
Navigate to:

http://localhost:8080/console


---

## 4. LAB TARGETS

### 4.1 Local Simulation Targets
- Internal metadata endpoints  
- Localhost‑restricted services  
- Mock internal APIs  
- File‑based fetch handlers  

### 4.2 Vulnerable Targets (Safe Labs Only)
- Deliberately vulnerable SSRF training apps  
- Dockerized microservices  
- Internal-only endpoints behind a reverse proxy  

### 4.3 Forbidden Targets
- Real production systems  
- Third‑party systems without explicit authorization  
- Cloud metadata endpoints on live infrastructure  

---

## 5. SCANNING MODES OVERVIEW

### 5.1 Direct Fetch Mode
Sends a raw URL to the backend’s fetch handler.

### 5.2 Header Injection Mode
Tests for SSRF filters that rely on header‑based allow/deny logic.

### 5.3 DNS‑Based Discovery Mode
Uses DNS callbacks to detect blind SSRF.

### 5.4 Port Sweep Mode
Enumerates internal ports via SSRF fetch behavior.

### 5.5 Protocol Abuse Mode
Attempts non‑HTTP protocols (file://, gopher://, dict://) when allowed.

---

## 6. LAB EXERCISE 1 — DIRECT SSRF DISCOVERY

### 6.1 Objective
Identify whether the backend fetcher allows arbitrary URL fetching.

### 6.2 Steps
1. Open the console.  
2. Select **Direct Fetch Mode**.  
3. Enter:
\`\`\`
http://127.0.0.1:80
\`\`\`
4. Observe response patterns:
   - Status codes  
   - Timeouts  
   - Redirect behavior  
   - Response body leakage  

### 6.3 Expected Outcomes
- If SSRF is allowed: backend returns internal service content.  
- If filtered: error messages or sanitized responses appear.  

---

## 7. LAB EXERCISE 2 — FILTER BYPASS TESTING

### 7.1 Objective
Identify weak allow/deny lists.

### 7.2 Test Payloads
\`\`\`
http://127.0.0.1
http://127.0.0.1:80
http://localhost
http://[::1]
http://2130706433
http://0x7f000001
\`\`\`

### 7.3 Steps
1. Switch to **Header Injection Mode**.  
2. Add variations of Host headers.  
3. Observe whether the backend trusts header‑based routing.  

### 7.4 Expected Outcomes
- Some filters fail when IP is encoded differently.  
- Some filters trust Host headers incorrectly.  

---

## 8. LAB EXERCISE 3 — BLIND SSRF DETECTION

### 8.1 Objective
Detect SSRF when no response is returned.

### 8.2 Requirements
- DNS logging server or callback domain  

### 8.3 Steps
1. Switch to **DNS‑Based Discovery Mode**.  
2. Enter:
\`\`\`
http://<your-callback-domain>/
\`\`\`
3. Trigger the request.  
4. Check DNS logs for resolution attempts.  

### 8.4 Expected Outcomes
- DNS lookup confirms backend attempted outbound fetch.  

---

## 9. LAB EXERCISE 4 — INTERNAL PORT ENUMERATION

### 9.1 Objective
Map internal services reachable by the backend.

### 9.2 Steps
1. Switch to **Port Sweep Mode**.  
2. Enter base target:
\`\`\`
http://127.0.0.1:{port}
\`\`\`
3. Sweep ports 1–1024 or custom ranges.  
4. Observe:
   - Fast failures  
   - Slow timeouts  
   - Successful connections  

### 9.3 Expected Outcomes
- Open ports produce distinct timing or content signatures.  

---

## 10. LAB EXERCISE 5 — PROTOCOL ABUSE

### 10.1 Objective
Test whether the backend fetcher mishandles non‑HTTP protocols.

### 10.2 Payloads
\`\`\`
file:///etc/passwd
gopher://127.0.0.1:11211/_stats
dict://127.0.0.1:2628/define:test
\`\`\`

### 10.3 Expected Outcomes
- Some backends incorrectly allow file:// reads.  
- Some libraries allow gopher:// or dict://.  

---

## 11. RESPONSE PATTERN ANALYSIS

### 11.1 Key Indicators
- Status code anomalies  
- Timing differences  
- Redirect loops  
- Partial content leakage  
- Header inconsistencies  

### 11.2 Forensic Workflow
1. Capture raw responses.  
2. Compare across payload classes.  
3. Cluster by timing, size, and error type.  
4. Identify patterns that reveal internal topology.  

---

## 12. DASHBOARD WORKFLOW

### 12.1 Live Request Builder
- Build payloads  
- Add headers  
- Toggle modes  

### 12.2 Response Viewer
- Color‑coded status  
- Timing indicators  
- Raw body + headers  

### 12.3 History Panel
- Timestamped request log  
- Diff viewer  
- Exportable JSON  

---

## 13. ADVANCED LAB: FILTER EVASION STRATEGIES

### 13.1 Encoding Variants
\`\`\`
http://127.0.0.1
http://127.0.0.1%23@evil.com
http://evil.com@127.0.0.1
\`\`\`

### 13.2 DNS Rebinding (Simulated Only)
- Use rebinding labs  
- Observe backend trust boundaries  

### 13.3 Chained Redirects
- Redirect external → internal  
- Observe whether backend follows redirects  

---

## 14. ADVANCED LAB: BACKEND BEHAVIOR PROFILING

### 14.1 Objective
Fingerprint backend fetch libraries.

### 14.2 Indicators
- Error message formats  
- TLS handshake quirks  
- Redirect handling  
- Timeout behavior  

### 14.3 Common Libraries
- Python requests  
- urllib  
- Node fetch  
- curl wrappers  

---

## 15. LAB COMPLETION CHECKLIST

### 15.1 Core Skills
- [ ] Direct SSRF detection  
- [ ] Blind SSRF detection  
- [ ] Filter bypassing  
- [ ] Port enumeration  
- [ ] Protocol abuse  

### 15.2 Analysis Skills
- [ ] Response clustering  
- [ ] Timing analysis  
- [ ] Redirect chain mapping  
- [ ] Internal topology inference  

### 15.3 Operational Skills
- [ ] Dashboard navigation  
- [ ] Mode selection  
- [ ] Payload crafting  
- [ ] Forensic logging  

---

## 16. NEXT STEPS

### 16.1 Build Your Own Modes
Extend the console with:
- Plugin‑style scanning modules  
- Custom protocol handlers  
- Automated diffing engines  

### 16.2 Integrate With Your Backend
- Add authentication  
- Add RBAC  
- Add session‑based access control  

### 16.3 Productization Path
- Package as consulting toolkit  
- Add operator dashboards  
- Add audit logging  

---

## 17. APPENDIX — ESCAPED FENCING EXAMPLES

### 17.1 Escaped Code Block
\`\`\`markdown
\`\`\`bash
curl http://127.0.0.1
\`\`\`
\`\`\`

### 17.2 Escaped JSON
\`\`\`markdown
\`\`\`json
{"url": "http://127.0.0.1"}
\`\`\`
\`\`\`

