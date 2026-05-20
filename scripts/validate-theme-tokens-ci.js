#!/usr/bin/env node
// SentinelOps — Frontend Theme Token Validator (CI Mode)

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

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

function validate() {
  if (!fs.existsSync(TOKENS_FILE)) {
    fail(`ERROR: tokens file missing: ${TOKENS_FILE}`);
  }

  const content = fs.readFileSync(TOKENS_FILE, "utf8");
  const missing = REQUIRED_TOKENS.filter((t) => !content.includes(t));

  if (missing.length > 0) {
    console.error("Missing theme tokens:");
    for (const t of missing) console.error(`  - ${t}`);
    fail("Theme token CI validation failed.");
  }

  // Optional: enforce no hard-coded colors in modules
  const forbiddenPatterns = [/#[0-9a-fA-F]{3,8}\b/g];
  const exts = [".css", ".jsx", ".tsx"];

  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(full);
      } else if (exts.some((e) => entry.name.endsWith(e))) {
        const c = fs.readFileSync(full, "utf8");
        for (const pattern of forbiddenPatterns) {
          if (pattern.test(c)) {
            fail(
              `Forbidden hard-coded color in: ${path.relative(
                ROOT,
                full
              )} (use tokens instead)`
            );
          }
        }
      }
    }
  }

  walk(MODULES_DIR);
}

console.log("=== SentinelOps Theme Token Validator (CI) ===");
validate();
console.log("=== Theme token CI validation passed ===");
