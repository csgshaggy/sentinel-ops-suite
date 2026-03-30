// =====================================================================
// SSRF Command Console — AdminLayout
// Role Guard • Breadcrumbs • Collapsible Sidebar • Page Transitions
// Global Loading Overlay • Theme Integration
// =====================================================================

import { Outlet, Navigate } from "react-router-dom";
import { useContext, useEffect } from "react";

import { AuthContext } from "../../context/AuthContext";
import { useLayout } from "../../context/LayoutContext";

import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

import PageTransition from "../../components/PageTransition";
import GlobalLoadingOverlay from "../../components/GlobalLoadingOverlay";

import "./AdminLayout.css";

export default function AdminLayout() {
  const { authenticated, user, loading, login } = useContext(AuthContext);
  const { setGlobalLoading } = useLayout();

  // Run session check on mount
  useEffect(() => {
    (async () => {
      setGlobalLoading(true);
      await login(); // /auth/me
      setGlobalLoading(false);
    })();
  }, [login, setGlobalLoading]);

  // Still checking session
  if (loading) {
    return (
      <div className="admin-shell">
        <div className="admin-shell-center">Checking session…</div>
      </div>
    );
  }

  // Not authenticated
  if (!authenticated) {
    return <Navigate to="/login" replace />;
  }

  // Role guard — only admin/operator allowed
  if (user && !["admin", "operator"].includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return (
    <div className="admin-shell">
      <Sidebar />

      <div className="admin-shell-main">
        <Topbar />

        <div className="admin-shell-content">
          <PageTransition>
            <Outlet />
          </PageTransition>
        </div>
      </div>

      <GlobalLoadingOverlay />
    </div>
  );
}
