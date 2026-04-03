#!/usr/bin/env node
import fs from "fs";
import path from "path";

const repoRoot = process.cwd();
const makefilePath = path.join(repoRoot, "Makefile");

console.log("🔎 Validating Makefile...");

if (!fs.existsSync(makefilePath)) {
  console.error("❌ Makefile not found at repo root.");
  process.exit(1);
}

const content = fs.readFileSync(makefilePath, "utf8");

const requiredTokens = [
  ".PHONY:",
  "backend:",
  "frontend:",
  "sync:",
  "drift:",
  "governance:",
  "repo-health:",
  "ops-health:",
  "ops-bootstrap:"
];

for (const token of requiredTokens) {
  if (!content.includes(token)) {
    console.error(`❌ Missing required token in Makefile: ${token}`);
    process.exit(1);
  }
}

const badIndent = content
  .split("\n")
  .filter(line => line.match(/^\s{4,}[^\s#]/));

if (badIndent.length > 0) {
  console.error("❌ Detected space-indented recipe lines. Make requires tabs.");
  console.error("Offending lines (first 5):");
  badIndent.slice(0, 5).forEach(l => console.error(`> ${l}`));
  process.exit(1);
}

console.log("✅ Makefile structure and invariants validated.");
