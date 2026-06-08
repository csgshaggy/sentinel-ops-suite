// /src/pages/Profile/components/tabs/ApiKeysTab.jsx
// SentinelOps — API Keys Tab (Safe + Placeholder Mode)

import { useState } from "react";
import ApiKeyCreateModal from "../ApiKeyCreateModal.jsx";
import "./ApiKeysTab.css";

export default function ApiKeysTab({ loading, apiKeys, onRefresh }) {
  const [createOpen, setCreateOpen] = useState(false);

  // ⭐ SAFETY: ensure apiKeys is always an array
  const safeKeys = Array.isArray(apiKeys) ? apiKeys : [];

  const copy = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (err) {
    Telemetry.ui("click", { action: "copy_api_key" }, "ApiKeysTab");
      console.error("Clipboard copy failed:", err);
    }
  };

  if (loading) {
    return (
      <div className="apikeys-skeleton">
        <div className="skeleton skeleton-line"></div>
        <div className="skeleton skeleton-line"></div>
        <div className="skeleton skeleton-line"></div>
      </div>
    );
  }

  // ⭐ If backend endpoint doesn't exist → show placeholder
  if (!Array.isArray(apiKeys)) {
    return (
      <div className="apikeys-tab-container">
        <div className="apikeys-header">
          <h3>API Keys</h3>

          <div className="apikeys-actions">
            <button className="btn-secondary" onClick={onRefresh}>
              Refresh
            </button>
          </div>
        </div>

        <div className="apikeys-empty glass">
          API Keys API not implemented on backend.
        </div>
      </div>
    );
  }

  return (
    <div className="apikeys-tab-container">
      <div className="apikeys-header">
        <h3>API Keys</h3>

        <div className="apikeys-actions">
          <button className="btn-secondary" onClick={onRefresh}>
            Refresh
          </button>

          <button className="btn-primary" onClick={() => setCreateOpen(true)}>
            Create API Key
          </button>
        </div>
      </div>

      {safeKeys.length === 0 ? (
        <div className="apikeys-empty glass">
          No API keys created yet.
        </div>
      ) : (
        <table className="apikeys-table glass">
          <thead>
            <tr>
              <th>Name</th>
              <th>Created</th>
              <th>Last Used</th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            {safeKeys.map((key) => (
              <tr key={key.id}>
                <td>{key.name}</td>

                <td>
                  {key.created_at
                    ? new Date(key.created_at).toLocaleString()
                    : "—"}
                </td>

                <td>
                  {key.last_used
                    ? new Date(key.last_used).toLocaleString()
                    : "Never"}
                </td>

                <td>
                  <button className="btn-danger btn-small">
                    Revoke
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {createOpen && (
        <ApiKeyCreateModal
          onClose={() => setCreateOpen(false)}
          onCreated={() => {
            setCreateOpen(false);
            onRefresh();
          }}
          onCopy={copy}
        />
      )}
    </div>
  );
}
