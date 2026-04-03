#!/usr/bin/env node
import fs from "fs";
import path from "path";
import crypto from "crypto";

const repoRoot = process.cwd();
const checksumFile = path.join(repoRoot, ".ops", "repo-structure-checksum.json");

console.log("🔐 Computing repo structure checksum...");

function walk(dir, base = "") {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  let files = [];
  for (const e of entries) {
    if ([".git", "node_modules", ".venv", ".ops", "snapshots"].includes(e.name)) continue;
    const rel = path.join(base, e.name);
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      files = files.concat(walk(full, rel));
    } else {
      files.push(rel);
    }
  }
  return files.sort();
}

const structure = walk(repoRoot);
const hash = crypto
  .createHash("sha256")
  .update(JSON.stringify(structure))
  .digest("hex");

if (!fs.existsSync(path.dirname(checksumFile))) {
  fs.mkdirSync(path.dirname(checksumFile), { recursive: true });
}

let previous = null;
if (fs.existsSync(checksumFile)) {
  previous = JSON.parse(fs.readFileSync(checksumFile, "utf8"));
}

const payload = {
  timestamp: new Date().toISOString(),
  hash,
  fileCount: structure.length
};

fs.writeFileSync(checksumFile, JSON.stringify(payload, null, 2));

console.log(`📁 Files tracked: ${structure.length}`);
console.log(`🔑 Current structure hash: ${hash}`);

if (previous && previous.hash !== hash) {
  console.log("⚠️ Structure drift detected (hash changed from previous run).");
} else if (previous) {
  console.log("✅ Structure unchanged since last checksum.");
} else {
  console.log("🆕 Baseline checksum created.");
}
