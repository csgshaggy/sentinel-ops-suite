// /src/components/profile/ProfileTabs.jsx
// SentinelOps — Profile Tabs (URL‑Synced + Mobile‑Safe + Neon‑Glassy)

import React, { useState, useEffect, useMemo } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./ProfileTabs.css";

export default function ProfileTabs({ tabs }) {
  const navigate = useNavigate();
  const location = useLocation();

  // ------------------------------------------------------------
  // Normalize tab keys (Avatar → avatar)
  // ------------------------------------------------------------
  const normalizedTabs = useMemo(() => {
    const map = {};
    Object.keys(tabs).forEach((key) => {
      map[key.toLowerCase()] = key; // "avatar" → "Avatar"
    });
    return map;
  }, [tabs]);

  const tabKeys = Object.keys(tabs); // ["Avatar", "Account", "MFA", "Security"]

  // ------------------------------------------------------------
  // Determine initial tab from URL or fallback
  // ------------------------------------------------------------
  const params = new URLSearchParams(location.search);
  const urlTab = params.get("tab")?.toLowerCase();

  const initialTab =
    normalizedTabs[urlTab] || tabKeys[0]; // fallback to first tab

  const [active, setActive] = useState(initialTab);
  const [animating, setAnimating] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  // ------------------------------------------------------------
  // Switch tab → update URL + animate
  // ------------------------------------------------------------
  const switchTab = (key) => {
    const lower = key.toLowerCase();

    setAnimating(true);
    setActive(key);

    navigate(`?tab=${lower}`, { replace: true });

    setTimeout(() => setAnimating(false), 220);
    setMobileOpen(false);
  };

  // ------------------------------------------------------------
  // URL changed → sync active tab
  // ------------------------------------------------------------
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const urlTab = params.get("tab")?.toLowerCase();

    if (urlTab && normalizedTabs[urlTab]) {
      const properCase = normalizedTabs[urlTab];
      if (properCase !== active) {
        setActive(properCase);
      }
    }
  }, [location.search, normalizedTabs, active]);

  // ------------------------------------------------------------
  // Tab icons
  // ------------------------------------------------------------
  const icons = {
    avatar: "🖼️",
    account: "👤",
    mfa: "🔐",
    security: "⚙️",
  };

  return (
    <div className="profile-tabs-container">
      {/* MOBILE TOGGLE */}
      <button
        className="profile-tabs-mobile-toggle"
        onClick={() => setMobileOpen((prev) => !prev)}
      >
        ☰ {active}
      </button>

      {/* TAB BAR */}
      <div className={`profile-tabs-bar ${mobileOpen ? "open" : ""}`}>
        {tabKeys.map((key) => {
          const lower = key.toLowerCase();
          return (
            <button
              key={key}
              className={`profile-tab-button ${
                active === key ? "active" : ""
              }`}
              onClick={() => switchTab(key)}
            >
              <span className="profile-tab-icon">
                {icons[lower] || "•"}
              </span>
              {key}
            </button>
          );
        })}
      </div>

      {/* TAB CONTENT */}
      <div
        className={`profile-tab-content ${
          animating ? "fade-in" : ""
        }`}
      >
        {tabs[active]}
      </div>
    </div>
  );
}
