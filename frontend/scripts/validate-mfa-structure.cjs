#!/usr/bin/env node

/**
 * Sentinel Ops Suite — MFA Module Structure Validator
 * Deterministic, operator‑grade, CI‑safe.
 *
 * This validator ensures the MFA module maintains:
 * - required directories
 * - required files
 * - no drift in structure
 * - no missing components
 */

const fs = require("fs");
const path = require("path");

function fail(message) {
  console.error(`❌ ${message}`);
  process.exit(1);
}

function ok(message) {
  console.log(`✅ ${message}`);
}

const ROOT = path.resolve(__dirname, "../../..");
const MFA_ROOT = path.join(ROOT, "frontend", "src", "modules", "mfa");

// ---------------------------------------------------------------------------
// 1. Required directories
// ---------------------------------------------------------------------------
const requiredDirs = [
  MFA_ROOT,
  path.join(MFA_ROOT, "components"),
  path.join(MFA_ROOT, "hooks"),
  path.join(MFA_ROOT, "services"),
  path.join(MFA_ROOT, "state"),
];

// ---------------------------------------------------------------------------
// 2. Required files
// ---------------------------------------------------------------------------
const requiredFiles = [
  path.join(MFA_ROOT, "index.ts"),
  path.join(MFA_ROOT, "components", "MfaSetup.tsx"),
  path.join(MFA_ROOT, "components", "MfaVerify.tsx"),
  path.join(MFA_ROOT, "hooks", "useMfa.ts"),
  path.join(MFA_ROOT, "services", "mfaApi.ts"),
  path.join(MFA_ROOT, "state", "mfaSlice.ts"),
];

// ---------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------
console.log("🔍 Validating MFA module structure...");

for (const dir of requiredDirs) {
  if (!fs.existsSync(dir)) {
    fail(`Missing required directory: ${dir}`);
  }
}

for (const file of requiredFiles) {
  if (!fs.existsSync(file)) {
    fail(`Missing required file: ${file}`);
  }
}

ok("MFA module structure is valid.");
process.exit(0);
