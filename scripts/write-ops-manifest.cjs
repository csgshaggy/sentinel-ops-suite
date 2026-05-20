#!/usr/bin/env node
import fs from "fs";
import path from "path";

const repoRoot = process.cwd();
const manifestPath = path.join(repoRoot, ".ops", "manifest.json");

console.log("📝 Writing .ops/manifest.json...");

const manifest = {
  generatedAt: new Date().toISOString(),
  tools: {
    makeTargets: [
      "backend",
      "frontend",
      "health",
      "lint",
      "test",
      "drift",
      "sync",
      "governance",
      "repo-health",
      "validate-makefile",
      "repo-structure-checksum",
      "drift-ci",
      "ops-health",
      "ops-bootstrap",
      "clean"
    ],
    scripts: {
      sync: "sync.sh",
      preSyncValidator: "scripts/sync/pre-sync-validate.cjs",
      postSyncHealth: "scripts/sync/post-sync-health-snapshot.cjs",
      postSyncGovernance: "scripts/sync/post-sync-governance.cjs",
      validateMakefile: "scripts/ops/validate-makefile.cjs",
      repoStructureChecksum: "scripts/ops/repo-structure-checksum.cjs",
      driftDetector: "scripts/ops/drift-detector.cjs",
      writeOpsManifest: "scripts/ops/write-ops-manifest.cjs",
      selfHeal: "ops/self-heal.sh"
    }
  }
};

if (!fs.existsSync(path.dirname(manifestPath))) {
  fs.mkdirSync(path.dirname(manifestPath), { recursive: true });
}

fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));

console.log(`✅ Manifest written to ${manifestPath}`);
