// /src/components/RouteLoader.jsx

import "./RouteLoader.css";
import logo from "../assets/SentinelOps.jpg";

export default function RouteLoader() {
  return (
    <div className="route-loader-overlay">
      <div className="route-loader-pulse"></div>

      <img src={logo} alt="Loading" className="route-loader-logo" />

      <p className="route-loader-text">Loading…</p>
    </div>
  );
}
