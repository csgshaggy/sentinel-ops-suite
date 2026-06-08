// src/components/SettingsFooter.jsx

import { useSettings } from "../context/SettingsContext";

export default function SettingsFooter() {
  const { settings, saveSettings } = useSettings();
  const [saving, setSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState(null);

  const DEFAULTS = {
    displayName: "",
    landingPage: "dashboard",
    sidebarCollapsed: false,
    use24h: false,
    showSeconds: false,
    showDate: true,
    enableSounds: false,
    enableToasts: true,
    autoRefresh: 30,
    emailAlerts: false,
    darkMode: false,
    sessionTimeout: 15,
  };

  // -----------------------------
  // APPLY (save to backend)
  // -----------------------------
  const handleApply = async () => {
    try {
      setSaving(true);
      await saveSettings(settings);
      setLastSaved(new Date());
    } catch (err) {
      console.error("Failed to apply settings:", err);
    } finally {
      setSaving(false);
    }
  };

  // -----------------------------
  // RESET (restore defaults)
  // -----------------------------
  const handleReset = async () => {
    try {
      setSaving(true);
      await saveSettings(DEFAULTS);
      setLastSaved(new Date());
    } catch (err) {
      console.error("Failed to reset settings:", err);
    } finally {
      setSaving(false);
    }
  };

  // -----------------------------
  // SAVE (apply + toast)
  // -----------------------------
  const handleSave = async () => {
    await handleApply();
    // If you have a toast system:
    if (window?.toast) {
      window.toast.success("Settings saved");
    }
  };

  return (
    <div
      className="glass-panel"
      style={{
        padding: "16px 24px",
        marginTop: "32px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        borderTop: "1px solid rgba(255,255,255,0.12)",
      }}
    >
      <div style={{ opacity: 0.7, fontSize: "0.85rem" }}>
        {lastSaved
          ? `Last saved: ${lastSaved.toLocaleTimeString()}`
          : "Unsaved changes"}
      </div>

      <div style={{ display: "flex", gap: "12px" }}>
        <button
          className="btn-secondary"
          disabled={saving}
          onClick={handleReset}
        >
          Reset
        </button>

        <button
          className="btn-secondary"
          disabled={saving}
          onClick={handleApply}
        >
          Apply
        </button>

        <button
          className="btn-primary"
          disabled={saving}
          onClick={handleSave}
        >
          {saving ? "Saving..." : "Save"}
        </button>
      </div>
    </div>
  );
}
