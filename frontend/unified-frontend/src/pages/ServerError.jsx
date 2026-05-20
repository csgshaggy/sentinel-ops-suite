// /src/pages/ServerError.jsx

import { useNavigate } from "react-router-dom";
import logo from "../assets/SentinelOps.jpg";

export default function ServerError() {
  const navigate = useNavigate();

  return (
    <div className="error-container">
      <div className="error-pulse error-pulse-red"></div>

      <img src={logo} alt="Sentinel Ops" className="error-logo" />

      <h1 className="error-code error-code-red">500</h1>
      <p className="error-message">
        An unexpected server error occurred. Our systems are working to restore service.
      </p>

      <button className="error-btn" onClick={() => navigate("/")}>
        Return to Dashboard
      </button>
    </div>
  );
}
