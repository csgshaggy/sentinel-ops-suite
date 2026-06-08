// /src/pages/Profile/components/AvatarUploadProgress.jsx
// SentinelOps — Avatar Upload Progress (Neon‑Glassy, Pipeline‑Ready)

import "./AvatarUploadProgress.css";

export default function AvatarUploadProgress({ progress }) {
  // Clamp progress safely (handles undefined/null)
  const pct = Math.min(100, Math.max(0, progress ?? 0));

  return (
    <div className="avatar-upload-progress glass">
      <div className="avatar-upload-bar">
        <div
          className="avatar-upload-bar-fill"
          style={{ width: `${pct}%` }}
          aria-valuenow={pct}
          aria-valuemin={0}
          aria-valuemax={100}
          role="progressbar"
        />
      </div>

      <div className="avatar-upload-label">
        Uploading… {pct}%
      </div>
    </div>
  );
}
