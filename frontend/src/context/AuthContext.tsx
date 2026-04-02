import React, { createContext, useContext, useEffect,useState } from "react";

export interface User {
  id: string;
  email: string;
  role: string;
}

export interface AuthContextType {
  authenticated: boolean;
  user: User | null;
  loading: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [authenticated, setAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // placeholder for token restore
    setLoading(false);
  }, []);

  const login = (token: string, userData: User) => {
    // store token if needed
    setUser(userData);
    setAuthenticated(true);
  };

  const logout = () => {
    setUser(null);
    setAuthenticated(false);
  };

  const value: AuthContextType = {
    authenticated,
    user,
    loading,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("AuthContext used outside AuthProvider");
  return ctx;
};
