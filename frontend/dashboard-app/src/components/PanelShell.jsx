import React from "react";
import "./../styles/panel-shell.css";

export default function PanelShell({ title, description, children }) {
  return (
    <div className="panel-shell glassy-panel">

      {/* HEADER */}
      <div className="panel-header">
        <h2 className="panel-title">{title}</h2>
        {description && (
          <p className="panel-description">{description}</p>
        )}
      </div>

      {/* CONTENT */}
      <div className="panel-content">
        {children}
      </div>

    </div>
  );
}
