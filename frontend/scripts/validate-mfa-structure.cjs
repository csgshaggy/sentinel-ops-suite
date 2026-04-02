#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");

const required = [
  "src/pages/settings/MfaSettings.tsx",
  "src/pages/settings/MfaEnrollment.tsx",
  "src/pages/settings/MfaChallenge.tsx",
  "src/pages/settings/mfa-router.tsx",
  "src/pages/settings/security/index.tsx",
  "src/components/mfa/TotpInput.tsx",
  "src/features/mfa-query/useEnrollMfa.ts",
  "src/features/mfa-query/useVerifyMfa.ts",
  "src/features/mfa-query/useDisableMfa.ts",
  "src/features/mfa-query/useMfaStatus.ts",
];

let missing = [];

for (const file of required) {
  const full = path.join(root, file);
  if (!fs.existsSync(full)) {
    missing.push(file);
  }
}

if (missing.length > 0) {
  console.error("\n❌ MFA structure validation failed.\nMissing files:");
  missing.forEach((f) => console.error(" - " + f));
  process.exit(1);
}

console.log("✅ MFA structure validated successfully.");
