// /src/pages/Profile/components/tabs/PreferencesTab.jsx
// SentinelOps — Full Preferences Suite (Theme, Accent, Timezone, Language, Notifications, Session Timeout)

import { useState } from "react";
import "./PreferencesTab.css";

export default function PreferencesTab({ profile }) {
  // Backend does NOT provide these yet, so we create safe defaults.
  const [prefs, setPrefs] = useState({
    theme: profile.theme || "system",
    accent: profile.accent || "cyan",
    timezone: profile.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone,
    language: profile.language || "en",

    notifications: {
      login_alerts: profile.notifications?.login_alerts ?? true,
      security_warnings: profile.notifications?.security_warnings ?? true,
      product_updates: profile.notifications?.product_updates ?? false,
    },

    session_timeout: profile.session_timeout || 15, // minutes
  });

  const update = (field, value) => {
    setPrefs((prev) => ({ ...prev, [field]: value }));
  };

  const updateNested = (group, field, value) => {
    setPrefs((prev) => ({
      ...prev,
      [group]: { ...prev[group], [field]: value },
    }));
  };

  return (
    <div className="preferences-tab-container">

      {/* -------------------------------------------------------
         THEME
      -------------------------------------------------------- */}
      <div className="pref-section">
        <h3 className="pref-title">Theme</h3>
        <select
          className="pref-select"
          value={prefs.theme}
          onChange={(e) => update("theme", e.target.value)}
        >
          <option value="system">System Default</option>
          <option value="dark">Dark Mode</option>
          <option value="light">Light Mode</option>
          <option value="neon">Neon‑Glassy</option>
        </select>
      </div>

      {/* -------------------------------------------------------
         ACCENT COLOR
      -------------------------------------------------------- */}
      <div className="pref-section">
        <h3 className="pref-title">Accent Color</h3>
        <select
          className="pref-select"
          value={prefs.accent}
          onChange={(e) => update("accent", e.target.value)}
        >
          <option value="cyan">Cyan</option>
          <option value="blue">Blue</option>
          <option value="purple">Purple</option>
          <option value="green">Green</option>
          <option value="red">Red</option>
        </select>
      </div>

      {/* -------------------------------------------------------
         TIMEZONE
      -------------------------------------------------------- */}
      <div className="pref-section">
        <h3 className="pref-title">Timezone</h3>
        <select
          className="pref-select"
          value={prefs.timezone}
          onChange={(e) => update("timezone", e.target.value)}
        >
          {Intl.supportedValuesOf("timeZone").map((tz) => (
            <option key={tz} value={tz}>
              {tz}
            </option>
          ))}
        </select>
      </div>

      {/* -------------------------------------------------------
         LANGUAGE
      -------------------------------------------------------- */}
      <div className="pref-section">
        <h3 className="pref-title">Language</h3>
        <select
          className="pref-select"
          value={prefs.language}
          onChange={(e) => update("language", e.target.value)}
        >
          <option value="en">English</option>
          <option value="es">Spanish</option>
          <option value="fr">French</option>
        </select>
      </div>

      {/* -------------------------------------------------------
         NOTIFICATIONS
      -------------------------------------------------------- */}
      <div className="pref-section">
        <h3 className="pref-title">Notifications</h3>

        <label className="pref-toggle">
          <input
            type="checkbox"
            checked={prefs.notifications.login_alerts}
            onChange={(e) =>
              updateNested("notifications", "login_alerts", e.target.checked)
            }
          />
          Login Alerts
        </label>

        <label className="pref-toggle">
          <input
            type="checkbox"
            checked={prefs.notifications.security_warnings}
            onChange={(e) =>
              updateNested("notifications", "security_warnings", e.target.checked)
            }
          />
          Security Warnings
        </label>

        <label className="pref-toggle">
          <input
            type="checkbox"
            checked={prefs.notifications.product_updates}
            onChange={(e) =>
              updateNested("notifications", "product_updates", e.target.checked)
            }
          />
          Product Updates
        </label>
      </div>

      {/* -------------------------------------------------------
         SESSION TIMEOUT
      -------------------------------------------------------- */}
      <div className="pref-section">
        <h3 className="pref-title">Session Timeout</h3>
        <select
          className="pref-select"
          value={prefs.session_timeout}
          onChange={(e) => update("session_timeout", Number(e.target.value))}
        >
          <option value={5}>5 minutes</option>
          <option value={15}>15 minutes</option>
          <option value={30}>30 minutes</option>
          <option value={60}>1 hour</option>
        </select>
      </div>
    </div>
  );
}

