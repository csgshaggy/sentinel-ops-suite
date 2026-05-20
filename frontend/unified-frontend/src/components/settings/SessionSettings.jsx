// /src/components/settings/SessionSettings.jsx
// Hybrid settings component:
// - Simple toggles update context immediately
// - Numeric inputs use local state + commit on blur
// - No API calls, no save button (handled by SettingsFooter)

import { useEffect, useState } from "react";
import { useSettings } from "../../context/SettingsContext.jsx";

export default function SessionSettings() {
  const { settings, updateSetting } = useSettings();

  // Local hybrid state for numeric fields
  const [sessionTimeout, setSessionTimeout] = useState(15);

  // Sync local state when settings load
  useEffect(() => {
    if (settings) {
      setSessionTimeout(settings.sessionTimeout ?? 15);
    }
  }, [settings]);

  // Commit numeric field on blur
  const commitSessionTimeout = () => {
    const value = Number(sessionTimeout);
    if (!Number.isNaN(value) && value !== settings.sessionTimeout) {
      updateSetting("sessionTimeout", value);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: "24px" }}>
      <h2 style={{ marginBottom: "16px" }}>Session & Security</h2>

      {/* Session Timeout */}
      <div style={{ marginBottom: "20px" }}>
        <label
          htmlFor="sessionTimeout"
          style={{ display: "block", marginBottom: "6px" }}
        >
          Session Timeout (minutes)
        </label>
        <input
          id="sessionTimeout"
          type="number"
          min="1"
          max="240"
          value={sessionTimeout}
          onChange={(e) => setSessionTimeout(e.target.value)}
          onBlur={commitSessionTimeout}
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

      {/* Email Alerts */}
      <div style={{ marginBottom: "20px" }}>
        <label style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <input
            type="checkbox"
            checked={settings.emailAlerts}
            onChange={(e) => updateSetting("emailAlerts", e.target.checked)}
          />
          Enable Email Alerts
        </label>
      </div>
    </div>
  );
}
