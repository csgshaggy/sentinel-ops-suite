# API Reference

## Overview

This document provides a complete reference for the SSRF Command Console API.
All endpoints are deterministic, validated, and return structured JSON responses.

---

# Base URL

\`\`\`
http://localhost:5000
\`\`\`

---

# Authentication

Authentication is optional but recommended.
Use a bearer token:

\`\`\`
Authorization: Bearer <token>
\`\`\`

---

# 1. MODE Endpoints

## GET /modes

Returns a list of all available MODEs.

### Example Response

\`\`\`
[
{
"name": "ssrf_basic_scan",
"version": "1.0.0",
"summary": "Basic SSRF scanning routine"
}
]
\`\`\`

---

## GET /modes/{mode_name}

Returns metadata for a specific MODE.

### Example Response

\`\`\`
{
"name": "ssrf_basic_scan",
"version": "1.0.0",
"summary": "Basic SSRF scanning routine",
"config": {
"timeout": 5,
"retries": 2
}
}
\`\`\`

---

## POST /modes/{mode_name}/run

Executes a MODE with the provided input.

### Example Request

\`\`\`
POST /modes/ssrf_basic_scan/run
{
"targets": ["example.com"]
}
\`\`\`

### Example Response

\`\`\`
{
"run_id": "20260317_120102_ssrf_basic_scan",
"status": "queued"
}
\`\`\`

---

# 2. Run Management

## GET /runs

Returns a list of all runs.

### Example Response

\`\`\`
[
{
"run_id": "20260317_120102_ssrf_basic_scan",
"mode": "ssrf_basic_scan",
"timestamp": "2026-03-17T12:01:02Z"
}
]
\`\`\`

---

## GET /runs/{run_id}

Returns metadata for a specific run.

### Example Response

\`\`\`
{
"run_id": "20260317_120102_ssrf_basic_scan",
"mode": "ssrf_basic_scan",
"timestamp": "2026-03-17T12:01:02Z",
"status": "completed"
}
\`\`\`

---

## GET /runs/{run_id}/output

Returns the final structured output of a run.

### Example Response

\`\`\`
{
"raw_responses": {
"example.com": "<html>...</html>"
},
"anomalies": []
}
\`\`\`

---

## GET /runs/{run_id}/logs

Returns execution logs for the run.

### Example Response

\`\`\`
[
{
"timestamp": "2026-03-17T12:01:03Z",
"event": "request_sent",
"target": "example.com",
"duration_ms": 120
}
]
\`\`\`

---

# 3. Artifact Endpoints

## GET /runs/{run_id}/artifacts

Lists all artifacts for a run.

### Example Response

\`\`\`
[
"raw/response_1.txt",
"processed/summary.json"
]
\`\`\`

---

## GET /runs/{run_id}/artifacts/{path}

Downloads a specific artifact.

### Response

Binary or text content depending on artifact type.

---

# 4. Snapshot & Diff

## POST /snapshots/{run_id}

Creates a snapshot of a run for future comparison.

### Example Response

\`\`\`
{
"snapshot_id": "snapshot_20260317_120102"
}
\`\`\`

---

## POST /diff

Compares two runs or snapshots.

### Example Request

\`\`\`
{
"left": "20260317_120102_ssrf_basic_scan",
"right": "20260317_121530_ssrf_basic_scan"
}
\`\`\`

### Example Response

\`\`\`
{
"differences": {
"anomalies": [],
"artifacts_changed": ["processed/summary.json"]
}
}
\`\`\`

---

# 5. Dashboard Endpoints

## GET /dashboard/summary

Returns high-level system and run statistics.

## GET /dashboard/recent

Returns the most recent runs.

---

# 6. Error Format

All errors follow a consistent structure:

\`\`\`
{
"error": {
"type": "ValidationError",
"message": "Invalid target format"
}
}
\`\`\`
