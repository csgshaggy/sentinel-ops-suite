// dashboard-app/src/components/settings/SettingsModal.jsx

import { useEffect, useState } from "react";
import { useSettings } from "../../context/SettingsContext";

const SettingsModal = ({ isOpen, onClose }) => {
  const { settings, saveSettings } = useSettings();

  const [form, setForm] = useState({});

  // Load settings into local form state when modal opens
  useEffect(() => {
    if (settings && isOpen) {
      setForm(settings);
    }
  }, [settings, isOpen]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, type, value, checked } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSave = async () => {
    await saveSettings(form);
    onClose();
  };

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <h2>User Settings</h2>

        {!settings ? (
          <p>Loading...</p>
        ) : (
          <>
            {/* Display Name */}
            <label>
              Display Name
              <input
                type="text"
                name="display_name"
                value={form.display_name || ""}
                onChange={handleChange}
              />
            </label>

            {/* Landing Page */}
            <label>
              Landing Page
              <select
                name="landing_page"
                value={form.landing_page || "dashboard"}
                onChange={handleChange}
              >
                <option value="dashboard">Dashboard</option>
                <option value="analytics">Analytics</option>
                <option value="settings">Settings</option>
              </select>
            </label>

            {/* Toggles */}
            <label>
              <input
                type="checkbox"
                name="show_profile"
                checked={form.show_profile || false}
                onChange={handleChange}
              />
              Show Profile
            </label>

            <label>
              <input
                type="checkbox"
                name="show_clock"
                checked={form.show_clock || false}
                onChange={handleChange}
              />
              Show Clock
            </label>

            <label>
              <input
                type="checkbox"
                name="use_24h"
                checked={form.use_24h || false}
                onChange={handleChange}
              />
              Use 24h Time
            </label>

            <label>
              <input
                type="checkbox"
                name="show_seconds"
                checked={form.show_seconds || false}
                onChange={handleChange}
              />
              Show Seconds
            </label>

            <label>
              <input
                type="checkbox"
                name="show_day"
                checked={form.show_day || false}
                onChange={handleChange}
              />
              Show Day
            </label>

            {/* Sidebar */}
            <label>
              <input
                type="checkbox"
                name="sidebar_collapsed"
                checked={form.sidebar_collapsed || false}
                onChange={handleChange}
              />
              Sidebar Collapsed
            </label>

            {/* Sounds */}
            <label>
              <input
                type="checkbox"
                name="enable_sounds"
                checked={form.enable_sounds || false}
                onChange={handleChange}
              />
              Enable Sounds
            </label>

            <label>
              <input
                type="checkbox"
                name="enable_toasts"
                checked={form.enable_toasts || false}
                onChange={handleChange}
              />
              Enable Toasts
            </label>

            {/* Auto Refresh */}
            <label>
              Auto Refresh (seconds)
              <input
                type="number"
                name="auto_refresh"
                value={form.auto_refresh || 0}
                onChange={handleChange}
              />
            </label>

            {/* Timezone */}
            <label>
              Timezone
              <input
                type="text"
                name="timezone"
                value={form.timezone || "UTC"}
                onChange={handleChange}
              />
            </label>

            {/* Locale */}
            <label>
              Locale
              <input
                type="text"
                name="locale"
                value={form.locale || "en-US"}
                onChange={handleChange}
              />
            </label>

            {/* Time Format */}
            <label>
              Time Format
              <input
                type="text"
                name="time_format"
                value={form.time_format || "24h"}
                onChange={handleChange}
              />
            </label>

            {/* Session Timeout */}
            <label>
              Session Timeout (seconds)
              <input
                type="number"
                name="session_timeout"
                value={form.session_timeout || 900}
                onChange={handleChange}
              />
            </label>

            {/* Auto Logout */}
            <label>
              <input
                type="checkbox"
                name="auto_logout"
                checked={form.auto_logout || false}
                onChange={handleChange}
              />
              Auto Logout
            </label>

            {/* Reauth Sensitive */}
            <label>
              <input
                type="checkbox"
                name="reauth_sensitive"
                checked={form.reauth_sensitive || false}
                onChange={handleChange}
              />
              Reauth on Sensitive Actions
            </label>

            <div className="modal-actions">
              <button onClick={onClose}>Cancel</button>
              <button onClick={handleSave} className="primary">
                Save
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default SettingsModal;
