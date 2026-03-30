// =====================================================================
// SSRF Command Console — AuthContext
// Session management • Login • Logout • Role-aware user state
// =====================================================================

import {
  createContext,
  useContext,
  useState,
  useCallback,
  ReactNode,
} from "react";

export type User = {
  id: string;
  email: string;
  role: "admin" | "operator" | "viewer";
};

type AuthContextType = {
  user: User | null;
  authenticated: boolean;
  loading: boolean;

  login: () => Promise<void>;
  logout: () => Promise<void>;
  setUser: (u: User | null) => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUserState] = useState<User | null>(null);
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(false);

  // -------------------------------------------------------------------
  // Session check (/auth/me)
  // -------------------------------------------------------------------
  const login = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch("/auth/me", {
        method: "GET",
        credentials: "include",
      });

      if (res.ok) {
        const data = await res.json();
        setUserState(data.user);
        setAuthenticated(true);
      } else {
        setUserState(null);
        setAuthenticated(false);
      }
    } catch {
      setUserState(null);
      setAuthenticated(false);
    } finally {
      setLoading(false);
    }
  }, []);

  // -------------------------------------------------------------------
  // Logout
  // -------------------------------------------------------------------
  const logout = useCallback(async () => {
    setLoading(true);
    try {
      await fetch("/auth/logout", {
        method: "POST",
        credentials: "include",
      });
    } catch {
      /* ignore network errors */
    } finally {
      setUserState(null);
      setAuthenticated(false);
      setLoading(false);
    }
  }, []);

  // -------------------------------------------------------------------
  // Manual setter (used by registration flows, etc.)
  // -------------------------------------------------------------------
  const setUser = useCallback((u: User | null) => {
    setUserState(u);
    setAuthenticated(!!u);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        authenticated,
        loading,
        login,
        logout,
        setUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}
