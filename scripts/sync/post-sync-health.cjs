#!/usr/bin/env node

/**
 * post-sync-health-snapshot.cjs
 * -----------------------------
 * Captures a timestamped snapshot of repo health immediately after sync.
 * This provides an immutable audit trail for debugging, governance,
 * and historical trend analysis.
 */

import fs from "fs";
import path from "path";
import { execSync } from "child_process";

const projectRoot = process.cwd();
const snapshotDir = path.join(projectRoot, "repo-health-snapshots");

function run(cmd) {
  return execSync(cmd, { encoding: "utf8" }).trim();
}

(function snapshot() {
  console.log("📊 Capturing post-sync repo health snapshot...");

  // Ensure snapshot directory exists
  if (!fs.existsSync(snapshotDir)) {
    fs.mkdirSync(snapshotDir, { recursive: true });
  }

  // Run RepoHealth collector
  const output = run("cd frontend && npx ts-node src/dashboard/repo-health/runRepoHealth.ts");

  // Parse JSON
  let parsed;
  try {
    parsed = JSON.parse(output);
  } catch (err) {
    console.error("❌ Failed to parse RepoHealth output as JSON.");
    process.exit(1);
  }

  // Timestamped filename
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  const filePath = path.join(snapshotDir, `repo-health-${timestamp}.json`);

  // Write snapshot
  fs.writeFileSync(filePath, JSON.stringify(parsed, null, 2), "utf8");

  console.log("✅ Repo health snapshot saved:");
  console.log("   " + filePath);
})();
