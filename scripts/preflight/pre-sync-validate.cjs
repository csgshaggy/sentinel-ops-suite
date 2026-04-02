#!/usr/bin/env node

/**
 * ============================================================
 *  PRE-SYNC VALIDATOR — HARDENED COMMONJS EDITION
 *  Features:
 *    • .venv exclusion
 *    • MIME-type filtering
 *    • Extension filtering
 *    • Directory blacklisting
 *    • Per-Makefile drift-check (file + file.canonical)
 *    • Correct Git conflict-marker detection
 * ============================================================
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

// ------------------------------------------------------------
// CONFIGURATION
// ------------------------------------------------------------

const BLACKLIST_DIRS = new Set([
  ".venv",
  "node_modules",
  "__pycache__",
  "dist",
  "build",
  ".git",
]);

const MAKEFILE_NAMES = new Set([
  "Makefile",
  "makefile",
]);

const ALLOWED_MIME_TYPES = new Set([
  "text/plain",
  "text/x-makefile",
]);

// Real Git conflict markers only
function scanFileForConflicts(filePath) {
  const lines = fs.readFileSync(filePath, "utf8").split("\n");

  return lines.some((line) =>
    line.startsWith("<<<<<<< ") ||
    line === "=======" ||
    line.startsWith(">>>>>>> ")
  );
}

// ------------------------------------------------------------
// UTILITY FUNCTIONS
// ------------------------------------------------------------

function getMimeType(filePath) {
  try {
    return execSync(`file --mime-type -b "${filePath}"`).toString().trim();
  } catch {
    return "unknown";
  }
}

function isBlacklisted(fullPath) {
  return fullPath.split(path.sep).some((segment) => BLACKLIST_DIRS.has(segment));
}

function isMakefileCandidate(filePath) {
  return MAKEFILE_NAMES.has(path.basename(filePath));
}

// ------------------------------------------------------------
// GENERALIZED DRIFT-CHECK PER MAKEFILE
// ------------------------------------------------------------

function verifyMakefileDrift(filePath) {
  const canonicalPath = filePath + ".canonical";

  if (!fs.existsSync(canonicalPath)) {
    // No canonical file → no drift enforcement for this Makefile
    return [];
  }

  const current = fs.readFileSync(filePath, "utf8").trim();
  const reference = fs.readFileSync(canonicalPath, "utf8").trim();

  if (current !== reference) {
    return [
      `Makefile drift detected: ${path.relative(
        process.cwd(),
        filePath
      )} differs from ${path.relative(process.cwd(), canonicalPath)}`,
    ];
  }

  return [];
}

// ------------------------------------------------------------
// DIRECTORY SCAN
// ------------------------------------------------------------

function scanDirectory(rootDir) {
  const issues = [];

  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      if (isBlacklisted(fullPath)) continue;

      if (entry.isDirectory()) {
        walk(fullPath);
        continue;
      }

      if (!isMakefileCandidate(fullPath)) continue;

      const mime = getMimeType(fullPath);
      if (!ALLOWED_MIME_TYPES.has(mime)) continue;

      // Conflict markers
      if (scanFileForConflicts(fullPath)) {
        issues.push(
          `Conflict markers found in Makefile: ${path.relative(
            process.cwd(),
            fullPath
          )}`
        );
      }

      // Drift
      const driftIssues = verifyMakefileDrift(fullPath);
      issues.push(...driftIssues);
    }
  }

  walk(rootDir);
  return issues;
}

// ------------------------------------------------------------
// MAIN EXECUTION
// ------------------------------------------------------------

const repoRoot = path.resolve(__dirname, "../../");
const issues = scanDirectory(repoRoot);

if (issues.length > 0) {
  console.error("❌ Pre-sync validation failed:");
  for (const issue of issues) {
    console.error("   " + issue);
  }
  process.exit(1);
}

console.log("✅ Pre-sync validation passed.");
process.exit(0);
