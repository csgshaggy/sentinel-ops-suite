import React from "react";

interface SyncHistoryEntry {
  timestamp: string;
  score: number;
  detail: any;
}

interface Props {
  entries: SyncHistoryEntry[];
}

export function SyncHistoryTile({ entries }: Props) {
  return (
    <div className="tile">
      <h2>Sync History</h2>

      {entries.length === 0 && (
        <p>No sync snapshots found.</p>
      )}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {entries.map((entry, idx) => (
          <li
            key={idx}
            style={{
              marginBottom: "1rem",
              padding: "0.75rem",
              border: "1px solid #ccc",
              borderRadius: "6px",
            }}
          >
            <strong>{entry.timestamp}</strong>
            <div>Score: {entry.score}</div>

            <details style={{ marginTop: "0.5rem" }}>
              <summary>Details</summary>
              <pre style={{ fontSize: "0.8rem" }}>
                {JSON.stringify(entry.detail, null, 2)}
              </pre>
            </details>
          </li>
        ))}
      </ul>
    </div>
  );
}
