#!/bin/bash

# Activate venv
source venv/bin/activate

# Start FastAPI
uvicorn app.main:app --reload
