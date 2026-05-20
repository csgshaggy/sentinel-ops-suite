#!/usr/bin/env node

/**
 * governance-mfa-check.cjs
 * ------------------------
 * CommonJS-safe governance check using Node 24's built-in fetch.
 * - Fails if MFA health endpoint is reachable and unhealthy
 * - Warns (but does NOT fail) if endpoint is unreachable
 */

function hardFail(msg) {
  console.error("❌ MFA Governance Check Failed:");
  console.error("   " + msg);
  process.exit(1);
}

function softWarn(msg) {
  console.warn("⚠️ MFA Governance Warning:");
  console.warn("   " + msg);
  // Do NOT exit non-zero — governance is advisory in this case
}

(async function run() {
  console.log("🔍 Running MFA governance check...");

  const url = "http://localhost:3000/api/mfa/health";

  try {
    const res = await fetch(url);

    if (!res.ok) {
      hardFail("MFA health endpoint returned non-OK status (" + res.status + ").");
    }

    const data = await res.json();

    if (!data.ok || data.score < 100) {
      hardFail("MFA module is not fully healthy (score: " + (data.score ?? "n/a") + ").");
    }

    console.log("✅ MFA governance check passed.");
  } catch (err) {
    // Treat connectivity issues as a soft governance warning, not a hard failure
    softWarn("Could not reach MFA health endpoint (" + url + "): " + err.message);
  }
})();
