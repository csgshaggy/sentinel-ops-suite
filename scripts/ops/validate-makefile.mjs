#!/usr/bin/env node
import fs from "fs";
import path from "path";
import process from "process";

const REPO_ROOT = process.cwd();
const MAKEFILE_PATH = path.join(REPO_ROOT, "Makefile");

const REQUIRED_TARGETS = [
  "ops-health",
  "sync",
  "ops-bootstrap",
];

function logInfo(msg) {
  console.log(`ℹ️  ${msg}`);
}

function logOk(msg) {
  console.log(`✅ ${msg}`);
}

function logWarn(msg) {
  console.warn(`⚠️  ${msg}`);
}

function logError(msg) {
  console.error(`❌ ${msg}`);
}

function ensureMakefileExists() {
  if (!fs.existsSync(MAKEFILE_PATH)) {
    logError(`Makefile not found at ${MAKEFILE_PATH}`);
    process.exit(1);
  }
  logOk("Makefile found.");
}

function loadMakefile() {
  return fs.readFileSync(MAKEFILE_PATH, "utf8");
}

function hasTarget(content, target) {
  const pattern = new RegExp(`^${target}:`, "m");
  return pattern.test(content);
}

function validateRequiredTargets(content) {
  let ok = true;
  for (const target of REQUIRED_TARGETS) {
    if (!hasTarget(content, target)) {
      logError(`Required target missing: ${target}`);
      ok = false;
    } else {
      logOk(`Required target present: ${target}`);
    }
  }
  return ok;
}

function validateTabs(content) {
  const lines = content.split("\n");
  let ok = true;
  lines.forEach((line, idx) => {
    if (/^\s+@/.test(line) && !/^\t@/.test(line)) {
      logWarn(`Line ${idx + 1}: recipe line should start with a tab, not spaces.`);
      ok = false;
    }
  });
  if (ok) {
    logOk("Recipe indentation looks consistent (tabs).");
  }
  return ok;
}

function main() {
  console.log("🔎 Validating Makefile...");
  ensureMakefileExists();
  const content = loadMakefile();

  const targetsOk = validateRequiredTargets(content);
  const tabsOk = validateTabs(content);

  if (!targetsOk || !tabsOk) {
    logError("Makefile validation failed.");
    process.exit(1);
  }

  logOk("Makefile validation passed.");
}

main();
