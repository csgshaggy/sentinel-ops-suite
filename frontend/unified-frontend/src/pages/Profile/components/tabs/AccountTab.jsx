// /src/pages/Profile/components/tabs/AccountTab.jsx
// SentinelOps — Account Tab (Email, Username, Role)

import { useState } from "react";
import "./AccountTab.css";

export default function AccountTab({ profile, onChange }) {
  const [local, setLocal] = useState({
    email: profile.email || "",
    username: profile.username || "",
    role: profile.role || "",
  });

  const update = (field, value) => {
    const updated = { ...local, [field]: value };
    setLocal(updated);
    onChange(updated);
  };

  return (
    <div className="account-tab-container">
      <div className="form-group">
        <label className="form-label">Email</label>
        <input
          className="form-input"
          type="email"
          value={local.email}
          onChange={(e) => update("email", e.target.value)}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Username</label>
        <input
          className="form-input"
          type="text"
          value={local.username}
          onChange={(e) => update("username", e.target.value)}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Role</label>
        <input
          className="form-input"
          type="text"
          value={local.role}
          disabled
        />
      </div>
    </div>
  );
}
