// /src/pages/Profile/components/tabs/PersonalInfoTab.jsx
// SentinelOps — Personal Info Tab (Full Name, Email, Optional Fields)

import { useState } from "react";
import "./PersonalInfoTab.css";

export default function PersonalInfoTab({ profile }) {
  // Your backend only provides: full_name, email, role, avatar_url, mfa_enabled
  // So we map safely and allow optional fields for future expansion.

  const [local, setLocal] = useState({
    full_name: profile.full_name || "",
    email: profile.email || "",
    phone: profile.phone || "",          // optional — backend may add later
    location: profile.location || "",    // optional
    bio: profile.bio || "",              // optional
  });

  const update = (field, value) => {
    setLocal((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <div className="personal-info-tab-container">

      {/* Full Name */}
      <div className="form-group">
        <label className="form-label">Full Name</label>
        <input
          className="form-input"
          type="text"
          value={local.full_name}
          onChange={(e) => update("full_name", e.target.value)}
        />
      </div>

      {/* Email */}
      <div className="form-group">
        <label className="form-label">Email</label>
        <input
          className="form-input"
          type="email"
          value={local.email}
          onChange={(e) => update("email", e.target.value)}
        />
      </div>

      {/* Phone (optional) */}
      <div className="form-group">
        <label className="form-label">Phone</label>
        <input
          className="form-input"
          type="text"
          value={local.phone}
          onChange={(e) => update("phone", e.target.value)}
        />
      </div>

      {/* Location (optional) */}
      <div className="form-group">
        <label className="form-label">Location</label>
        <input
          className="form-input"
          type="text"
          value={local.location}
          onChange={(e) => update("location", e.target.value)}
        />
      </div>

      {/* Bio (optional) */}
      <div className="form-group">
        <label className="form-label">Bio</label>
        <textarea
          className="form-textarea"
          value={local.bio}
          onChange={(e) => update("bio", e.target.value)}
        />
      </div>
    </div>
  );
}
