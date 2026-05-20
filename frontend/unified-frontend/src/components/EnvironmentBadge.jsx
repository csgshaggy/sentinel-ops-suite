// /src/components/EnvironmentBadge.jsx

import React from "react";
import "./EnvironmentBadge.css";

export default function EnvironmentBadge() {
  const env = import.meta.env.VITE_ENV || "DEV";

  const getClass = () => {
    switch (env.toUpperCase()) {
      case "PROD":
        return "env-badge env-prod";
      case "STAGING":
        return "env-badge env-staging";
      default:
        return "env-badge env-dev";
    }
  };

  return (
    <div className={getClass()}>
      {env.toUpperCase()}
    </div>
  );
}
