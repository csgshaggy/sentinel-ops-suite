import React from "react";
import "./SnapshotDrawer.css";

export const SnapshotDrawer = ({ workflow, onClose }) => {
  if (!workflow) return null;

  return (
    <div className="snapshot-drawer">
      <div className="drawer-content">
        <button className="close-btn" onClick={onClose}>Close</button>

        <h2>Workflow: {workflow.path}</h2>
        <p>Status: {workflow.status}</p>

        <h3>Violations</h3>
        {workflow.violations.length === 0 && <p>No violations.</p>}

        <ul>
          {workflow.violations.map((v, idx) => (
            <li key={idx}>
              <strong>{v.rule_id}</strong> — {v.message}
              <br />
              Severity: {v.severity}
              <br />
              File: {v.file_path}
              {v.line && <> (line {v.line})</>}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
