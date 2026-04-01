import React from "react";

import { SystemHealthTile } from "../components/SystemHealthTile";
import { WorkflowRunsTile } from "../components/WorkflowRunsTile";
import { GitSnapshotsTile } from "../components/GitSnapshotsTile";
import { MakefileDriftTile } from "../components/MakefileDriftTile";

export const Dashboard: React.FC = () => {
  return (
    <div style={{ padding: "2rem" }}>
      <h1 style={{ marginBottom: "1.5rem" }}>Operator Dashboard</h1>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: "1rem",
          marginBottom: "2rem",
        }}
      >
        <SystemHealthTile />
        <WorkflowRunsTile />
        <GitSnapshotsTile />
        <MakefileDriftTile />
      </div>

      <div style={{ marginTop: "2rem" }}>
        <h2>Details</h2>
        <p>Select a tile above to view deeper diagnostics.</p>
      </div>
    </div>
  );
};

export default Dashboard;
