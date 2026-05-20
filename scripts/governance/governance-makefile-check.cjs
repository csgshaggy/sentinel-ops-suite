#!/usr/bin/env node

/**
 * governance-makefile-check.cjs
 * Strict governance validator for Makefile integrity.
 * Node 24-compatible, CJS, deterministic, operator-grade.
 */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const MAKEFILE_PATH = path.join(process.cwd(), "Makefile");
const SNAPSHOT_PATH = path.join(process.cwd(), "scripts/snapshots/makefile.sha256");

const REQUIRED_TARGETS = [
  "governance",
  "governance-mfa",
  "governance-structure",
  "governance-integrity",
  "governance-makefile",
  "snapshot-makefile",
  "ci",
  "sync",
  "prepush"
];

const REQUIRED_INCLUDES = [
  "include scripts/make",
  "include scripts/governance"
];

const FORBIDDEN_PATTERNS = [
  /^ {2,}\w+/m, // spaces instead of tabs
  /deprecated/i,
  /todo:/i,
  /fixme:/i
];

const REQUIRED_HEADER = "# Operator-Grade Makefile";

function color(text, code) {
  return `\x1b[${code}m${text}\x1b[0m`;
}

function green(t) { return color(t, 32); }
function red(t) { return color(t, 31); }
function yellow(t) { return color(t, 33); }
function cyan(t) { return color(t, 36); }

function fail(reason) {
  console.error(red(`✖ ${reason}`));
  process.exit(1);
}

function ok(msg) {
  console.log(green(`✔ ${msg}`));
}

console.log(cyan("\n=== MAKEFILE GOVERNANCE CHECK (STRICT MODE) ===\n"));

// ------------------------------------------------------------
// 1. Load Makefile
// ------------------------------------------------------------
if (!fs.existsSync(MAKEFILE_PATH)) {
  fail("Makefile not found at repo root.");
}

const makefile = fs.readFileSync(MAKEFILE_PATH, "utf8");

// ------------------------------------------------------------
// 2. Header Validation
// ------------------------------------------------------------
if (!makefile.startsWith(REQUIRED_HEADER)) {
  fail(`Makefile missing required header: "${REQUIRED_HEADER}"`);
}
ok("Header validated");

// ------------------------------------------------------------
// 3. Required Targets
// ------------------------------------------------------------
for (const target of REQUIRED_TARGETS) {
  const regex = new RegExp(`^${target}:`, "m");
  if (!regex.test(makefile)) {
    fail(`Missing required target: ${target}`);
  }
}
ok("All required targets present");

// ------------------------------------------------------------
// 4. Required Includes
// ------------------------------------------------------------
for (const inc of REQUIRED_INCLUDES) {
  if (!makefile.includes(inc)) {
    fail(`Missing required include: ${inc}`);
  }
}
ok("All required includes present");

// ------------------------------------------------------------
// 5. PHONY Validation
// ------------------------------------------------------------
for (const target of REQUIRED_TARGETS) {
  const regex = new RegExp(`\\.PHONY:\\s*.*\\b${target}\\b`);
  if (!regex.test(makefile)) {
    fail(`Missing .PHONY declaration for: ${target}`);
  }
}
ok("All required .PHONY declarations present");

// ------------------------------------------------------------
// 6. Forbidden Patterns
// ------------------------------------------------------------
for (const pattern of FORBIDDEN_PATTERNS) {
  if (pattern.test(makefile)) {
    fail(`Forbidden pattern detected: ${pattern}`);
  }
}
ok("No forbidden patterns detected");

// ------------------------------------------------------------
// 7. Checksum Enforcement
// ------------------------------------------------------------
if (!fs.existsSync(SNAPSHOT_PATH)) {
  fail("Missing Makefile checksum snapshot. Run: make snapshot-makefile");
}

const currentHash = crypto.createHash("sha256").update(makefile).digest("hex");
const snapshotHash = fs.readFileSync(SNAPSHOT_PATH, "utf8").trim();

if (currentHash !== snapshotHash) {
  fail("Makefile checksum mismatch. Run: make snapshot-makefile");
}

ok("Checksum validated");

// ------------------------------------------------------------
// SUCCESS
// ------------------------------------------------------------
console.log(green("\nMakefile governance check passed.\n"));
process.exit(0);
