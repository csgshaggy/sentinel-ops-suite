#!/bin/bash

# Absolute backend path
BACKEND_DIR="/home/ubuntu/sentinel-ops-suite/backend"

# Output directory
OUT_DIR="/home/ubuntu/backend-login-scan"
mkdir -p "$OUT_DIR"

echo "[+] Scanning backend for login routes and templates..."

# 1. Search for 'login'
grep -R "login" -n "$BACKEND_DIR" > "$OUT_DIR/login-grep.txt"
echo "[+] Saved: $OUT_DIR/login-grep.txt"

# 2. Search for HTMLResponse
grep -R "HTMLResponse" -n "$BACKEND_DIR" > "$OUT_DIR/htmlresponse-grep.txt"
echo "[+] Saved: $OUT_DIR/htmlresponse-grep.txt"

# 3. Search for template usage
grep -R "template" -n "$BACKEND_DIR" > "$OUT_DIR/template-grep.txt"
echo "[+] Saved: $OUT_DIR/template-grep.txt"

echo "[+] Scan complete."
echo "[+] Files ready for SCP or copy:"
ls -l "$OUT_DIR"
