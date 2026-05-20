import "./index.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/layout/Layout.jsx";
import ProtectedRoute from "./components/auth/ProtectedRoute.jsx";

import { useSession } from "./services/useSession.js";
import { useInactivityTimer } from "./services/useInactivityTimer.js";

import {
  SessionExpireProvider,
  useSessionExpire
} from "./components/modals/SessionExpireManager.jsx";

// Pages
import DashboardHome from "./pages/DashboardHome.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import NotFound from "./pages/NotFound.jsx";

// ✅ Unified frontend (router‑agnostic)
import UnifiedFrontend from "../unified-frontend/src/App.jsx";

function AppInner() {
  const { loading, isAuthenticated } = useSession();
  const { showModal } = useSessionExpire();

  // 15‑minute inactivity timeout
  useInactivityTimer(900000, () => {
    showModal();
  });

  return (
    // ✅ Single router, owned by dashboard-app
    <BrowserRouter basename="/admin">
      <Routes>

        {/* ✅ Protected dashboard root → /admin */}
        <Route
          path="/"
          element={
            <ProtectedRoute
              loading={loading}
              isAuthenticated={isAuthenticated}
            >
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<DashboardHome />} />

          {/* ✅ UnifiedFrontend mounted safely under /admin/sentinel */}
          <Route path="sentinel/*" element={<UnifiedFrontend />} />

          <Route path="*" element={<DashboardHome />} />
        </Route>

        {/* ✅ Login → /admin/login */}
        <Route path="/login" element={<LoginPage />} />

        {/* ✅ Fallback */}
        <Route path="*" element={<NotFound />} />

      </Routes>
    </BrowserRouter>
  );
}

export default function App() {
  return (
    <SessionExpireProvider>
      <AppInner />
    </SessionExpireProvider>
  );
}
