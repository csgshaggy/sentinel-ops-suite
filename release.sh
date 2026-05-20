#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 vX.Y.Z"
  exit 1
fi

TAG="$1"

echo "=== SSRF Command Console — Release $TAG ==="

# Ensure clean working tree
if [ -n "$(git status --porcelain)" ]; then
  echo "[FAIL] Working tree is dirty. Commit or stash changes first."
  exit 1
fi

echo "[*] Running doctor suite..."
make doctor

echo "[*] Cleaning old artifacts..."
make clean

echo "[*] Building package..."
make build

echo "[*] Running CLI smoke test..."
make smoke

echo "[*] Creating git tag: $TAG"
git tag -a "$TAG" -m "Release $TAG"

echo "[*] Pushing tag to origin..."
git push origin "$TAG"

echo "=== Release $TAG complete. ==="
