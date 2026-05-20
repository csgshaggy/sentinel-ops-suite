// frontend/dashboard-app/src/services/AuthContext.jsx

import React, { createContext, useContext, useState, useEffect } from "react";
import { apiFetch } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [authChecked, setAuthChecked] = useState(false);
  const [authOk, setAuthOk] = useState(false);

  // User + roles (required by Sidebar, TopBar, etc.)
  const [user, setUser] = useState(null);
  const [roles, setRoles] = useState([]);

  // ----------------------------------------------------
  // Initial session validation
  // ----------------------------------------------------
  useEffect(() => {
    const verify = async () => {
      try {
        const res = await apiFetch("/api/dashboard/summary");

        if (!res || !res.ok) throw new Error("Not authenticated");

        const data = await res.json();

        setUser(data.user || null);
        setRoles(data.roles || []);

        setAuthOk(true);
      } catch (err) {
        window.location.href = "/login/";
      } finally {
        setAuthChecked(true);
      }
    };

    verify();
  }, []);

  // ----------------------------------------------------
  // Logout function
  // ----------------------------------------------------
  const logout = async () => {
    try {
      await apiFetch("/auth/logout", { method: "POST" });
    } catch (err) {
      // ignore
    } finally {
      window.location.href = "/login/";
    }
  };

  // ----------------------------------------------------
  // RBAC helpers (required by Sidebar)
  // ----------------------------------------------------
  const hasRole = (role) => roles.includes(role);
  const hasAnyRole = (list) => list.some((r) => roles.includes(r));

  // ----------------------------------------------------
  // HEARTBEAT
  // ----------------------------------------------------
  useEffect(() => {
    let lastHeartbeat = 0;

    const sendHeartbeat = async () => {
      const now = Date.now();
      if (now - lastHeartbeat < 60_000) return;
      lastHeartbeat = now;

      try {
        await apiFetch("/api/auth/heartbeat");
      } catch (err) {}
    };

    const events = ["click", "mousemove", "keydown", "scroll", "touchstart"];
    const handler = () => sendHeartbeat();

    events.forEach((evt) => window.addEventListener(evt, handler));
    return () => events.forEach((evt) => window.removeEventListener(evt, handler));
  }, []);

  return (
    <AuthContext.Provider
      value={{
        authChecked,
        authOk,
        user,
        roles,
        hasRole,
        hasAnyRole,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
