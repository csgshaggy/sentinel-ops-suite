#!/usr/bin/env node

/**
 * pre-sync-validate.cjs
 * ---------------------
 * Ensures the repository is in a safe state before running sync.sh.
 * Uses CommonJS require() because this file is .cjs.
 */

const { execSync } = require("child_process");
const fs = require("fs");

function run(cmd) {
  return execSync(cmd, { encoding: "utf8" }).toString().trim();
}

function fail(msg) {
  console.error("❌ Pre-sync validation failed:");
  console.error("   " + msg);
  process.exit(1);
}

(function validate() {
  console.log("🔍 Running pre-sync validation...");

  // 1. Ensure Git is available
  try {
    run("git --version");
  } catch {
    fail("Git is not installed or not available in PATH.");
  }

  // 2. Ensure we are inside a Git repo
  try {
    run("git rev-parse --is-inside-work-tree");
  } catch {
    fail("Not inside a Git repository.");
  }

  // 3. Ensure no rebase is in progress
  try {
    const gitDir = run("git rev-parse --git-dir");
    const rebaseApply = `${gitDir}/rebase-apply`;
    const rebaseMerge = `${gitDir}/rebase-merge`;

    if (fs.existsSync(rebaseApply) || fs.existsSync(rebaseMerge)) {
      fail("A rebase is currently in progress. Resolve it before syncing.");
    }
  } catch {}

  // 4. Ensure no merge conflicts
  const conflicts = run("git diff --name-only --diff-filter=U");
  if (conflicts.length > 0) {
    fail("Merge conflicts detected:\n" + conflicts);
  }

  // 5. Ensure working tree is clean (except staged changes)
  const dirty = run("git status --porcelain");
  if (dirty.includes("??")) {
    fail("Untracked files present. Add or remove them before syncing.");
  }

  // 6. Ensure branch is valid
  const branch = run("git rev-parse --abbrev-ref HEAD");
  if (branch === "HEAD") {
    fail("Detached HEAD state. Checkout a branch before syncing.");
  }

  // 7. Ensure remote exists
  const remotes = run("git remote");
  if (!remotes.includes("origin")) {
    fail("Remote 'origin' does not exist.");
  }

  // 8. Ensure branch tracks a remote branch
  try {
    run("git rev-parse --abbrev-ref --symbolic-full-name @{u}");
  } catch {
    fail(`Branch '${branch}' does not track a remote branch.`);
  }

  console.log("✅ Pre-sync validation passed.");
})();
