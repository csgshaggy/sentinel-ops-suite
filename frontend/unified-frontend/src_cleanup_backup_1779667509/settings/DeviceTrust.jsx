// File: /src/pages/settings/DeviceTrust.jsx

import { useState, useEffect, useCallback } from "react";
import axios from "../../utils/axiosInstance";
import "./DeviceTrust.css";

export default function DeviceTrust() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [trusting, setTrusting] = useState(false);
  const [removing, setRemoving] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadDevices = useCallback(async () => {
    try {
      setLoading(true);
      const res = await axios.get("/api/auth/devices");
      setDevices(res.data.devices || []);
    } catch {
      setError("Failed to load trusted devices.");
    } finally {
      setLoading(false);
    }
  }, []);

  const trustCurrentDevice = useCallback(async () => {
    try {
      setTrusting(true);
      setError("");
      setSuccess("");

      const res = await axios.post("/api/auth/devices/trust");

      if (res.data.success) {
        setSuccess("This device is now trusted.");
        Promise.resolve().then(loadDevices);
      } else {
        setError("Failed to trust this device.");
      }
    } catch {
      setError("Failed to trust this device.");
    } finally {
      setTrusting(false);
    }
  }, [loadDevices]);

  const removeDevice = useCallback(
    async (deviceId) => {
      try {
        setRemoving(deviceId);
        setError("");
        setSuccess("");

        const res = await axios.post("/api/auth/devices/remove", {
          device_id: deviceId,
        });

        if (res.data.success) {
          setSuccess("Device removed.");
          Promise.resolve().then(loadDevices);
        } else {
          setError("Failed to remove device.");
        }
      } catch {
        setError("Failed to remove device.");
      } finally {
        setRemoving(null);
      }
    },
    [loadDevices]
  );

  useEffect(() => {
    Promise.resolve().then(loadDevices);
  }, [loadDevices]);

  return (
    <div className="device-trust-container">
      <h1>Trusted Devices</h1>

      <p>
        Trusted devices allow you to skip MFA challenges on devices you use
        frequently.
      </p>

      <button
        className="trust-button"
        onClick={trustCurrentDevice}
        disabled={trusting}
      >
        {trusting ? "Trusting..." : "Trust This Device"}
      </button>

      {loading ? (
        <p>Loading devices...</p>
      ) : (
        <div className="device-list">
          {devices.length === 0 ? (
            <p>No trusted devices.</p>
          ) : (
            devices.map((device) => (
              <div key={device.id} className="device-item">
                <div>
                  <strong>{device.name || "Unknown Device"}</strong>
                  <br />
                  Last Used: {device.last_used}
                  <br />
                  IP: {device.ip}
                </div>

                <button
                  className="remove-button danger"
                  onClick={() => removeDevice(device.id)}
                  disabled={removing === device.id}
                >
                  {removing === device.id ? "Removing..." : "Remove"}
                </button>
              </div>
            ))
          )}
        </div>
      )}

      {error && <p className="device-error">{error}</p>}
      {success && <p className="device-success">{success}</p>}
    </div>
  );
}
