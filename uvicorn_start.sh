#!/bin/bash
exec /home/ubuntu/sentinel-ops-suite/venv/bin/uvicorn sentinel_ops_suite.main:app --host 127.0.0.1 --port 8000
