// /src/components/RoleBadge.jsx

import React from "react";
import "./RoleBadge.css";

export default function RoleBadge({ role }) {
  if (!role) return null;

  const normalized = role.toLowerCase();

  const getClass = () => {
    switch (normalized) {
      case "admin":
        return "role-badge role-admin";
      case "analyst":
        return "role-badge role-analyst";
      case "operator":
        return "role-badge role-operator";
      default:
        return "role-badge role-default";
    }
  };

  return <span className={getClass()}>{normalized.toUpperCase()}</span>;
}
