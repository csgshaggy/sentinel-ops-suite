import React, { useState } from "react";
import { useGovernanceSnapshot } from "../../hooks/useGovernanceSnapshot";
import { SnapshotDrawer } from "./SnapshotDrawer";

export const SnapshotTab = ({ runId }) => {
  const { data, loading, error } = useGovernanceSnapshot(runId);
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);

  if (loading) return <div>Loading snapshot…</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>No snapshot found.</div>;

  return (
    <div className="snapshot-tab">
      <h2>Snapshot for Run #{data.run_id}</h2>

      <table>
        <thead>
          <tr>
            <th>Workflow</th>
            <th>Status</th>
            <th>Violations</th>
          </tr>
        </thead>
        <tbody>
          {data.workflows.map((wf) => (
            <tr key={wf.workflow_id} onClick={() => setSelectedWorkflow(wf)}>
              <td>{wf.path}</td>
              <td>{wf.status}</td>
              <td>{wf.violations.length}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <SnapshotDrawer
        workflow={selectedWorkflow}
        onClose={() => setSelectedWorkflow(null)}
      />
    </div>
  );
};
