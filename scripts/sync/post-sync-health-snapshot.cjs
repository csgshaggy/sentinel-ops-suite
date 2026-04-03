#!/usr/bin/env node
import fs from "fs";
import path from "path";

console.log("📊 Generating repo health snapshot...");

const repoRoot = process.cwd();
const outDir = path.join(repoRoot, "snapshots");
const outFile = path.join(outDir, `health-${Date.now()}.json`);

if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const snapshot = {
  timestamp: new Date().toISOString(),
  filesAtRoot: fs.readdirSync(repoRoot).length,
  backendExists: fs.existsSync(path.join(repoRoot, "backend")),
  frontendExists: fs.existsSync(path.join(repoRoot, "frontend")),
  syncScripts: fs.existsSync(path.join(repoRoot, "scripts/sync"))
    ? fs.readdirSync(path.join(repoRoot, "scripts/sync"))
    : []
};

fs.writeFileSync(outFile, JSON.stringify(snapshot, null, 2));

console.log(`📁 Snapshot written: ${outFile}`);
console.log("✅ Repo health snapshot complete.");
