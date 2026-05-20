import React from "react";
import PanelShell from "../components/PanelShell.jsx";

export default function GitHealthPanel() {
  return (
    <PanelShell
      title="Git Health"
      description="Commit hygiene & branch stability"
    >
      <div className="panel-section">
        <h3 className="section-title">Overview</h3>
        <p className="section-desc">
          This module will surface commit hygiene metrics, branch stability
          indicators, merge‑conflict risk, and repository activity signals.
        </p>
      </div>

      <div className="panel-grid">

        <div className="panel-widget glassy-panel">
          <h4 className="widget-title">Commit Hygiene</h4>
          <p className="widget-placeholder">[Commit audit placeholder]</p>
        </div>

        <div className="panel-widget glassy-panel">
          <h4 className="widget-title">Branch Stability</h4>
          <p className="widget-placeholder">[Branch analysis placeholder]</p>
        </div>

        <div className="panel-widget glassy-panel">
          <h4 className="widget-title">Merge Conflict Risk</h4>
          <p className="widget-placeholder">[Risk model placeholder]</p>
        </div>

        <div className="panel-widget glassy-panel">
          <h4 className="widget-title">Repo Activity</h4>
          <p className="widget-placeholder">[Activity timeline placeholder]</p>
        </div>

      </div>
    </PanelShell>
  );
}
