// /src/layouts/ProtectedLayout.jsx

import React from "react";
import { Outlet } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";

export default function ProtectedLayout() {
  const { user } = useAuth();

  // Just pass user to Layout via context
  return <Outlet context={{ user }} />;
}
