// /src/components/settings/GeneralSettings.jsx
// Hybrid settings component:
// - Simple toggles update context immediately
// - Text fields use local state and commit on blur

import { useEffect, useState } from "react";
import { useSettings } from "../../context/SettingsContext.jsx";

export default function GeneralSettings() {
  const { settings, updateSetting } = useSettings();

  // -----------------------------
  // Local state for text fields
  // -----------------------------
  const [displayName, setDisplayName] = useState("");

  // Sync local state when settings load
  useEffect(() => {
    if (settings) {
      setDisplayName(settings.displayName || "");
    }
  }, [settings]);

  // Commit text field changes on blur
  const commitDisplayName = () => {
    if (displayName !== settings.displayName) {
      updateSetting("displayName", displayName);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: "24px" }}>
      <h2 style={{ marginBottom: "16px" }}>General Settings</h2>

      {/* Display Name */}
      <div style={{ marginBottom: "20px" }}>
        <label
          htmlFor="displayName"
          style={{ display: "block", marginBottom: "6px" }}
        >
          Display Name
        </label>
        <input
          id="displayName"
          type="text"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          onBlur={commitDisplayName}
          className="input"
          style={{
            width: "100%",
            padding: "10px",
            borderRadius: "var(--radius)",
            border: "1px solid var(--border)",
            background: "rgba(255,255,255,0.06)",
            color: "var(--text-primary)",
          }}
        />
      </div>

      {/* Landing Page */}
      <div style={{ marginBottom: "20px" }}>
        <label
          htmlFor="landingPage"
          style={{ display: "block", marginBottom: "6px" }}
        >
          Landing Page
        </label>
        <select
          id="landingPage"
          value={settings.landingPage}
          onChange={(e) => updateSetting("landingPage", e.target.value)}
          className="input"
          style={{
            width: "100%",
            padding: "10px",
            borderRadius: "var(--radius)",
            border: "1px solid var(--border)",
            background: "rgba(255,255,255,0.06)",
            color: "var(--text-primary)",
          }}
        >
          <option value="dashboard">Dashboard</option>
          <option value="alerts">Alerts</option>
          <option value="settings">Settings</option>
        </select>
      </div>

      {/* Sidebar Collapse Toggle */}
      <div style={{ marginBottom: "20px" }}>
        <label style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <input
            type="checkbox"
            checked={settings.sidebarCollapsed}
            onChange={(e) =>
              updateSetting("sidebarCollapsed", e.target.checked)
            }
          />
          Collapse Sidebar
        </label>
      </div>

      {/* Enable Toasts */}
      <div style={{ marginBottom: "20px" }}>
        <label style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <input
            type="checkbox"
            checked={settings.enableToasts}
            onChange={(e) => updateSetting("enableToasts", e.target.checked)}
          />
          Enable Toast Notifications
        </label>
      </div>

      {/* Enable Sounds */}
      <div style={{ marginBottom: "20px" }}>
        <label style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <input
            type="checkbox"
            checked={settings.enableSounds}
            onChange={(e) => updateSetting("enableSounds", e.target.checked)}
          />
          Enable UI Sounds
        </label>
      </div>
    </div>
  );
}
