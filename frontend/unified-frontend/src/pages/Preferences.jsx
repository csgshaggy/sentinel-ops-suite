import React, { useEffect, useState } from "react";
import { Telemetry } from "@/features/telemetry/telemetry";
import { getUserPreferences, updateUserPreferences } from "../../api/preferences";

const Preferences = () => {
  const [formState, setFormState] = useState({
    theme: "light",
    accent_color: "#00f7ff",
    layout_density: "comfortable",
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    getUserPreferences()
      .then((prefs) => {
        setFormState(prefs);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const handleSave = async () => {
    Telemetry.ui("submit", { form: "preferences" }, "Preferences");
    setSaving(true);

    try {
      await updateUserPreferences(formState);
      setMessage("Preferences saved!");
      setTimeout(() => setMessage(""), 2000);
    } catch (err) {
      console.error(err);
      setMessage("Error saving preferences.");
    }

    setSaving(false);
  };

  if (loading) return <div>Loading preferences...</div>;

  return (
    <div className="preferences-container">
      <h2>User Preferences</h2>

      {message && <div className="status-message">{message}</div>}

      <label>
        Theme:
        <select
          value={formState.theme}
          onChange={(e) =>
            setFormState({ ...formState, theme: e.target.value })
          }
        >
          <option value="light">Light</option>
          <option value="dark">Dark</option>
          <option value="neon">Neon</option>
        </select>
      </label>

      <label>
        Accent Color:
        <input
          type="color"
          value={formState.accent_color}
          onChange={(e) =>
            setFormState({ ...formState, accent_color: e.target.value })
          }
        />
      </label>

      <label>
        Layout Density:
        <select
          value={formState.layout_density}
          onChange={(e) =>
            setFormState({ ...formState, layout_density: e.target.value })
          }
        >
          <option value="comfortable">Comfortable</option>
          <option value="compact">Compact</option>
        </select>
      </label>

      <button onClick={handleSave} disabled={saving}>
        {saving ? "Saving..." : "Save Preferences"}
      </button>
    </div>
  );
};

export default Preferences;
