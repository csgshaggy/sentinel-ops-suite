#!/usr/bin/env node
import fs from "fs";
import path from "path";

console.log("🔍 Running governance checks...");

const repoRoot = process.cwd();
const required = [
  "Makefile",
  "backend",
  "frontend",
  "scripts/sync",
  "scripts/ops",
  "ops"
];

for (const item of required) {
  const full = path.join(repoRoot, item);
  if (!fs.existsSync(full)) {
    console.error(`❌ Governance violation: missing ${item}`);
    process.exit(1);
  }
}

console.log("📘 Required structure validated.");

const makefile = fs.readFileSync(path.join(repoRoot, "Makefile"), "utf8");
if (!makefile.includes(".PHONY")) {
  console.error("❌ Governance violation: Makefile missing .PHONY declarations.");
  process.exit(1);
}

console.log("📄 Makefile PHONY declarations validated.");
console.log("✅ Governance checks passed.");
