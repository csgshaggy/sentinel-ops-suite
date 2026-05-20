#!/usr/bin/env node

/**
 * governance-structure-check.cjs
 * ------------------------------
 * CommonJS-safe governance check using Node 24's built-in fetch.
 * - Fails if structure health endpoint is reachable and unhealthy
 * - Warns (but does NOT fail) if endpoint is unreachable
 */

function hardFail(msg) {
  console.error("❌ Structure Governance Check Failed:");
  console.error("   " + msg);
  process.exit(1);
}

function softWarn(msg) {
  console.warn("⚠️ Structure Governance Warning:");
  console.warn("   " + msg);
  // advisory only, do not exit non-zero
}

(async function run() {
  console.log("🔍 Running structure governance check...");

  const url = "http://localhost:3000/api/structure/health";

  try {
    const res = await fetch(url);

    if (!res.ok) {
      hardFail("Structure health endpoint returned non-OK status (" + res.status + ").");
    }

    const data = await res.json();

    if (!data.ok || data.score < 100) {
      hardFail(
        "Repository structure is not fully healthy (score: " + (data.score ?? "n/a") + ")."
      );
    }

    console.log("✅ Structure governance check passed.");
  } catch (err) {
    softWarn("Could not reach structure health endpoint (" + url + "): " + err.message);
  }
})();
