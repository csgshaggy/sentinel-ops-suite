#!/usr/bin/env node
import fs from "fs";
import path from "path";
import process from "process";

const REPO_ROOT = process.cwd();

const REQUIRED_PATHS = [
  "Makefile",
  "ops",
  "ops_dir",
  "scripts",
  "scripts/sync",
  "scripts/ops",
];

function logOk(msg) {
  console.log(`✅ ${msg}`);
}

function logError(msg) {
  console.error(`❌ ${msg}`);
}

function exists(relPath) {
  return fs.existsSync(path.join(REPO_ROOT, relPath));
}

function main() {
  console.log("🔎 Validating repository structure...");

  let ok = true;

  for (const p of REQUIRED_PATHS) {
    if (!exists(p)) {
      logError(`Missing required path: ${p}`);
      ok = false;
    } else {
      logOk(`Found: ${p}`);
    }
  }

  if (!ok) {
    logError("Repository structure validation failed.");
    process.exit(1);
  }

  logOk("Repository structure validation passed.");
}

main();
