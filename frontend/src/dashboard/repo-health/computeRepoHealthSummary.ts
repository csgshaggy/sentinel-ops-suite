// File: src/dashboard/repo-health/computeRepoHealthSummary.ts

export function computeRepoHealthSummary(results) {
  return {
    makefile: results.makefile?.status ?? "unknown",
    structure: results.structure?.status ?? "unknown",
    dependencies: results.dependencies?.status ?? "unknown",
    docs: results.docs?.status ?? "unknown",
    syncHistory: results.syncHistory?.status ?? "unknown",
  };
}
