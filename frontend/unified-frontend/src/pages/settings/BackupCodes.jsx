// File: /src/pages/settings/BackupCodes.jsx

import { useState, useEffect } from "react";     // ✅ FIX: required hooks
import axios from "../../utils/axiosInstance";
import "./BackupCodes.css";

export default function BackupCodes() {
  const [codes, setCodes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [regenerating, setRegenerating] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadCodes = async () => {
    try {
      setLoading(true);
      const res = await axios.get("/api/auth/mfa/backup-codes");
      setCodes(res.data.codes || []);
    } catch {
      setError("Failed to load backup codes.");
    } finally {
      setLoading(false);
    }
  };

  const regenerateCodes = async () => {
    try {
      setRegenerating(true);
      setError("");
      setSuccess("");

      const res = await axios.post("/api/auth/mfa/backup-codes/regenerate");
      setCodes(res.data.codes || []);
      setSuccess("Backup codes regenerated.");
    } catch {
      setError("Failed to regenerate backup codes.");
    } finally {
      setRegenerating(false);
    }
  };

  const downloadCodes = () => {
    const blob = new Blob([codes.join("\n")], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "backup_codes.txt";
    a.click();

    URL.revokeObjectURL(url);
  };

  useEffect(() => {
    loadCodes();
  }, []);

  return (
    <div className="backup-codes-container">
      <h1>Backup Codes</h1>

      <p>
        Backup codes allow you to access your account if you lose access to your
        authenticator device.
      </p>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          <div className="backup-codes-box">
            {codes.length === 0 ? (
              <p>No backup codes available.</p>
            ) : (
              <ul>
                {codes.map((code, idx) => (
                  <li key={idx}>{code}</li>
                ))}
              </ul>
            )}
          </div>

          <div className="backup-codes-actions">
            <button className="backup-button" onClick={downloadCodes}>
              Download Codes
            </button>

            <button
              className="backup-button danger"
              onClick={regenerateCodes}
              disabled={regenerating}
            >
              {regenerating ? "Regenerating..." : "Regenerate Codes"}
            </button>
          </div>

          {error && <p className="backup-error">{error}</p>}
          {success && <p className="backup-success">{success}</p>}
        </>
      )}
    </div>
  );
}
