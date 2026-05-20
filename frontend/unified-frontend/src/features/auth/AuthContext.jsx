// /src/features/auth/AuthContext.jsx

import {
  createContext,
  useState,
  useEffect,
  useCallback,
  useContext,
  useRef,
} from "react";

import { toast } from "../../components/ToastManager.jsx";

import {
  login as apiLogin,
  verifyTotp as apiVerifyTotp,
  restoreSession as apiRestoreSession,
  logout as apiLogout,
} from "../../api/auth.js";

import { logSessionEvent } from "../../utils/sessionLogger.js";
import { recordRestore } from "../../utils/sessionMetrics.js";

export const AuthContext = createContext(null);

/* ------------------------------------------------------------
   USER ENRICHMENT — ensures initials + logout handler exist
------------------------------------------------------------- */
function enrichUser(rawUser, logoutFn) {
  if (!rawUser) return null;

  const initials =
    rawUser.initials ||
    rawUser.name?.[0] ||
    rawUser.username?.[0] ||
    rawUser.email?.[0] ||
    "U";

  return {
    ...rawUser,
    initials,
    onLogout: logoutFn,
  };
}

/* ------------------------------------------------------------
   AuthProvider
------------------------------------------------------------- */
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [mfaPending, setMfaPending] = useState(false);
  const [pendingLoginToken, setPendingLoginToken] = useState(null);

  // Prevent overlapping + repeated restore calls
  const restoreLock = useRef(false);
  const hasRestoredOnce = useRef(false);   // <-- NEW: permanent one‑shot gate

  /* ------------------------------------------------------------
     logout() — idempotent
  ------------------------------------------------------------- */
  const logout = useCallback(async () => {
    logSessionEvent("logout_attempt", {
      user: user?.username || null,
    });

    try {
      await apiLogout();
    } catch {
      logSessionEvent("logout_api_error");
    }

    setUser(null);
    setMfaPending(false);
    setPendingLoginToken(null);

    logSessionEvent("logout_success");
    toast.info("You have been logged out.");
  }, [user]);

  /* ------------------------------------------------------------
     restoreSession() — loop‑safe + ONE‑SHOT
  ------------------------------------------------------------- */
  const restoreSession = useCallback(async () => {
    // 🚫 If we've already restored once this page load → NEVER restore again
    if (hasRestoredOnce.current) return;

    // 🚫 Prevent overlapping calls
    if (restoreLock.current) return;
    restoreLock.current = true;

    logSessionEvent("session_restore_attempt");

    try {
      const data = await apiRestoreSession();

      if (data?.user) {
        const enriched = enrichUser(data.user, logout);
        setUser(enriched);

        recordRestore();
        logSessionEvent("session_restore_success", {
          user: data.user.username,
        });

        // 🔒 Permanently block all future restore attempts
        hasRestoredOnce.current = true;
      } else {
        setUser(null);
        logSessionEvent("session_restore_no_user");
      }
    } catch {
      setUser(null);
      logSessionEvent("session_restore_error");
    } finally {
      restoreLock.current = false;
      setLoading(false);
    }
  }, [logout]);

  /* ------------------------------------------------------------
     Initial session restore (ONE TIME ONLY)
  ------------------------------------------------------------- */
  useEffect(() => {
    restoreSession();
  }, [restoreSession]);

  /* ------------------------------------------------------------
     login(username, password)
  ------------------------------------------------------------- */
  const login = useCallback(
    async (username, password) => {
      logSessionEvent("login_attempt", { username });

      try {
        const res = await apiLogin(username, password);

        if (res?.mfa_required) {
          setMfaPending(true);
          setPendingLoginToken(res.pending_login_token);

          logSessionEvent("mfa_challenge", { username });
          return "mfa_required";
        }

        if (res?.user) {
          const enriched = enrichUser(res.user, logout);
          setUser(enriched);
          setMfaPending(false);
          setPendingLoginToken(null);

          logSessionEvent("login_success", {
            user: res.user.username,
          });

          toast.success("Logged in successfully.");
          return "success";
        }

        logSessionEvent("login_failed", { username });
        return "error";
      } catch {
        logSessionEvent("login_error", { username });
        toast.error("Login failed. Check your credentials.");
        return "error";
      }
    },
    [logout]
  );

  /* ------------------------------------------------------------
     verifyMfa(code)
  ------------------------------------------------------------- */
  const verifyMfa = useCallback(
    async (code) => {
      if (!pendingLoginToken) {
        toast.error("No pending MFA session.");
        logSessionEvent("mfa_verify_no_pending");
        return "error";
      }

      logSessionEvent("mfa_verify_attempt");

      try {
        const res = await apiVerifyTotp(pendingLoginToken, code);

        if (res?.user) {
          const enriched = enrichUser(res.user, logout);
          setUser(enriched);
          setMfaPending(false);
          setPendingLoginToken(null);

          logSessionEvent("mfa_success", {
            user: res.user.username,
          });

          toast.success("MFA verified. Welcome!");
          return "success";
        }

        logSessionEvent("mfa_failed");
        return "error";
      } catch {
        logSessionEvent("mfa_error");
        toast.error("Invalid MFA code.");
        return "error";
      }
    },
    [pendingLoginToken, logout]
  );

  /* ------------------------------------------------------------
     Auto-logout when backend session expires
  ------------------------------------------------------------- */
  useEffect(() => {
    if (!user) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch("/api/auth/session-status", {
          credentials: "include",
        });

        if (res.status === 401) {
          logSessionEvent("session_expired_auto_logout");
          toast.warning("Your session has expired.");
          logout();
        }
      } catch (err) {
        console.error("session-status check failed:", err);
      }
    }, 10000);

    return () => clearInterval(interval);
  }, [user, logout]);

  /* ------------------------------------------------------------
     isAuthenticated()
  ------------------------------------------------------------- */
  const isAuthenticated = useCallback(() => !!user, [user]);

  const value = {
    user,
    loading,
    mfaPending,
    pendingLoginToken,
    login,
    verifyMfa,
    logout,
    restoreSession,
    isAuthenticated,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/* ------------------------------------------------------------
   useAuth()
------------------------------------------------------------- */
export function useAuth() {
  return useContext(AuthContext);
}
