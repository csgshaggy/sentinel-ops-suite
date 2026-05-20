#!/usr/bin/env node

/**
 * check_imports.js
 * Operator-grade broken import detector.
 * Scans all JS/JSX/TS/TSX files and verifies that every import target exists.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "frontend", "unified-frontend", "src");

const exts = [".js", ".jsx", ".ts", ".tsx"];

function fileExists(p) {
  if (fs.existsSync(p)) return true;

  // Try with extensions
  for (const ext of exts) {
    if (fs.existsSync(p + ext)) return true;
  }
  return false;
}

function scanDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      scanDir(full);
    } else if (entry.isFile()) {
      if (/\.(js|jsx|ts|tsx)$/.test(entry.name)) {
        scanFile(full);
      }
    }
  }
}

let broken = [];

function scanFile(filePath) {
  const content = fs.readFileSync(filePath, "utf8");
  const importRegex = /import\s+[^'"]*['"]([^'"]+)['"]/g;

  let match;
  while ((match = importRegex.exec(content)) !== null) {
    const importPath = match[1];

    // Skip non-relative imports
    if (!importPath.startsWith(".")) continue;

    // ✅ Ignore Vite raw imports (e.g., version.txt?raw)
    if (importPath.includes("?raw")) continue;

    const resolved = path.resolve(path.dirname(filePath), importPath);

    if (!fileExists(resolved)) {
      broken.push({
        file: filePath,
        importPath,
        resolved
      });
    }
  }
}

console.log("🔍 Scanning for broken imports...");
scanDir(ROOT);

if (broken.length === 0) {
  console.log("✅ No broken imports found.");
  process.exit(0);
}

console.log("❌ Broken imports detected:");
for (const b of broken) {
  console.log(`\nFile: ${b.file}`);
  console.log(`Import: ${b.importPath}`);
  console.log(`Resolved: ${b.resolved}`);
}

process.exit(1);
