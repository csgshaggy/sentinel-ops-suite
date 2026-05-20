// /src/components/SystemLockdown.jsx

import "./SystemLockdown.css";
import logo from "../assets/SentinelOps.jpg";

export default function SystemLockdown() {
  return (
    <div className="lockdown-container">
      <div className="lockdown-pulse"></div>

      <img src={logo} alt="Sentinel Ops" className="lockdown-logo" />

      <h1 className="lockdown-title">SYSTEM LOCKDOWN ACTIVE</h1>
      <p className="lockdown-subtitle">
        Access to the Sentinel Ops Suite has been temporarily restricted.
      </p>

      <p className="lockdown-footer">
        Please stand by while system integrity checks are performed.
      </p>
    </div>
  );
}
