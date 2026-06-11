import React from "react";
import { useGovernanceHistory } from "../../hooks/useGovernanceHistory";

interface Props {
  repoId: number;
}

export const HistoryTab: React.FC<Props> = ({ repoId }) => {
  const { data, loading, error } = useGovernanceHistory(repoId);

  if (loading) return <div>Loading history…</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data || data.runs.length === 0) return <div>No history found.</div>;

  return (
    <div className="history-table">
      <table>
        <thead>
          <tr>
            <th>Run ID</th>
            <th>Status</th>
            <th>Score</th>
            <th>Violations</th>
            <th>Triggered</th>
            <th>Completed</th>
          </tr>
        </thead>
        <tbody>
          {data.runs.map((run) => (
            <tr key={run.run_id}>
              <td>{run.run_id}</td>
              <td>{run.status}</td>
              <td>{run.score}</td>
              <td>{run.violations_count}</td>
              <td>{new Date(run.triggered_at).toLocaleString()}</td>
              <td>
                {run.completed_at
                  ? new Date(run.completed_at).toLocaleString()
                  : "—"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
