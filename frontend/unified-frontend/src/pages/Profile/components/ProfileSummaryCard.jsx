import { useAvatarContext } from "../../context/AvatarContext";
// /src/pages/Profile/components/ProfileSummaryCard.jsx
// SentinelOps — Profile Summary Card (Neon‑Glassy + Global Avatar Cache‑Buster)

import MFAStatusBadge from "./MFAStatusBadge.jsx";
import "./ProfileSummaryCard.css";

export default function ProfileSummaryCard({ profile }) {
  const { avatarUrl } = useAvatarContext();
  if (!profile) return null;

  const {
    username,
    email,
    role,
    last_login,
    last_login_ip,
  } = profile;

  // 🔥 Global avatar cache‑buster hook

  return (
    <div className="profile-summary-card glass">
      <div className="profile-summary-left">
        <img
          src={avatarUrl}   // <-- FIXED: uses global cache‑buster
          alt="Avatar"
          className="profile-summary-avatar"
        />
      </div>

      <div className="profile-summary-right">
        <div className="profile-summary-header">
          <h2 className="profile-summary-name">{username}</h2>
          <MFAStatusBadge enabled={profile.mfa_enabled} />
        </div>

        <div className="profile-summary-info">
          <div className="profile-summary-row">
            <span className="label">Email:</span>
            <span className="value">{email}</span>
          </div>

          <div className="profile-summary-row">
            <span className="label">Role:</span>
            <span className="value role">{role}</span>
          </div>

          {last_login && (
            <div className="profile-summary-row">
              <span className="label">Last Login:</span>
              <span className="value">
                {new Date(last_login).toLocaleString()}
              </span>
            </div>
          )}

          {last_login_ip && (
            <div className="profile-summary-row">
              <span className="label">IP Address:</span>
              <span className="value">{last_login_ip}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
