// ============================================================
// FILE: src/components/auth/UnifiedAuthShell.jsx
// SentinelOps Glassy Neon Auth Shell (Complete)
// ============================================================

import React from "react";
import "./UnifiedAuthShell.css";

export default function UnifiedAuthShell({ title, children, footer }) {
  return (
    <div className="auth-shell">
      <div className="auth-card">

        {/* TITLE */}
        {title && <h1 className="auth-title">{title}</h1>}

        {/* MAIN CONTENT */}
        <div className="auth-content">
          {children}
        </div>

        {/* OPTIONAL FOOTER (links, legal text, etc.) */}
        {footer && (
          <div className="auth-footer">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
}

