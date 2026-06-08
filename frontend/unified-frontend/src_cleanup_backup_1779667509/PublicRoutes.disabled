// /src/routes/PublicRoutes.jsx

import { Routes, Route, Navigate } from "react-router-dom";
import Login from "../pages/Login.jsx";

export default function PublicRoutes() {
  return (
    <Routes>
      {/* Explicit /login route */}
      <Route path="login" element={<Login />} />

      {/* Also allow index → /login */}
      <Route index element={<Login />} />

      {/* Fallback → redirect to /login */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}
