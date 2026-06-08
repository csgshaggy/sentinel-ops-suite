// /src/pages/Profile/components/ApiKeyCreateModal.jsx
// SentinelOps — API Key Creation Modal (Secret‑Once Reveal)

import { useState } from "react";
import "./ApiKeyCreateModal.css";

export default function ApiKeyCreateModal({ onClose, onCreated, onCopy }) {
  const [name, setName] = useState("");
  const [createdKey, setCreatedKey] = useState(null);

  const handleCreate = async () => {
    // NOTE: Real API call will be wired in Phase 3
    const fakeKey = {
      id: crypto.randomUUID(),
      secret: "sk-" + crypto.randomUUID().replace(/-/g, "").slice(0, 24),
    };

    setCreatedKey(fakeKey);
  };

  const handleDone = () => {
    onCreated();
  };

  return (
    <div className="apikey-modal-overlay">
      <div className="apikey-modal glass">
        {!createdKey ? (
          <>
            <h2>Create API Key</h2>

            <div className="form-group">
              <label className="form-label">Key Name</label>
              <input
                className="form-input"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="apikey-modal-actions">
              <button className="btn-secondary" onClick={onClose}>
                Cancel
              </button>

              <button
                className="btn-primary"
                disabled={!name.trim()}
                onClick={handleCreate}
              >
                Create Key
              </button>
            </div>
          </>
        ) : (
          <>
            <h2>API Key Created</h2>

            <p className="apikey-warning">
              This is the only time you will see this secret.
              Copy it now and store it securely.
            </p>

            <div className="apikey-secret-box glass">
              {createdKey.secret}
            </div>

            <button
              className="btn-secondary"
              onClick={() => onCopy(createdKey.secret)}
            >
              Copy to Clipboard
            </button>

            <div className="apikey-modal-actions">
              <button className="btn-primary" onClick={handleDone}>
                Done
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
