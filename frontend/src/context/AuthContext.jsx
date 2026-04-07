import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useRef,
} from "react";
import axios from "axios";

const AuthContext = createContext();

// Dedicated axios instance for authenticated calls
const api = axios.create({
  baseURL: "/api",
});

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("authUser");
    return stored ? JSON.parse(stored) : null;
  });

  const [loading, setLoading] = useState(false);
  const isRefreshingRef = useRef(false);
  const refreshQueueRef = useRef([]);

  // ---------------------------
  // Persist user session
  // ---------------------------
  useEffect(() => {
    if (user) {
      localStorage.setItem("authUser", JSON.stringify(user));
    } else {
      localStorage.removeItem("authUser");
    }
  }, [user]);

  // ---------------------------
  // Attach auth interceptor
  // ---------------------------
  useEffect(() => {
    const requestInterceptor = api.interceptors.request.use(
      (config) => {
        if (user?.token) {
          config.headers.Authorization = `Bearer ${user.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    const responseInterceptor = api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        // If unauthorized and we have a refresh token, try to refresh
        if (
          error.response &&
          error.response.status === 401 &&
          user?.refreshToken &&
          !originalRequest._retry
        ) {
          originalRequest._retry = true;

          if (isRefreshingRef.current) {
            // Queue requests while a refresh is in progress
            return new Promise((resolve, reject) => {
              refreshQueueRef.current.push({ resolve, reject, originalRequest });
            });
          }

          isRefreshingRef.current = true;

          try {
            const newTokens = await refreshToken(user.refreshToken);

            const updatedUser = {
              ...user,
              token: newTokens.access_token,
              refreshToken: newTokens.refresh_token || user.refreshToken,
            };

            setUser(updatedUser);

            // Retry queued requests
            refreshQueueRef.current.forEach(({ resolve, originalRequest }) => {
              originalRequest.headers.Authorization = `Bearer ${updatedUser.token}`;
              resolve(api(originalRequest));
            });
            refreshQueueRef.current = [];

            // Retry the original request
            originalRequest.headers.Authorization = `Bearer ${updatedUser.token}`;
            return api(originalRequest);
          } catch (refreshError) {
            refreshQueueRef.current.forEach(({ reject }) =>
              reject(refreshError)
            );
            refreshQueueRef.current = [];
            setUser(null);
            return Promise.reject(refreshError);
          } finally {
            isRefreshingRef.current = false;
          }
        }

        return Promise.reject(error);
      }
    );

    return () => {
      api.interceptors.request.eject(requestInterceptor);
      api.interceptors.response.eject(responseInterceptor);
    };
  }, [user]);

  // ---------------------------
  // Refresh token call
  // ---------------------------
  const refreshToken = async (refreshTokenValue) => {
    const response = await axios.post("/api/auth/refresh", {
      refresh_token: refreshTokenValue,
    });
    return response.data;
  };

  // ---------------------------
  // Login Handler
  // ---------------------------
  const login = async (username, password) => {
    setLoading(true);

    try {
      const response = await axios.post("/api/auth/login", {
        username,
        password,
      });

      const authUser = {
        username: response.data.username,
        role: response.data.role,
        token: response.data.access_token,
        refreshToken: response.data.refresh_token,
      };

      setUser(authUser);
      return authUser;
    } finally {
      setLoading(false);
    }
  };

  // ---------------------------
  // Logout Handler
  // ---------------------------
  const logout = () => {
    setUser(null);
    localStorage.removeItem("authUser");
  };

  // ---------------------------
  // Context Value
  // ---------------------------
  const value = {
    user,
    login,
    logout,
    loading,
    isAuthenticated: !!user,
    role: user?.role || null,
    api, // use this for authenticated API calls
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
