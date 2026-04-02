#!/usr/bin/env node

/**
 * governance-mfa-check.cjs
 * ------------------------
 * CommonJS-safe governance check using Node 24's built-in fetch.
 * No external dependencies required.
 */

const { execSync } = require("child_process");

function fail(msg) {
  console.error("❌ MFA Governance Check Failed:");
  console.error("   " + msg);
  process.exit(1);
}

(async function run() {
  console.log("🔍 Running MFA governance check...");

  try {
    const res = await fetch("http://localhost:3000/api/mfa/health");

    if (!res.ok) {
      fail("MFA health endpoint returned non-OK status.");
    }

    const data = await res.json();

    if (!data.ok || data.score < 100) {
      fail("MFA module is not fully healthy.");
    }

    console.log("✅ MFA governance check passed.");
  } catch (err) {
    fail("Error during MFA governance check: " + err.message);
  }
})();
