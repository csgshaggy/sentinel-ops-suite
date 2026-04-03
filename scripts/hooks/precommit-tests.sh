#!/usr/bin/env bash
set -e

echo "🔍 Running backend unit tests..."
make -C backend test-unit

echo "🔍 Running dashboard unit tests..."
make -C dashboard test-unit

echo "🔍 Running dashboard Playwright smoke tests..."
make -C dashboard test-ui-ci

echo "✅ All tests passed. Commit allowed."
