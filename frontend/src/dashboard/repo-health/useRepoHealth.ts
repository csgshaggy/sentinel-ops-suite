/**
 * Repo Health Aggregator
 * ----------------------
 * Collects all subsystem health signals and produces a unified
 * repo-level health object consumed by:
 *  - RepoHealthPanel
 *  - GovernanceSummary
 *  - RepoHealthScore
 *  - DashboardHome
 */

import { collectCiHealth } from "./collectors/collectCiHealth";
import { collectDocsHealth } from "./collectors/collectDocsHealth";
import { collectDependencyHealth } from "./collectors/collectDependencyHealth";
import { collectGovernanceHealth } from "./collectors/collectGovernanceHealth";
import { collectMfaHealth } from "./collectors/collectMfaHealth";
import { collectMakefileHealth } from "./collectors/collectMakefileHealth";

/**
 * Utility: average numeric values
 */
function average(values: number[]) {
  const valid = values.filter((v) => typeof v === "number");
  return valid.reduce((a, b) => a + b, 0) / valid.length;
}

/**
 * Main Repo Health Aggregator
 */
export async function useRepoHealth() {
  const [
    ci,
    docs,
    deps,
    governance,
    mfa,
    makefile, // ← NEW
  ] = await Promise.all([
    collectCiHealth(),
    collectDocsHealth(),
    collectDependencyHealth(),
    collectGovernanceHealth(),
    collectMfaHealth(),
    collectMakefileHealth(), // ← NEW
  ]);

  return {
    ci,
    docs,
    deps,
    governance,
    mfa,
    makefile, // ← NEW

    overallScore: average([
      ci.score,
      docs.score,
      deps.score,
      governance.score,
      mfa.score,
      makefile.score, // ← NEW
    ]),
  };
}
