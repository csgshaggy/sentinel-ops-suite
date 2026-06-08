// /src/components/settings/TimeSettings.jsx
// Hybrid settings component:
// - Simple toggles update context immediately
// - Numeric inputs use local state + commit on blur
// - No API calls, no save button (handled by SettingsFooter)

import { useEffect, useState } from "react";
import { useSettings } from "../../context/SettingsContext.jsx";

export default function TimeSettings() {
  const { settings, updateSetting } = useSettings();

  // Local hybrid state for numeric fields
  const [autoRefresh, setAutoRefresh] = useState(30);

  // Sync local state when settings load
  useEffect(() => {
    if (settings) {
      setAutoRefresh(settings.autoRefresh ?? 30);
    }
  }, [settings]);

  // Commit numeric field on blur
  const commitAutoRefresh = () => {
    const value = Number(autoRefresh);
    if (!Number.isNaN(value) && value !== settings.autoRefresh) {
      updateSetting("autoRefresh", value);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: "24px" }}>
      <h2 style={{ marginBottom: "16px" }}>Time & Display Settings</h2>

      {/* 24-Hour Time */}
      <div style={{ marginBottom: "20px" }}>
        <label style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <input
            type="checkbox"
            checked={settings.use24h}
            onChange={(e) => updateSetting("use24h", e.target.checked)}
          />
          Use 24‑Hour Time
        </label>
      </div>

      {/* Show Seconds */}
      <div style={{ marginBottom: "20px" }}>
        <label style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <input
            type="checkbox"
            checked={settings.showSeconds}
            onChange={(e) => updateSetting("showSeconds", e.target.checked)}
          />
          Show Seconds
        </label>
      </div>

      {/* Show Date */}
      <div style={{ marginBottom: "20px" }}>
        <label style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <input
            type="checkbox"
            checked={settings.showDate}
            onChange={(e) => updateSetting("showDate", e.target.checked)}
          />
          Show Date
        </label>
      </div>

      {/* Auto Refresh Interval */}
      <div style={{ marginBottom: "20px" }}>
        <label
          htmlFor="autoRefresh"
          style={{ display: "block", marginBottom: "6px" }}
        >
          Auto‑Refresh Interval (seconds)
        </label>
        <input
          id="autoRefresh"
          type="number"
          min="5"
          max="3600"
          value={autoRefresh}
          onChange={(e) => setAutoRefresh(e.target.value)}
          onBlur={commitAutoRefresh}
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
    </div>
  );
}
