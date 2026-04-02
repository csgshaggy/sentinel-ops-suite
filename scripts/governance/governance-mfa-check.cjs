#!/usr/bin/env node

/**
 * MFA Governance Check
 * ---------------------
 * Enforces MFA as a hard governance requirement.
 *
 * CI will fail if:
 *  - MFA is disabled
 *  - MFA status cannot be retrieved
 *
 * CI will pass if:
 *  - MFA is enabled
 */

import fetch from "node-fetch";
import path from "path";
import fs from "fs";

const projectRoot = path.resolve(process.cwd());
const configPath = path.join(projectRoot, "frontend/config/runtime.json");

async function fetchMfaStatus() {
  try {
    const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
    const endpoint = `${config.apiBaseUrl}/auth/mfa/status`;

    const res = await fetch(endpoint, {
      method: "GET",
      credentials: "include",
    });

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    return await res.json();
  } catch (err) {
    console.error("❌ MFA governance check failed: unable to retrieve MFA status");
    console.error("   Error:", err.message);
    process.exit(1);
  }
}

(async () => {
  console.log("🔍 Running MFA governance check...");

  const status = await fetchMfaStatus();

  if (!status || typeof status.enabled !== "boolean") {
    console.error("❌ MFA governance check failed: invalid MFA status response");
    process.exit(1);
  }

  if (!status.enabled) {
    console.error("❌ MFA governance violation:");
    console.error("   MFA must be enabled for all operator accounts.");
    console.error("   Current status: DISABLED");
    process.exit(1);
  }

  console.log("✅ MFA governance check passed: MFA is enabled");
  process.exit(0);
})();
