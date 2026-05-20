#!/usr/bin/env node

import fs from "fs";
import path from "path";
import process from "process";

console.log("🔎 Pre-sync validation starting...");

// -----------------------------
// Utility helpers
// -----------------------------
function readFileSafe(filePath) {
    try {
        return fs.readFileSync(filePath, "utf8");
    } catch {
        return null;
    }
}

function listFilesRecursively(dir) {
    let results = [];
    const list = fs.readdirSync(dir);

    for (const file of list) {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory()) {
            results = results.concat(listFilesRecursively(fullPath));
        } else {
            results.push(fullPath);
        }
    }
    return results;
}

// -----------------------------
// 1. Validate directory structure
// -----------------------------
const requiredDirs = [
    "backend",
    "frontend",
    "scripts",
    "scripts/sync",
    "ops_dir"
];

let missing = [];

for (const dir of requiredDirs) {
    if (!fs.existsSync(dir) || !fs.statSync(dir).isDirectory()) {
        missing.push(dir);
    }
}

if (missing.length > 0) {
    console.error("❌ Missing required directories:");
    for (const m of missing) console.error("   - " + m);
    process.exit(1);
}

console.log("📁 Directory structure validated.");


// -----------------------------
// 2. Detect REAL merge conflict markers
// -----------------------------
const conflictPatterns = [
    /^<<<<<<<\s/,
    /^=======\s*$/,
    /^>>>>>>>/
];

const allFiles = listFilesRecursively(".");
let conflictFiles = [];

for (const file of allFiles) {
    // Skip node_modules, venv, binaries, etc.
    if (file.includes("node_modules")) continue;
    if (file.includes(".venv")) continue;
    if (file.includes("dist")) continue;

    const content = readFileSafe(file);
    if (!content) continue;

    const lines = content.split("\n");

    for (const line of lines) {
        if (conflictPatterns.some(pattern => pattern.test(line))) {
            conflictFiles.push(file);
            break;
        }
    }
}

if (conflictFiles.length > 0) {
    console.error("❌ Merge conflict markers found in:");
    for (const f of conflictFiles) console.error("   - " + f);
    process.exit(1);
}

console.log("✔ No merge conflict markers found.");


// -----------------------------
// 3. Final success
// -----------------------------
console.log("✅ Pre-sync validation complete.");
process.exit(0);
