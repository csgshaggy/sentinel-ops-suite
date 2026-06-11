// src/pages/Dashboard.jsx
import { useEffect, useState } from "react";
import { useUser } from "../context/UserContext";

import "../styles/panels.css";
import "../styles/layout.css";
import "../styles/icons.css";
import "../styles/buttons.css";
import "../styles/animations.css";

export default function Dashboard() {
  const { user, loading } = useUser();
  const [stats, setStats] = useState({
    alerts: 0,
    systemsOnline: 0,
    usersOnline: 0,
    failedLogins: 0,
  });

  const [refreshing, setRefreshing] = useState(false);

  if (loading) return null;
  if (!user) return null;

  async function loadStats() {
    try {
      setRefreshing(true);

      // 🔥 FIXED API PATH
      const res = await fetch("/dashboard/summary", {
        credentials: "include",
      });

      if (res.ok) {
        const data = await res.json();

        // Map backend → frontend fields
        setStats({
          alerts: data.tiles?.find(t => t.title === "Alerts")?.value ?? 0,
          systemsOnline: data.tiles?.find(t => t.title === "System Health")?.value === "OK" ? 1 : 0,
          usersOnline: data.tiles?.find(t => t.title === "Active Sessions")?.value ?? 0,
          failedLogins: 0, // placeholder
        });
      } else {
        console.error("Dashboard stats request failed:", res.status);
      }
    } catch (err) {
      console.error("Failed to load dashboard stats:", err);
    } finally {
      setRefreshing(false);
    }
  }

  useEffect(() => {
    loadStats();
  }, []);

  return (
    <div className="page-container fade-in">
      <div className="page-header">
        <h1 className="page-title">Dashboard Overview</h1>

        <div className="page-actions">
          <button
            className="btn-secondary"
            onClick={loadStats}
            disabled={refreshing}
          >
            {refreshing ? "Refreshing..." : "Refresh"}
          </button>

          <button className="btn-primary">
            {user?.username ?? "Profile"}
          </button>
        </div>
      </div>

      <div className="panel-grid">
        <div className="panel glass-panel">
          <div className="panel-icon warning-icon"></div>
          <div className="panel-content">
            <h2>{stats.alerts}</h2>
            <p>Active Alerts</p>
          </div>
        </div>

        <div className="panel glass-panel">
          <div className="panel-icon success-icon"></div>
          <div className="panel-content">
            <h2>{stats.systemsOnline}</h2>
            <p>Online Systems</p>
          </div>
        </div>

        <div className="panel glass-panel">
          <div className="panel-icon user-icon"></div>
          <div className="panel-content">
            <h2>{stats.usersOnline}</h2>
            <p>Users Online</p>
          </div>
        </div>

        <div className="panel glass-panel">
          <div className="panel-icon lock-icon"></div>
          <div className="panel-content">
            <h2>{stats.failedLogins}</h2>
            <p>Failed Logins (24h)</p>
          </div>
        </div>
      </div>
    </div>
  );
}
