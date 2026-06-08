// /src/features/auth/AuthContext.jsx
// SentinelOps — Unified Auth Context (Corrected for /api namespace)

import {
  createContext,
  useState,
  useEffect,
  useCallback,
  useContext,
} from "react";

import { useLocation } from "react-router-dom";
import client, { setUnauthorizedHandler } from "../../api/apiClient.js";
import { toast } from "../../components/ToastManager.jsx";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [mfaUserId, setMfaUserId] = useState(null);

  const location = useLocation();
  const isLoginPage = location.pathname === "/login";

  // ------------------------------------------------------------
  // refreshUser — correct session restore via /api/users/me
  // ------------------------------------------------------------
  const refreshUser = useCallback(async () => {
    try {
      const res = await client.get("/api/users/me", {
        withCredentials: true,
      });

      if (res.status === 200 && res.data) {
        setUser(res.data);
        return res.data;
      }

      setUser(null);
      return null;
    } catch {
      setUser(null);
      return null;
    }
  }, []);

  // ------------------------------------------------------------
  // logout — destroys session + resets state
  // ------------------------------------------------------------
  const logout = useCallback(async () => {
    try {
      await client.post("/api/auth/logout", {}, { withCredentials: true });
    } catch {}

    setUser(null);
    setMfaUserId(null);
    toast.info("You have been logged out.");
    window.location.href = "/login";
  }, []);

  // ------------------------------------------------------------
  // login — unified backend login flow
  // ------------------------------------------------------------
  const login = useCallback(
    async (username, password) => {
      try {
        const res = await client.post(
          "/api/auth/login",
          { username, password },
          { withCredentials: true }
        );

        if (res.data?.mfa_required === true) {
          setMfaUserId(res.data.user_id);
          return { status: "mfa_required", user_id: res.data.user_id };
        }

        await refreshUser();
        toast.success("Logged in successfully.");
        return { status: "success" };
      } catch {
        toast.error("Invalid username or password.");
        return { status: "error" };
      }
    },
    [refreshUser]
  );

  // ------------------------------------------------------------
  // completeMfa — correct endpoint: /api/auth/login/mfa-complete
  // ------------------------------------------------------------
  const completeMfa = useCallback(
    async () => {
      if (!mfaUserId) return "error";

      try {
        await client.post(
          "/api/auth/login/mfa-complete",
          { user_id: mfaUserId },
          { withCredentials: true }
        );

        setMfaUserId(null);
        await refreshUser();
        toast.success("MFA verified. Welcome!");
        return "success";
      } catch {
        toast.error("Invalid MFA code.");
        return "error";
      }
    },
    [mfaUserId, refreshUser]
  );

  // ------------------------------------------------------------
  // 401 interceptor — ONLY logout if user was authenticated
  // ------------------------------------------------------------
  useEffect(() => {
    setUnauthorizedHandler(() => {
      if (user) logout();
    });
  }, [logout, user]);

  // ------------------------------------------------------------
  // Initial load — restore session (but NOT on login page)
  // ------------------------------------------------------------
  useEffect(() => {
    if (isLoginPage) {
      setLoading(false);
      return;
    }

    (async () => {
      await refreshUser();
      setLoading(false);
    })();
  }, [refreshUser, isLoginPage]);

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        completeMfa,
        logout,
        refreshUser,
        mfaUserId,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
