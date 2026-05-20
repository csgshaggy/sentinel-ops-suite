import React from "react";
import PanelShell from "../components/PanelShell.jsx";

export default function PELMPanel() {
  return (
    <PanelShell
      title="PELM Panel"
      description="Privilege Escalation & Lateral Movement"
    >
      <div className="panel-section">
        <h3 className="section-title">Overview</h3>
        <p className="section-desc">
          This module will visualize privilege escalation paths, lateral movement
          opportunities, and identity exposure surfaces across your environment.
        </p>
      </div>

      <div className="panel-grid">

        <div className="panel-widget glassy-panel">
          <h4 className="widget-title">High-Risk Accounts</h4>
          <p className="widget-placeholder">[Data pending backend integration]</p>
        </div>

        <div className="panel-widget glassy-panel">
          <h4 className="widget-title">Lateral Movement Paths</h4>
          <p className="widget-placeholder">[Graph view placeholder]</p>
        </div>

        <div className="panel-widget glassy-panel">
          <h4 className="widget-title">Privilege Escalation Chains</h4>
          <p className="widget-placeholder">[Chain analysis placeholder]</p>
        </div>

        <div className="panel-widget glassy-panel">
          <h4 className="widget-title">Identity Exposure Score</h4>
          <p className="widget-placeholder">[Scorecard placeholder]</p>
        </div>

      </div>
    </PanelShell>
  );
}
