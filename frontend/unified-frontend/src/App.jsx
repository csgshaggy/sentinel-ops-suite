// /src/App.jsx

import { useEffect, useState } from "react";
import { useLocation, Outlet } from "react-router-dom";

import RouteLoader from "./components/RouteLoader.jsx";
import SystemLockdown from "./components/SystemLockdown.jsx";

import { ModalProvider } from "./components/ModalManager.jsx";

import { initSessionEventBridge } from "./services/sessionEventBridge.js";
import { isAuthRoute } from "./utils/isAuthRoute.js";

const LOCKDOWN_ENABLED = false;

export default function App() {
  const [loadingRoute, setLoadingRoute] = useState(false);
  const location = useLocation();

  useEffect(() => {
    if (!import.meta.env.PROD) {
      initSessionEventBridge();
    }
  }, []);

  const isPublicRoute = isAuthRoute(location.pathname);

  useEffect(() => {
    Promise.resolve().then(() => setLoadingRoute(true));
    const t = setTimeout(() => setLoadingRoute(false), 350);
    return () => clearTimeout(t);
  }, [location.pathname]);

  if (LOCKDOWN_ENABLED) {
    return <SystemLockdown />;
  }

  return (
    <ModalProvider>
      {!isPublicRoute && loadingRoute && <RouteLoader />}
      <Outlet />   {/* <-- ALWAYS render Outlet */}
    </ModalProvider>
  );
}
