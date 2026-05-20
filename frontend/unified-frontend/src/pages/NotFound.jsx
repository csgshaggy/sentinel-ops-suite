// /src/pages/NotFound.jsx

import { useNavigate } from "react-router-dom";
import logo from "../assets/SentinelOps.jpg";

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="error-container">
      <div className="error-pulse"></div>

      <img src={logo} alt="Sentinel Ops" className="error-logo" />

      <h1 className="error-code">404</h1>
      <p className="error-message">
        The page you’re looking for doesn’t exist or may have been moved.
      </p>

      <button className="error-btn" onClick={() => navigate("/login")}>
        Return to Login
      </button>
    </div>
  );
}
