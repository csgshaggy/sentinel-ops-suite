import React from "react";
import { Link } from "react-router-dom";

export default function SecurityIndex() {
  return (
    <div style={{ padding: "2rem" }}>
      <h1>Security Settings</h1>

      <ul style={{ marginTop: "1rem" }}>
        <li>
          <Link to="/settings/mfa">Multi‑Factor Authentication</Link>
        </li>
      </ul>
    </div>
  );
}
