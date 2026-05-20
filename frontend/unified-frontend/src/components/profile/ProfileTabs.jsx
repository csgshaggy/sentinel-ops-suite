import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./ProfileTabs.css";

export default function ProfileTabs({ tabs }) {
  const navigate = useNavigate();
  const location = useLocation();

  // Extract ?tab=xyz from URL
  const params = new URLSearchParams(location.search);
  const initialTab = params.get("tab") || Object.keys(tabs)[0];

  const [active, setActive] = useState(initialTab);
  const [animating, setAnimating] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  // Sync tab → URL
  const switchTab = (key) => {
    setAnimating(true);
    setActive(key);
    navigate(`?tab=${key.toLowerCase()}`);
    setTimeout(() => setAnimating(false), 250);
    setMobileOpen(false);
  };

  // Sync URL → tab
  useEffect(() => {
    const urlTab = params.get("tab");
    if (urlTab && tabs[urlTab.charAt(0).toUpperCase() + urlTab.slice(1)]) {
      setActive(urlTab.charAt(0).toUpperCase() + urlTab.slice(1));
    }
  }, [location.search]);

  return (
    <div className="profile-tabs-container">
      {/* Mobile toggle */}
      <button
        className="profile-tabs-mobile-toggle"
        onClick={() => setMobileOpen((prev) => !prev)}
      >
        ☰ {active}
      </button>

      <div className={`profile-tabs-bar ${mobileOpen ? "open" : ""}`}>
        {Object.keys(tabs).map((key) => (
          <button
            key={key}
            className={`profile-tab-button ${
              active === key ? "active" : ""
            }`}
            onClick={() => switchTab(key)}
          >
            <span className="profile-tab-icon">
              {key === "Avatar" && "🖼️"}
              {key === "Account" && "👤"}
              {key === "MFA" && "🔐"}
              {key === "Security" && "⚙️"}
            </span>
            {key}
          </button>
        ))}
      </div>

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
