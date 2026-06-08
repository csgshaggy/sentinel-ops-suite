// /src/utils/axiosInstance.js
// SentinelOps — Unified Axios Instance with Global Error Boundary

import axios from "axios";
import { emitApiError } from "../components/apiErrorBus.js";
import { logout } from "./logout.js";

const api = axios.create({
  baseURL: "/api",
  withCredentials: true,
});

// ------------------------------------------------------------
// Request Interceptor
// ------------------------------------------------------------
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    emitApiError({
      type: "request",
      message: "Failed to send request.",
      error,
    });
    return Promise.reject(error);
  }
);

// ------------------------------------------------------------
// Response Interceptor
// ------------------------------------------------------------
api.interceptors.response.use(
  (response) => response,

  (error) => {
    const status = error?.response?.status;

    // -------------------------------
    // Session expired
    // -------------------------------
    if (status === 401 || status === 419) {
      emitApiError({
        type: "auth",
        message: "Your session has expired. Redirecting to login...",
        error,
      });

      logout(); // clears cookies + redirects
      return Promise.reject(error);
    }

    // -------------------------------
    // Forbidden
    // -------------------------------
    if (status === 403) {
      emitApiError({
        type: "forbidden",
        message: "You do not have permission to perform this action.",
        error,
      });
      return Promise.reject(error);
    }

    // -------------------------------
    // Server errors
    // -------------------------------
    if (status >= 500) {
      emitApiError({
        type: "server",
        message: "A server error occurred.",
        error,
      });
      return Promise.reject(error);
    }

    // -------------------------------
    // Network / unknown errors
    // -------------------------------
    emitApiError({
      type: "network",
      message: "A network error occurred.",
      error,
    });

    return Promise.reject(error);
  }
);

export default api;
