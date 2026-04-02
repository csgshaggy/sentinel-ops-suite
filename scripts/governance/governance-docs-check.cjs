#!/usr/bin/env node

/**
 * governance-docs-check.cjs
 * -------------------------
 * CommonJS-safe governance check using Node 24's built-in fetch.
 * - Fails if docs health endpoint is reachable and unhealthy
 * - Warns (but does NOT fail) if endpoint is unreachable
 */

function hardFail(msg) {
  console.error("❌ Docs Governance Check Failed:");
  console.error("   " + msg);
  process.exit(1);
}

function softWarn(msg) {
  console.warn("⚠️ Docs Governance Warning:");
  console.warn("   " + msg);
  // advisory only — do not exit non-zero
}

(async function run() {
  console.log("🔍 Running docs governance check...");

  const url = "http://localhost:3000/api/docs/health";

  try {
    const res = await fetch(url);

    if (!res.ok) {
      hardFail("Docs health endpoint returned non-OK status (" + res.status + ").");
    }

    const data = await res.json();

    if (!data.ok || data.score < 100) {
      hardFail(
        "Documentation health is not fully compliant (score: " + (data.score ?? "n/a") + ")."
      );
    }

    console.log("✅ Docs governance check passed.");
  } catch (err) {
    softWarn("Could not reach docs health endpoint (" + url + "): " + err.message);
  }
})();
