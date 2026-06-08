// /src/pages/Admin/AdminPreferences.jsx
// ============================================================
// SentinelOps — Admin: User Preference Overrides (Unified + Neon‑Glassy)
// - RBAC protected (admin only)
// - Uses unified apiClient.js
// - Uses unified AuthContext
// - Matches AdminPanel.css theme
// ============================================================

import React, { useEffect, useState } from "react";
import { useAuth } from "../../features/auth/AuthContext.jsx";
import { useNavigate } from "react-router-dom";
import client from "../../api/apiClient.js";
import { toast } from "../../components/ToastManager.jsx";
import "../AdminPanel.css"; // unified admin theme

export default function AdminPreferences() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  const [users, setUsers] = useState([]);
  const [saving, setSaving] = useState(null);

  // ------------------------------------------------------------
  // RBAC: Only admins may enter
  // ------------------------------------------------------------
  useEffect(() => {
    if (!loading) {
      if (!user) {
        navigate("/login", { replace: true });
      } else if (user.role !== "admin") {
        navigate("/dashboard", { replace: true });
      }
    }
  }, [user, loading, navigate]);

  // ------------------------------------------------------------
  // Load user preference overrides
  // ------------------------------------------------------------
  async function loadPreferences() {
    const res = await client.get("/api/v1/admin/user-preferences");

    if (!res.ok) {
      toast.error("Failed to load admin preferences.");
      return;
    }

    setUsers(res.data || []);
  }

  useEffect(() => {
    if (user?.role === "admin") {
      loadPreferences();
    }
  }, [user]);

  // ------------------------------------------------------------
  // Save preferences for a user
  // ------------------------------------------------------------
  async function handleSave(userId, prefs) {
    setSaving(userId);

    const res = await client.put(`/api/v1/admin/user-preferences/${userId}`, prefs);

    setSaving(null);

    if (!res.ok) {
      toast.error("Error saving preferences.");
      return;
    }

    toast.success("Preferences updated.");
    loadPreferences();
  }

  // ------------------------------------------------------------
  // Render
  // ------------------------------------------------------------
  if (loading || !user || user.role !== "admin") {
    return <div className="admin-panel">Loading...</div>;
  }

  return (
    <div className="admin-panel">
      <h1 className="admin-title">User Preference Overrides</h1>

      <div className="admin-table-wrapper">
        {users.length === 0 ? (
          <div className="admin-empty">No user preferences found.</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Theme</th>
                <th>Accent</th>
                <th>Timezone</th>
                <th>Language</th>
                <th>Login Alerts</th>
                <th>Security Warnings</th>
                <th>Product Updates</th>
                <th>Session Timeout</th>
                <th>Save</th>
              </tr>
            </thead>

            <tbody>
              {users.map((u) => (
                <tr key={u.user_id}>
                  <td>{u.username}</td>

                  {/* Theme */}
                  <td>
                    <select
                      value={u.theme}
                      onChange={(e) =>
                        setUsers((prev) =>
                          prev.map((x) =>
                            x.user_id === u.user_id
                              ? { ...x, theme: e.target.value }
                              : x
                          )
                        )
                      }
                    >
                      <option value="system">System</option>
                      <option value="light">Light</option>
                      <option value="dark">Dark</option>
                      <option value="neon">Neon</option>
                    </select>
                  </td>

                  {/* Accent */}
                  <td>
                    <input
                      type="color"
                      value={u.accent}
                      onChange={(e) =>
                        setUsers((prev) =>
                          prev.map((x) =>
                            x.user_id === u.user_id
                              ? { ...x, accent: e.target.value }
                              : x
                          )
                        )
                      }
                    />
                  </td>

                  {/* Timezone */}
                  <td>
                    <input
                      type="text"
                      value={u.timezone}
                      onChange={(e) =>
                        setUsers((prev) =>
                          prev.map((x) =>
                            x.user_id === u.user_id
                              ? { ...x, timezone: e.target.value }
                              : x
                          )
                        )
                      }
                    />
                  </td>

                  {/* Language */}
                  <td>
                    <select
                      value={u.language}
                      onChange={(e) =>
                        setUsers((prev) =>
                          prev.map((x) =>
                            x.user_id === u.user_id
                              ? { ...x, language: e.target.value }
                              : x
                          )
                        )
                      }
                    >
                      <option value="en-US">English (US)</option>
                      <option value="en-GB">English (UK)</option>
                      <option value="es-ES">Spanish</option>
                      <option value="fr-FR">French</option>
                    </select>
                  </td>

                  {/* Login Alerts */}
                  <td>
                    <input
                      type="checkbox"
                      checked={u.login_alerts}
                      onChange={(e) =>
                        setUsers((prev) =>
                          prev.map((x) =>
                            x.user_id === u.user_id
                              ? { ...x, login_alerts: e.target.checked }
                              : x
                          )
                        )
                      }
                    />
                  </td>

                  {/* Security Warnings */}
                  <td>
                    <input
                      type="checkbox"
                      checked={u.security_warnings}
                      onChange={(e) =>
                        setUsers((prev) =>
                          prev.map((x) =>
                            x.user_id === u.user_id
                              ? { ...x, security_warnings: e.target.checked }
                              : x
                          )
                        )
                      }
                    />
                  </td>

                  {/* Product Updates */}
                  <td>
                    <input
                      type="checkbox"
                      checked={u.product_updates}
                      onChange={(e) =>
                        setUsers((prev) =>
                          prev.map((x) =>
                            x.user_id === u.user_id
                              ? { ...x, product_updates: e.target.checked }
                              : x
                          )
                        )
                      }
                    />
                  </td>

                  {/* Session Timeout */}
                  <td>
                    <input
                      type="number"
                      min="1"
                      max="120"
                      value={u.session_timeout}
                      onChange={(e) =>
                        setUsers((prev) =>
                          prev.map((x) =>
                            x.user_id === u.user_id
                              ? { ...x, session_timeout: Number(e.target.value) }
                              : x
                          )
                        )
                      }
                    />
                  </td>

                  {/* Save */}
                  <td>
                    <button
                      className="admin-btn"
                      disabled={saving === u.user_id}
                      onClick={() =>
                        handleSave(u.user_id, {
                          theme: u.theme,
                          accent: u.accent,
                          timezone: u.timezone,
                          language: u.language,
                          login_alerts: u.login_alerts,
                          security_warnings: u.security_warnings,
                          product_updates: u.product_updates,
                          session_timeout: u.session_timeout,
                        })
                      }
                    >
                      {saving === u.user_id ? "Saving..." : "Save"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
