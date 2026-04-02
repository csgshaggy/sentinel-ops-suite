#!/usr/bin/env node

/**
 * validate-makefile.cjs
 * ---------------------
 * CommonJS-safe Makefile validator for Node 24.
 * - Ensures Makefile exists
 * - Ensures it contains required governance targets
 * - Hard fails on structural issues
 */

const fs = require("fs");
const path = require("path");

function fail(msg) {
  console.error("❌ Makefile Validation Failed:");
  console.error("   " + msg);
  process.exit(1);
}

function ok(msg) {
  console.log("✅ " + msg);
}

(function run() {
  console.log("🔍 Validating Makefile...");

  const makefilePath = path.join(process.cwd(), "Makefile");

  // 1. Ensure Makefile exists
  if (!fs.existsSync(makefilePath)) {
    fail("Makefile not found at: " + makefilePath);
  }

  const content = fs.readFileSync(makefilePath, "utf8");

  // 2. Ensure required governance targets exist
  const requiredTargets = [
    "check-mfa:",
    "check-structure:",
    "check-docs:",
    "check-deps:",
  ];

  for (const target of requiredTargets) {
    if (!content.includes(target)) {
      fail("Missing required Makefile target: " + target);
    }
  }

  ok("Makefile validation passed.");
})();
