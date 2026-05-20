// File: src/dashboard/repo-health/tiles/RepoHealthSummaryTile.tsx

import { useEffect, useState } from "react";
import { runRepoHealth } from "../runRepoHealth";

export default function RepoHealthSummaryTile() {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    runRepoHealth().then(setSummary);
  }, []);

  if (!summary) return <div className="tile">Loading repo health…</div>;

  return (
    <div className="tile">
      <h3>Repo Health</h3>
      <ul>
        <li>Makefile: {summary.makefile}</li>
        <li>Structure: {summary.structure}</li>
        <li>Dependencies: {summary.dependencies}</li>
        <li>Docs: {summary.docs}</li>
        <li>Sync History: {summary.syncHistory}</li>
      </ul>
    </div>
  );
}
