#!/usr/bin/env node

/**
 * Sentinel Ops Suite — Makefile Drift Detector (Ultra Local Edition)
 * Features:
 *   - Drift detection
 *   - Optional strict mode (--strict or STRICT=1)
 *   - Optional quiet mode (--quiet)
 *   - Optional no-diff mode (--no-diff)
 *   - Baseline update (--update)
 *   - Baseline history archiving
 */

import fs from "fs";
import { execSync } from "child_process";

const args = process.argv.slice(2);

const shouldUpdate = args.includes("--update");
const strictMode = args.includes("--strict") || process.env.STRICT === "1";
const quietMode = args.includes("--quiet");
const noDiff = args.includes("--no-diff");

const baselineDir = ".meta/makefile";
const historyDir = `${baselineDir}/history`;
const baselinePath = `${baselineDir}/Makefile.baseline`;
const makefilePath = "Makefile";

fs.mkdirSync(baselineDir, { recursive: true });
fs.mkdirSync(historyDir, { recursive: true });

// ------------------------------------------------------------
// Update baseline mode
// ------------------------------------------------------------
if (shouldUpdate) {
    if (!quietMode) console.log("📌 Updating Makefile baseline...");

    if (fs.existsSync(baselinePath)) {
        const timestamp = new Date().toISOString().replace(/[-:T]/g, "").slice(0, 15);
        const backupPath = `${historyDir}/Makefile.${timestamp}.bak`;
        fs.copyFileSync(baselinePath, backupPath);
        if (!quietMode) console.log(`🗄️ Archived previous baseline → ${backupPath}`);
    }

    fs.copyFileSync(makefilePath, baselinePath);
    if (!quietMode) console.log("✅ Baseline updated.");
    process.exit(0);
}

// ------------------------------------------------------------
// Drift detection mode
// ------------------------------------------------------------
if (!fs.existsSync(baselinePath)) {
    if (!quietMode) console.log("ℹ️ No baseline found. Creating initial Makefile baseline...");
    fs.copyFileSync(makefilePath, baselinePath);
    if (!quietMode) console.log("✅ Baseline created.");
    process.exit(0);
}

let driftDetected = false;

try {
    execSync(`diff -u ${baselinePath} ${makefilePath}`, { stdio: "pipe" });
    if (!quietMode) console.log("✅ No Makefile drift detected.");
} catch (err) {
    driftDetected = true;
    if (!quietMode) console.log("⚠️ Makefile drift detected.");

    if (!quietMode && !noDiff) {
        try {
            execSync(`diff -u ${baselinePath} ${makefilePath}`, { stdio: "inherit" });
        } catch (_) {}
    }
}

if (driftDetected && strictMode) {
    if (!quietMode) console.log("❌ Strict mode enabled — exiting due to drift.");
    process.exit(1);
}

process.exit(0);
