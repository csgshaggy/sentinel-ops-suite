#!/usr/bin/env node

/**
 * Sentinel Ops Suite — MFA Module Structure Validator
 * Deterministic, operator-grade, CI-safe.
 *
 * This validator ensures the MFA module maintains:
 * - required directories
 * - required files
 * - no drift in structure
 * - no missing components
 */

const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------
// Utility helpers
// ---------------------------------------------------------------------
function fail(message) {
  console.error(`❌ ${message}`);
  process.exit(1);
}

function ok(message) {
  console.log(`✅ ${message}`);
}

// ---------------------------------------------------------------------
// Resolve project root dynamically (no hardcoded paths)
// Script lives at: frontend/scripts/validate-mfa-structure.cjs
// Project root is two levels up from here.
// ---------------------------------------------------------------------
const ROOT = path.resolve(__dirname, "../../");
const MFA_ROOT = path.join(ROOT, "frontend", "src", "modules", "mfa");

console.log("🔍 Validating MFA module structure...");
console.log(`🔧 Project root resolved to: ${ROOT}`);
console.log(`🔧 MFA module root expected at: ${MFA_ROOT}`);

// ---------------------------------------------------------------------
// Required directories
// ---------------------------------------------------------------------
const requiredDirs = [
  MFA_ROOT,
  path.join(MFA_ROOT, "components"),
  path.join(MFA_ROOT, "hooks"),
  path.join(MFA_ROOT, "services"),
  path.join(MFA_ROOT, "state"),
];

// ---------------------------------------------------------------------
// Required files
// ---------------------------------------------------------------------
const requiredFiles = [
  path.join(MFA_ROOT, "index.ts"),
  path.join(MFA_ROOT, "mfa.types.ts"),
  path.join(MFA_ROOT, "services", "mfa.service.ts"),
  path.join(MFA_ROOT, "state", "mfa.store.ts"),
];

// ---------------------------------------------------------------------
// Directory validation
// ---------------------------------------------------------------------
for (const dir of requiredDirs) {
  if (!fs.existsSync(dir)) {
    fail(`Missing required directory: ${dir}`);
  }
}

ok("All required directories exist.");

// ---------------------------------------------------------------------
// File validation
// ---------------------------------------------------------------------
for (const file of requiredFiles) {
  if (!fs.existsSync(file)) {
    fail(`Missing required file: ${file}`);
  }
}

ok("All required files exist.");
ok("MFA module structure validated successfully.");
