import React, { useEffect, useState } from "react";

import { collectRepoHealth } from "../dashboard/repo-health/collectRepoHealth";

import { RepoHealthSummaryTile } from "../dashboard/repo-health/tiles/RepoHealthSummaryTile";
import { MakefileHealthTile } from "../dashboard/repo-health/tiles/MakefileHealthTile";
import { SyncHistoryTile } from "../dashboard/repo-health/tiles/SyncHistoryTile";

import { computeRepoHealthSummary } from "../dashboard/repo-health/computeRepoHealthSummary";

export default function DashboardHome() {
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    async function load() {
      const data = await collectRepoHealth();
      setHealth(data);
    }
    load();
  }, []);

  if (!health) {
    return <div>Loading dashboard…</div>;
  }

  const summary = computeRepoHealthSummary(health);

  return (
    <div className="dashboard-grid">

      {/* -------------------------------- */}
      {/* Repo Health Section              */}
      {/* -------------------------------- */}
      <div className="dashboard-section">
        <h1>Repository Health</h1>

        {/* Summary Tile */}
        <RepoHealthSummaryTile
          score={summary.score}
          status={summary.status}
          breakdown={summary.breakdown}
        />

        {/* Makefile Health */}
        <MakefileHealthTile data={health.makefile} />

        {/* Sync History */}
        <SyncHistoryTile entries={health.syncHistory?.entries || []} />
      </div>

    </div>
  );
}
