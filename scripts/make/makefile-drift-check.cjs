#!/usr/bin/env node

/**
 * Sentinel Ops Suite — Makefile Drift Detector (Ultra Local Edition, CJS Version)
 */

const fs = require("fs");
const { execSync } = require("child_process");

const args = process.argv.slice(2);

const shouldUpdate = args.includes("--update");
const strictMode = args.includes("--strict") || process.env.STRICT === "1";
const quietMode = args.includes("--quiet");
const noDiff = args.includes("--no-diff");
const jsonMode = args.includes("--json");
const statusOnly = args.includes("--status-only");
const listHistory = args.includes("--history");

const baselineDir = ".meta/makefile";
const historyDir = `${baselineDir}/history`;
const baselinePath = `${baselineDir}/Makefile.baseline`;
const makefilePath = "Makefile";

fs.mkdirSync(baselineDir, { recursive: true });
fs.mkdirSync(historyDir, { recursive: true });

// ------------------------------------------------------------
// List baseline history
// ------------------------------------------------------------
if (listHistory) {
    const files = fs.readdirSync(historyDir).filter(f => f.startsWith("Makefile."));
    if (jsonMode) {
        console.log(JSON.stringify(files, null, 2));
    } else {
        console.log("📜 Baseline History:");
        files.forEach(f => console.log(" - " + f));
    }
    process.exit(0);
}

// ------------------------------------------------------------
// Update baseline
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
// Drift detection
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
    if (!quietMode && !statusOnly) console.log("✅ No Makefile drift detected.");
} catch (err) {
    driftDetected = true;

    if (!quietMode && !statusOnly) console.log("⚠️ Makefile drift detected.");

    if (!quietMode && !noDiff && !statusOnly) {
        try {
            execSync(`diff -u ${baselinePath} ${makefilePath}`, { stdio: "inherit" });
        } catch (_) {}
    }
}

if (jsonMode) {
    console.log(JSON.stringify({ drift: driftDetected }, null, 2));
}

if (driftDetected && strictMode) process.exit(1);
if (statusOnly) process.exit(driftDetected ? 1 : 0);

process.exit(0);
