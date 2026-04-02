/**
 * runRepoHealth.ts
 * -----------------
 * Aggregates all RepoHealth collectors into a single JSON output.
 * Node 24 + ts-node requires explicit .ts extensions.
 */

import { collectMfaHealth } from "./collectors/collectMfaHealth.ts";
import { collectDocsHealth } from "./collectors/collectDocsHealth.ts";
import { collectStructureHealth } from "./collectors/collectStructureHealth.ts";
import { collectDepsHealth } from "./collectors/collectDepsHealth.ts";
import { collectMakefileHealth } from "./collectors/collectMakefileHealth.ts";
import { collectSyncHistory } from "./collectors/collectSyncHistory.ts";

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
