#!/usr/bin/env node

/**
 * Makefile Self-Validator
 * -----------------------
 * Ensures:
 *  - Makefile exists at repo root
 *  - Makefile is syntactically valid
 *  - Required targets are present
 *
 * Intended to be run via:
 *   make validate-makefile
 */

import fs from "fs";
import path from "path";
import { spawnSync } from "child_process";

const projectRoot = process.cwd();
const makefilePath = path.join(projectRoot, "Makefile");

const REQUIRED_TARGETS = [
  "ci",
  "governance",
  "validate-mfa",
  "repo-health",
  "validate-makefile",
];

function ensureMakefileExists() {
  if (!fs.existsSync(makefilePath)) {
    console.error("❌ Makefile validation failed: Makefile not found at project root.");
    console.error("   Expected at:", makefilePath);
    process.exit(1);
  }
}

function checkSyntax() {
  // -n (dry run) + a harmless target name to force parsing
  const result = spawnSync("make", ["-n", "help"], {
    cwd: projectRoot,
    shell: true,
    stdio: "ignore",
  });

  if (result.status !== 0) {
    console.error("❌ Makefile validation failed: syntax error or invalid structure.");
    process.exit(1);
  }
}

function getTargets() {
  const result = spawnSync("make", ["-qp"], {
    cwd: projectRoot,
    shell: true,
    encoding: "utf8",
  });

  if (result.status !== 0) {
    console.error("❌ Makefile validation failed: unable to query targets with `make -qp`.");
    process.exit(1);
  }

  return result.stdout;
}

function checkRequiredTargets(output) {
  const missing = REQUIRED_TARGETS.filter((t) => !output.includes(`${t}:`));

  if (missing.length > 0) {
    console.error("❌ Makefile validation failed: missing required targets:");
    for (const t of missing) {
      console.error(`   - ${t}`);
    }
    process.exit(1);
  }
}

(function run() {
  console.log("🔍 Validating Makefile...");

  ensureMakefileExists();
  checkSyntax();

  const targetsOutput = getTargets();
  checkRequiredTargets(targetsOutput);

  console.log("✅ Makefile validation passed.");
  process.exit(0);
})();
