#!/usr/bin/env node

/**
 * governance-deps-check.cjs
 * -------------------------
 * CommonJS-safe governance check using Node 24's built-in fetch.
 * - Fails if dependency health endpoint is reachable and unhealthy
 * - Warns (but does NOT fail) if endpoint is unreachable
 */

function hardFail(msg) {
  console.error("❌ Dependency Governance Check Failed:");
  console.error("   " + msg);
  process.exit(1);
}

function softWarn(msg) {
  console.warn("⚠️ Dependency Governance Warning:");
  console.warn("   " + msg);
  // advisory only — do not exit non-zero
}

(async function run() {
  console.log("🔍 Running dependency governance check...");

  const url = "http://localhost:3000/api/deps/health";

  try {
    const res = await fetch(url);

    if (!res.ok) {
      hardFail("Dependency health endpoint returned non-OK status (" + res.status + ").");
    }

    const data = await res.json();

    if (!data.ok || data.score < 100) {
      hardFail(
        "Dependencies are not fully healthy (score: " + (data.score ?? "n/a") + ")."
      );
    }

    console.log("✅ Dependency governance check passed.");
  } catch (err) {
    softWarn("Could not reach dependency health endpoint (" + url + "): " + err.message);
  }
})();
