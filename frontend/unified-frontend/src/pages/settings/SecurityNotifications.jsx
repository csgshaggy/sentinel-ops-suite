// File: /src/pages/settings/SecurityNotifications.jsx

import axios from "../../utils/axiosInstance";
import "./SecurityNotifications.css";

export default function SecurityNotifications() {
  const [settings, setSettings] = useState({
    login_alerts: false,
    password_change: true,
    mfa_changes: true,
    new_device: true,
    recovery_updates: true,
    session_terminated: true,
  });

  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadSettings = async () => {
    try {
      setLoading(true);
      const res = await axios.get("/api/auth/security-notifications");
      setSettings(res.data || settings);
    } catch (err) {
      setError("Failed to load security notification settings.");
    } finally {
      setLoading(false);
    }
  };

  const saveSettings = async () => {
    try {
      setSaving(true);
      setError("");
      setSuccess("");

      await axios.post("/api/auth/security-notifications", settings);

      setSuccess("Security notification settings updated.");
    } catch (err) {
      setError("Failed to update settings.");
    } finally {
      setSaving(false);
    }
  };

  const toggle = (key) => {
    setSettings((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  useEffect(() => {
    loadSettings();
  }, []);

  return (
    <div className="security-notifications-container">
      <h1>Security Notifications</h1>

      <p>
        Choose which security‑related events you want to be notified about. These
        alerts help you stay aware of changes to your account.
      </p>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="security-notifications-list">
          {Object.entries(settings).map(([key, value]) => (
            <label key={key} className="security-notification-item">
              <input
                type="checkbox"
                checked={value}
                onChange={() => toggle(key)}
              />
              {key
                .replace(/_/g, " ")
                .replace(/\b\w/g, (c) => c.toUpperCase())}
            </label>
          ))}
        </div>
      )}

      <button
        className="security-notifications-button"
        onClick={saveSettings}
        disabled={saving}
      >
        {saving ? "Saving..." : "Save Settings"}
      </button>

      {error && <p className="security-notifications-error">{error}</p>}
      {success && <p className="security-notifications-success">{success}</p>}
    </div>
  );
}
