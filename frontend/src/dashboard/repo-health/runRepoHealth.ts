// File: src/dashboard/repo-health/runRepoHealth.ts

import { collectDepsHealth } from "./collectors/collectDepsHealth";
import { collectDocsHealth } from "./collectors/collectDocsHealth";
import { collectMakefileHealth } from "./collectors/collectMakefileHealth";
import { collectStructureHealth } from "./collectors/collectStructureHealth";
import { collectSyncHistory } from "./collectors/collectSyncHistory";
import { computeRepoHealthSummary } from "./computeRepoHealthSummary";

export async function runRepoHealth() {
  const results = {
    dependencies: await collectDepsHealth(),
    docs: await collectDocsHealth(),
    makefile: await collectMakefileHealth(),
    structure: await collectStructureHealth(),
    syncHistory: await collectSyncHistory(),
  };

  return computeRepoHealthSummary(results);
}
