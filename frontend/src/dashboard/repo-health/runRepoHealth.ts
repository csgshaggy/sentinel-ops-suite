/**
 * runRepoHealth.ts
 * -----------------
 * Aggregates all RepoHealth collectors into a single JSON output.
 */

import { collectMfaHealth } from "./collectors/collectMfaHealth";
import { collectDocsHealth } from "./collectors/collectDocsHealth";
import { collectStructureHealth } from "./collectors/collectStructureHealth";
import { collectDepsHealth } from "./collectors/collectDepsHealth";
import { collectMakefileHealth } from "./collectors/collectMakefileHealth";
import { collectSyncHistory } from "./collectors/collectSyncHistory";

async function run() {
  const results = {
    mfa: await collectMfaHealth(),
    docs: await collectDocsHealth(),
    structure: await collectStructureHealth(),
    deps: await collectDepsHealth(),
    makefile: await collectMakefileHealth(),
    syncHistory: await collectSyncHistory(),
  };

  console.log(JSON.stringify(results, null, 2));
}

run();
