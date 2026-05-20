# MODE Catalog

## Overview

This catalog provides a centralized index of all MODEs available in the SSRF Command Console.
Each MODE entry includes its purpose, capabilities, configuration options, input/output schemas, and operational notes.

This document is intended for operators, developers, and contributors who need a quick reference to the MODE ecosystem.

---

# 1. MODE Index

| MODE Name       | Version | Summary                                           |
| --------------- | ------- | ------------------------------------------------- |
| ssrf_basic_scan | 1.0.0   | Performs basic SSRF detection against target URLs |

As new MODEs are added, they should be documented here following the structure below.

---

# 2. MODE Details

## 2.1 ssrf_basic_scan

### Summary

A foundational SSRF scanning MODE that performs HTTP requests against targets and analyzes responses for indicators of server-side request forgery.

### Capabilities

- Network access
- HTTP request execution
- Response capture
- Basic anomaly detection

### Manifest

\`\`\`
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

### Configuration

| Field   | Type | Default | Description                |
| ------- | ---- | ------- | -------------------------- |
| timeout | int  | 5       | Request timeout in seconds |
| retries | int  | 2       | Number of retry attempts   |

### Input Schema

\`\`\`
targets: List[str]
\`\`\`

### Output Schema

\`\`\`
raw_responses: Dict[str, str]
anomalies: List[str]
\`\`\`

### Handlers

- **Preflight:** Validates targets and configuration
- **Executor:** Sends HTTP requests and records responses
- **Postprocess:** Identifies anomalies and normalizes output

### Artifacts

- Raw HTTP responses
- Normalized response summaries
- Anomaly list

### Notes

This MODE is ideal for baseline SSRF detection and serves as a template for more advanced scanning MODEs.

---

# 3. MODE Template (For New MODE Authors)

To add a new MODE, follow this structure:

## <mode_name>

### Summary

Short description of what the MODE does.

### Capabilities

- List required capabilities
- Example: `network`, `dns`, `http`, `filesystem`

### Manifest

\`\`\`
name: <mode_name>
version: <version>
entrypoint: main:run
summary: <summary>
requires:

- <capability>
  config:
    <key>: <default>
  outputs:
- <artifact>
  \`\`\`

### Configuration

| Field   | Type   | Default   | Description   |
| ------- | ------ | --------- | ------------- |
| <field> | <type> | <default> | <description> |

### Input Schema

\`\`\`
<schema>
\`\`\`

### Output Schema

\`\`\`
<schema>
\`\`\`

### Handlers

- Preflight
- Executor
- Postprocess

### Artifacts

- Raw artifacts
- Processed artifacts
- Logs

### Notes

Any operational considerations, limitations, or special behaviors.

---

# 4. Adding a New MODE to the Catalog

To register a new MODE:

1. Add the MODE directory under:
   \`\`\`
   console/modes/<mode_name>/
   \`\`\`

2. Ensure the MODE passes validation:
   \`\`\`
   console modes validate <mode_name>
   \`\`\`

3. Add a new entry to the MODE Index table

4. Add a full MODE Details section following the template

5. Update CHANGELOG.md if applicable

---

# Conclusion

The MODE Catalog provides a structured, scalable reference for all MODEs in the SSRF Command Console.
As the ecosystem grows, this catalog ensures clarity, consistency, and discoverability across all operational modules.
