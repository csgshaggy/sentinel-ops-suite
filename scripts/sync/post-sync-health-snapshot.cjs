#!/usr/bin/env node

/**
 * post-sync-health-snapshot.cjs
 * -----------------------------
 * Captures a timestamped snapshot of repo health immediately after sync.
 * Uses CommonJS require() because this file is .cjs.
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const projectRoot = process.cwd();
const snapshotDir = path.join(projectRoot, "repo-health-snapshots");

function run(cmd) {
  return execSync(cmd, { encoding: "utf8" }).toString().trim();
}

(function snapshot() {
  console.log("📊 Capturing post-sync repo health snapshot...");

  // Ensure snapshot directory exists
  if (!fs.existsSync(snapshotDir)) {
    fs.mkdirSync(snapshotDir, { recursive: true });
  }

  // Run RepoHealth collector
  let output;
  try {
    output = run("cd frontend && npx ts-node src/dashboard/repo-health/runRepoHealth.ts");
  } catch (err) {
    console.error("❌ Failed to run RepoHealth collector.");
    console.error(err.message);
    process.exit(1);
  }

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
  try {
    fs.writeFileSync(filePath, JSON.stringify(parsed, null, 2), "utf8");
  } catch (err) {
    console.error("❌ Failed to write snapshot file.");
    console.error(err.message);
    process.exit(1);
  }

  console.log("✅ Repo health snapshot saved:");
  console.log("   " + filePath);
})();
