// /src/api/apiClient.js
// ============================================================
// Operator‑Grade API Client
// Centralized fetch wrapper with:
// - JSON parsing
// - Error normalization
// - Timeout protection
// - Credentials included by default
// - Automatic FormData handling (file uploads)
// - 401 Unauthorized handler ("interceptor"-style)
// ============================================================

const DEFAULT_TIMEOUT = 12_000; // 12 seconds

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
// Core API client
// ------------------------------------------------------------
export async function apiClient(path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT);

  const isFormData = options.body instanceof FormData;

  try {
    const res = await fetch(path, {
      credentials: "include", // ⭐ ALWAYS send cookies
      signal: controller.signal,

      // ⭐ Only set JSON headers when NOT sending FormData
      headers: isFormData
        ? {
            ...(options.headers || {}),
          }
        : {
            "Content-Type": "application/json",
            ...(options.headers || {}),
          },

      ...options,
    });

    clearTimeout(timeout);

    // Try to parse JSON, but tolerate non‑JSON responses
    let data = null;
    try {
      data = await res.json();
    } catch {
      data = null;
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
    };
  } catch (err) {
    clearTimeout(timeout);

    if (err.name === "AbortError") {
      console.error("API timeout:", path);
      return {
        ok: false,
        status: 0,
        data: { detail: "Request timed out" },
      };
    }

    console.error("API network error:", err);
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

// GET ---------------------------------------------------------
export function get(path, extraOptions = {}) {
  return apiClient(path, {
    method: "GET",
    ...extraOptions,
  });
}

// POST --------------------------------------------------------
export function post(path, body, extraOptions = {}) {
  // ⭐ Special case: FormData (file uploads)
  if (body instanceof FormData) {
    return apiClient(path, {
      method: "POST",
      body, // raw FormData
      ...extraOptions,
      headers: {
        ...(extraOptions.headers || {}), // DO NOT set Content-Type
      },
    });
  }

  // ⭐ Normal JSON POST
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

// PUT ---------------------------------------------------------
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

// DELETE ------------------------------------------------------
export function del(path, extraOptions = {}) {
  return apiClient(path, {
    method: "DELETE",
    ...extraOptions,
  });
}

// ============================================================
// Axios‑style wrapper (for compatibility with existing code)
// ============================================================
const client = {
  get,
  post,
  put,
  delete: del,
};

export default client;
