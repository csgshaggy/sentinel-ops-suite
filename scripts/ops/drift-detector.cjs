#!/usr/bin/env node
import fs from "fs";
import path from "path";
import crypto from "crypto";
import { execSync } from "child_process";

const repoRoot = process.cwd();
const baselineFile = path.join(repoRoot, ".ops", "drift-baseline.json");

console.log("🛰  Running CI-grade drift detector...");

function hashFile(filePath) {
  const data = fs.readFileSync(filePath);
  return crypto.createHash("sha256").update(data).digest("hex");
}

function collectFiles(dir, base = "") {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  let files = [];
  for (const e of entries) {
    if ([".git", "node_modules", ".venv", ".ops", "snapshots"].includes(e.name)) continue;
    const rel = path.join(base, e.name);
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      files = files.concat(collectFiles(full, rel));
    } else {
      files.push(rel);
    }
  }
  return files.sort();
}

const files = collectFiles(repoRoot);
const map = {};

for (const rel of files) {
  const full = path.join(repoRoot, rel);
  map[rel] = hashFile(full);
}

if (!fs.existsSync(path.dirname(baselineFile))) {
  fs.mkdirSync(path.dirname(baselineFile), { recursive: true });
}

if (!fs.existsSync(baselineFile)) {
  fs.writeFileSync(
    baselineFile,
    JSON.stringify({ createdAt: new Date().toISOString(), files: map }, null, 2)
  );
  console.log("🆕 Drift baseline created.");
  process.exit(0);
}

const baseline = JSON.parse(fs.readFileSync(baselineFile, "utf8"));
const baselineFiles = baseline.files;

const added = [];
const removed = [];
const changed = [];

for (const rel of Object.keys(map)) {
  if (!baselineFiles[rel]) {
    added.push(rel);
  } else if (baselineFiles[rel] !== map[rel]) {
    changed.push(rel);
  }
}

for (const rel of Object.keys(baselineFiles)) {
  if (!map[rel]) {
    removed.push(rel);
  }
}

if (added.length === 0 && removed.length === 0 && changed.length === 0) {
  console.log("✅ No drift detected vs baseline.");
  process.exit(0);
}

console.log("⚠️ Drift detected:");
if (added.length) {
  console.log("  ➕ Added:");
  added.forEach(f => console.log(`    - ${f}`));
}
if (removed.length) {
  console.log("  ➖ Removed:");
  removed.forEach(f => console.log(`    - ${f}`));
}
if (changed.length) {
  console.log("  ✏️ Changed:");
  changed.forEach(f => console.log(`    - ${f}`));
}

try {
  const gitStatus = execSync("git status --short", { cwd: repoRoot }).toString();
  console.log("\n📄 git status --short:");
  console.log(gitStatus || "(clean)");
} catch {
  console.log("⚠️ Unable to run git status.");
}

process.exit(1);
