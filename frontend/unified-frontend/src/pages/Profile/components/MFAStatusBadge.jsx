// /src/pages/Profile/components/MFAStatusBadge.jsx
// SentinelOps — MFA Status Badge (Neon‑Glassy)

import "./MFAStatusBadge.css";

export default function MFAStatusBadge({ enabled }) {
  return (
    <div
      className={
        enabled
          ? "mfa-status-badge enabled glass"
          : "mfa-status-badge disabled glass"
      }
      role="status"
      aria-label={enabled ? "MFA Enabled" : "MFA Disabled"}
      tabIndex={0}
    >
      <span className="mfa-status-icon">
        {enabled ? "🟢" : "🔴"}
      </span>

      <span className="mfa-status-text">
        {enabled ? "MFA Enabled" : "MFA Disabled"}
      </span>
    </div>
  );
}
