#!/usr/bin/env node
// SentinelOps — Frontend Theme Token Validator (Primary)

import fs from "fs";
import path from "path";
import url from "url";

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));

const ROOT = path.resolve(__dirname, "..");
const TOKENS_FILE = path.join(ROOT, "src", "styles", "tokens.css");
const MODULES_DIR = path.join(ROOT, "src");

const REQUIRED_TOKENS = [
  "--so-color-bg",
  "--so-color-surface",
  "--so-color-accent",
  "--so-color-accent-soft",
  "--so-color-border-subtle",
  "--so-radius-md",
  "--so-radius-lg",
  "--so-shadow-soft",
];

function readFileSafe(p) {
  try {
    return fs.readFileSync(p, "utf8");
  } catch {
    return null;
  }
}

function validateTokensDefined() {
  const content = readFileSafe(TOKENS_FILE);
  if (!content) {
    console.error(`ERROR: tokens file missing: ${TOKENS_FILE}`);
    process.exit(1);
  }

  let ok = true;
  for (const token of REQUIRED_TOKENS) {
    if (!content.includes(token)) {
      console.error(`MISSING TOKEN DEFINITION: ${token}`);
      ok = false;
    } else {
      console.log(`OK: ${token}`);
    }
  }

  if (!ok) {
    console.error("Theme token validation failed.");
    process.exit(1);
  }
}

function scanModulesForUsage() {
  const exts = [".css", ".jsx", ".tsx", ".js", ".ts"];

  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(full);
      } else if (exts.some((e) => entry.name.endsWith(e))) {
        const content = readFileSafe(full);
        if (!content) continue;

        for (const token of REQUIRED_TOKENS) {
          if (content.includes(token)) {
            console.log(`USAGE: ${token} -> ${path.relative(ROOT, full)}`);
          }
        }
      }
    }
  }

  walk(MODULES_DIR);
}

console.log("=== SentinelOps Theme Token Validator (Primary) ===");
validateTokensDefined();
scanModulesForUsage();
console.log("=== Theme token validation complete ===");
