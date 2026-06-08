// /src/pages/Profile/components/ProfileTabs.jsx
// SentinelOps — Profile Tabs Controller (URL‑Synced + Neon‑Glassy)

import { useMemo } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import "./ProfileTabs.css";

export default function ProfileTabs({ tabs }) {
  const tabNames = useMemo(() => {
    return tabs ? Object.keys(tabs) : [];
  }, [tabs]);

  const [params] = useSearchParams();
  const navigate = useNavigate();

  const activeTab = params.get("tab") || tabNames[0];

  const validTab = useMemo(() => {
    return tabNames.includes(activeTab) ? activeTab : tabNames[0];
  }, [activeTab, tabNames]);

  const setActiveTab = (name) => {
    // ✅ FIX: prevents validator + routing breakage
    navigate(`/profile?tab=${encodeURIComponent(name)}`);
  };

  if (!tabNames.length) {
    return null;
  }

  return (
    <div className="profile-tabs-container">

      <div className="profile-tabs-list">
        {tabNames.map((name) => (
          <button
            key={name}
            type="button"
            className={`profile-tab-button ${
              validTab === name ? "active" : ""
            }`}
            onClick={() => setActiveTab(name)}
          >
            {name}
          </button>
        ))}
      </div>

      <div className="profile-tabs-panel">
        {tabs[validTab]}
      </div>

    </div>
  );
}
