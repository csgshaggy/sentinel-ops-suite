// /src/pages/Settings.jsx
// SentinelOps — Neon‑Glassy Settings UI (Refactored)

import { useContext } from "react";
import { SettingsContext } from "../context/SettingsContext.jsx";
import "./Settings.css";

export default function SettingsPage() {
  const { settings, saveSettings, loading, error } = useContext(SettingsContext);

  if (loading) {
    return (
      <div className="settings-page fade-in">
        <div className="settings-loading">Loading settings…</div>
      </div>
    );
  }

  if (error || !settings) {
    return (
      <div className="settings-page fade-in">
        <div className="settings-error">
          Unable to load settings.
          <br />
          {error?.message || "Unknown error"}
        </div>
      </div>
    );
  }

  const handleChange = (key, value) => {
    saveSettings({ ...settings, [key]: value });
  };

  const handleToggle = (key) => {
    saveSettings({ ...settings, [key]: !settings[key] });
  };

  return (
    <div className="settings-page fade-in">
      <h1 className="settings-title">Application Settings</h1>

      <div className="settings-grid">

        {/* THEME MODE */}
        <div className="settings-card">
          <h2 className="settings-card-title">Theme Mode</h2>
          <select
            className="settings-select"
            value={settings.theme}
            onChange={(e) => handleChange("theme", e.target.value)}
          >
            <option value="system">System Default</option>
            <option value="dark">Dark Mode</option>
            <option value="light">Light Mode</option>
          </select>
        </div>

        {/* ACCENT COLOR */}
        <div className="settings-card">
          <h2 className="settings-card-title">Accent Color</h2>
          <input
            type="color"
            className="settings-color-picker"
            value={settings.accentColor || "#00e5ff"}
            onChange={(e) => handleChange("accentColor", e.target.value)}
          />
        </div>

        {/* NOTIFICATIONS */}
        <div className="settings-card">
          <h2 className="settings-card-title">Notifications</h2>

          <label className="settings-toggle-row">
            <input
              type="checkbox"
              checked={settings.notifications_enabled}
              onChange={() => handleToggle("notifications_enabled")}
            />
            <span>Enable Notifications</span>
          </label>

          <label className="settings-toggle-row">
            <input
              type="checkbox"
              checked={settings.enableToasts}
              onChange={() => handleToggle("enableToasts")}
            />
            <span>Enable Toasts</span>
          </label>

          <label className="settings-toggle-row">
            <input
              type="checkbox"
              checked={settings.enableSounds}
              onChange={() => handleToggle("enableSounds")}
            />
            <span>Enable Sounds</span>
          </label>
        </div>

        {/* DATE & TIME */}
        <div className="settings-card">
          <h2 className="settings-card-title">Date & Time</h2>

          <label className="settings-toggle-row">
            <input
              type="checkbox"
              checked={settings.use24h}
              onChange={() => handleToggle("use24h")}
            />
            <span>Use 24‑Hour Time</span>
          </label>

          <label className="settings-toggle-row">
            <input
              type="checkbox"
              checked={settings.showSeconds}
              onChange={() => handleToggle("showSeconds")}
            />
            <span>Show Seconds</span>
          </label>

          <label className="settings-toggle-row">
            <input
              type="checkbox"
              checked={settings.showDate}
              onChange={() => handleToggle("showDate")}
            />
            <span>Show Date</span>
          </label>
        </div>

        {/* SESSION TIMEOUT */}
        <div className="settings-card">
          <h2 className="settings-card-title">Session Timeout</h2>
          <input
            type="number"
            min="5"
            max="120"
            className="settings-number"
            value={settings.sessionTimeout}
            onChange={(e) =>
              handleChange("sessionTimeout", Number(e.target.value))
            }
          />
        </div>

      </div>
    </div>
  );
}
