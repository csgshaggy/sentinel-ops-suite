// /src/pages/Profile/components/tabs/LoginHistoryTab.jsx

import { useEffect, useState } from "react";
import apiClient from "../../../../api/apiClient";
import { toast } from "../../../../components/ToastManager.jsx";

import "./LoginHistoryTab.css";

export default function LoginHistoryTab({ profile }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const res = await apiClient.get("/users/me/login-history");
        setHistory(res.data || []);
      } catch (err) {
    Telemetry.ui("load", { action: "login_history" }, "LoginHistoryTab");
        toast.error("Failed to load login history.");
      } finally {
        setLoading(false);
      }
    };

    loadHistory();
  }, []);

  if (loading) {
    return (
      <div className="loginhistory-tab-container">
        <div className="loginhistory-empty">Loading login history...</div>
      </div>
    );
  }

  if (!history.length) {
    return (
      <div className="loginhistory-tab-container">
        <div className="loginhistory-empty">No login history available.</div>
      </div>
    );
  }

  return (
    <div className="loginhistory-tab-container">
      <h2 className="tab-title">Login History</h2>

      <div className="loginhistory-table-wrapper">
        <table className="loginhistory-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>IP Address</th>
              <th>User Agent</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {history.map((entry, idx) => (
              <tr key={idx}>
                <td>{entry.timestamp}</td>
                <td>{entry.ip_address}</td>
                <td>{entry.user_agent}</td>
                <td>{entry.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

