// /src/api/apiClient.js
// ============================================================
// SentinelOps — Operator‑Grade API Client (Unified Backend)
// - Fetch-based (deterministic, low drift)
// - JSON parsing with fallback
// - Timeout protection
// - Credentials included by default
// - Automatic FormData handling
// - 401 Unauthorized interceptor (AuthContext-driven)
// - Axios-style wrapper for compatibility
// ============================================================

const DEFAULT_TIMEOUT = 12_000; // 12 seconds
const BASE_URL = "/api";

// ------------------------------------------------------------
// 401 handler registration (set by AuthContext)
// ------------------------------------------------------------
let onUnauthorized = null;
let unauthorizedLock = false;

export function setUnauthorizedHandler(handler) {
  onUnauthorized = typeof handler === "function" ? handler : null;
}

function triggerUnauthorizedOnce(meta = {}) {
  if (unauthorizedLock) return;
  unauthorizedLock = true;

  try {
    onUnauthorized?.(meta);
  } finally {
    setTimeout(() => {
      unauthorizedLock = false;
    }, 1500);
  }
}

// ------------------------------------------------------------
// Normalize path to avoid double /api/api
// ------------------------------------------------------------
function normalizePath(path) {
  if (path.startsWith("/api/")) return path;
  if (path.startsWith("api/")) return "/" + path;
  return BASE_URL + path;
}

// ------------------------------------------------------------
// Core API client
// ------------------------------------------------------------
export async function apiClient(path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT);

  const isFormData = options.body instanceof FormData;
  const noJSON = options.noJSON === true;

  try {
    const res = await fetch(normalizePath(path), {
      credentials: "include",
      signal: controller.signal,

      headers: isFormData
        ? {
            ...(options.headers || {}),
          }
        : {
            "Content-Type": "application/json",
            Accept: "application/json",
            ...(options.headers || {}),
          },

      ...options,
    });

    clearTimeout(timeout);

    // --------------------------------------------------------
    // Parse JSON unless explicitly disabled
    // --------------------------------------------------------
    let data = null;
    if (!noJSON) {
      try {
        data = await res.json();
      } catch {
        data = null;
      }
    }

    // --------------------------------------------------------
    // 401 interceptor
    // --------------------------------------------------------
    if (res.status === 401) {
      triggerUnauthorizedOnce({
        path,
        method: options.method || "GET",
        status: res.status,
      });
    }

    return {
      ok: res.ok,
      status: res.status,
      data,
      raw: res,
    };
  } catch (err) {
    clearTimeout(timeout);

    if (err.name === "AbortError") {
      return {
        ok: false,
        status: 0,
        data: { detail: "Request timed out" },
      };
    }

    return {
      ok: false,
      status: 0,
      data: { detail: "Network error" },
    };
  }
}

// ============================================================
// Convenience helpers
// ============================================================

export function get(path, extraOptions = {}) {
  return apiClient(path, {
    method: "GET",
    ...extraOptions,
  });
}

export function post(path, body, extraOptions = {}) {
  if (body instanceof FormData) {
    return apiClient(path, {
      method: "POST",
      body,
      ...extraOptions,
      headers: {
        ...(extraOptions.headers || {}),
      },
    });
  }

  return apiClient(path, {
    method: "POST",
    body: JSON.stringify(body),
    ...extraOptions,
    headers: {
      "Content-Type": "application/json",
      ...(extraOptions.headers || {}),
    },
  });
}

export function put(path, body, extraOptions = {}) {
  return apiClient(path, {
    method: "PUT",
    body: JSON.stringify(body),
    ...extraOptions,
    headers: {
      "Content-Type": "application/json",
      ...(extraOptions.headers || {}),
    },
  });
}

export function del(path, extraOptions = {}) {
  return apiClient(path, {
    method: "DELETE",
    ...extraOptions,
  });
}

// ============================================================
// Axios‑style wrapper (compatibility)
// ============================================================
const client = {
  get,
  post,
  put,
  delete: del,
};

export default client;
