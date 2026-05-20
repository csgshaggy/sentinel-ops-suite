# Training Lab Scenarios

## Overview

This document provides structured, hands‑on training labs for operators learning to use the SSRF Command Console.
Each scenario simulates a realistic environment, includes clear objectives, step‑by‑step tasks, expected artifacts, and evaluation criteria.

These labs are ideal for:

- Operator onboarding
- SOC analyst training
- Internal red/blue team exercises
- Skill validation and certification

---

# 1. Scenario: Basic SSRF Scan

## Objective

Learn to run a MODE, inspect run output, and identify basic anomalies.

## Environment

- Target: `example.com`
- MODE: `ssrf_basic_scan`

## Tasks

1. List available MODEs
2. Run `ssrf_basic_scan` against `example.com`
3. Locate the run directory
4. Inspect `input.json`, `output.json`, and `anomalies.json`
5. Review artifacts and logs

## Expected Skills

- Running MODEs
- Navigating run directories
- Understanding basic anomalies

## Success Criteria

- Operator identifies at least one anomaly or confirms none exist
- Operator can explain the structure of a run directory

---

# 2. Scenario: Redirect Chain Analysis

## Objective

Analyze redirect behavior and detect internal hops.

## Environment

- Target: `redirect.example.lab`
- MODE: `redirect_chain_analyzer`

## Tasks

1. Run the MODE with default settings
2. Inspect `redirect_chains.json`
3. Identify any internal or suspicious hops
4. Document findings

## Expected Skills

- Reading redirect chains
- Recognizing internal IP patterns
- Understanding SSRF redirect indicators

## Success Criteria

- Operator identifies internal hops or confirms external‑only behavior

---

# 3. Scenario: Metadata Endpoint Exposure

## Objective

Detect cloud metadata exposure through SSRF.

## Environment

- Target: `metadata-vulnerable.lab`
- MODE: `metadata_endpoint_detector`

## Tasks

1. Run the MODE
2. Inspect `metadata_hits`
3. Review anomalies
4. Document severity

## Expected Skills

- Identifying metadata endpoint exposure
- Understanding cloud SSRF risks

## Success Criteria

- Operator correctly identifies metadata exposure indicators

---

# 4. Scenario: DNS Resolution Behavior

## Objective

Determine whether the target resolves internal DNS names.

## Environment

- Domains:
  - `metadata.google.internal`
  - `internal.service.lab`
- MODE: `dns_resolution_check`

## Tasks

1. Run the MODE
2. Inspect `resolutions.json`
3. Identify internal IP resolution
4. Document findings

## Expected Skills

- Reading DNS resolution artifacts
- Recognizing internal IP ranges

## Success Criteria

- Operator identifies internal DNS resolution behavior

---

# 5. Scenario: Header Analysis

## Objective

Identify SSRF‑relevant headers and internal service leakage.

## Environment

- Target: `header-leak.lab`
- MODE: `header_probe`

## Tasks

1. Run the MODE
2. Inspect `headers.json`
3. Identify suspicious headers
4. Document anomalies

## Expected Skills

- Understanding SSRF‑relevant headers
- Recognizing internal hostnames

## Success Criteria

- Operator identifies at least one suspicious header

---

# 6. Scenario: Fuzzing SSRF Parameters

## Objective

Use payload‑driven fuzzing to detect SSRF vulnerabilities.

## Environment

- URL: `https://fuzz-target.lab`
- Parameters: `url`, `redirect`
- MODE: `ssrf_fuzz`

## Tasks

1. Run the MODE with default payload set
2. Inspect `fuzz_results.json`
3. Identify payloads that triggered anomalies
4. Document findings

## Expected Skills

- Running fuzzing MODEs
- Interpreting fuzzing artifacts
- Recognizing SSRF payload behavior

## Success Criteria

- Operator identifies at least one payload that triggers anomalous behavior

---

# 7. Scenario: Snapshot & Diff Workflow

## Objective

Detect drift between two runs.

## Environment

- Target: `drift.lab`
- MODE: `ssrf_basic_scan`
- Two runs with different responses

## Tasks

1. Run the MODE twice
2. Create a snapshot of the first run
3. Diff the second run against the snapshot
4. Identify differences

## Expected Skills

- Snapshot creation
- Diff analysis
- Drift detection

## Success Criteria

- Operator identifies at least one difference between runs

---

# 8. Scenario: Multi‑MODE Correlation

## Objective

Correlate results from two MODEs to identify deeper SSRF indicators.

## Environment

- Target: `correlation.lab`
- MODEs:
  - `dns_resolution_check`
  - `redirect_chain_analyzer`

## Tasks

1. Run both MODEs
2. Compare DNS results with redirect chains
3. Identify correlated anomalies
4. Document findings

## Expected Skills

- Cross‑MODE analysis
- Correlating artifacts
- Recognizing multi‑layer SSRF indicators

## Success Criteria

- Operator identifies at least one correlation between DNS and redirect behavior

---

# 9. Scenario: Error‑Signature Analysis

## Objective

Use error messages to detect SSRF‑related internal service exposure.

## Environment

- Target: `error-signal.lab`
- MODE: `ssrf_basic_scan`

## Tasks

1. Run the MODE
2. Inspect error messages in artifacts
3. Identify internal service indicators
4. Document findings

## Expected Skills

- Recognizing SSRF‑relevant error signatures
- Understanding internal service exposure

## Success Criteria

- Operator identifies at least one SSRF‑relevant error signature

---

# 10. Scenario: Full Operator Workflow

## Objective

Perform a complete operator workflow from execution to reporting.

## Environment

- Target: `full-workflow.lab`
- MODEs:
  - `ssrf_basic_scan`
  - `header_probe`
  - `redirect_chain_analyzer`

## Tasks

1. Run all three MODEs
2. Inspect all artifacts
3. Identify anomalies
4. Correlate findings
5. Create a snapshot
6. Produce a final operator report

## Expected Skills

- Full lifecycle operation
- Multi‑MODE correlation
- Snapshot usage
- Reporting

## Success Criteria

- Operator produces a complete, accurate report summarizing findings

---

# Conclusion

These training scenarios provide structured, realistic exercises for operators learning to use the SSRF Command Console.
They build confidence, reinforce best practices, and prepare operators for real‑world SSRF detection workflows.
