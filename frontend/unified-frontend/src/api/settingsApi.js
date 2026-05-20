// /src/api/settingsApi.js

// ------------------------------------------------------------
// Generic API wrapper (same pattern as /api/auth.js)
// ------------------------------------------------------------
async function apiRequest(path, options = {}) {
  try {
    const res = await fetch(path, {
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      ...options,
    });

    let data = null;
    try {
      data = await res.json();
    } catch {
      data = null;
    }

    return {
      ok: res.ok,
      status: res.status,
      data,
    };
  } catch (err) {
    console.error("API request failed:", err);
    return {
      ok: false,
      status: 0,
      data: { detail: "Network error" },
    };
  }
}

// ------------------------------------------------------------
// GET USER SETTINGS (DB-backed)
// ------------------------------------------------------------
export async function fetchSettings() {
  const res = await apiRequest("/api/settings", {
    method: "GET",
  });

  if (!res.ok) {
    return { error: res.data?.detail || "Failed to load settings" };
  }

  return res.data;
}

// ------------------------------------------------------------
// UPDATE USER SETTINGS (DB-backed)
// ------------------------------------------------------------
export async function updateSettings(payload) {
  const res = await apiRequest("/api/settings", {
    method: "PATCH",
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    return { error: res.data?.detail || "Failed to update settings" };
  }

  return res.data;
}

// ------------------------------------------------------------
// MFA: START ENROLLMENT
// ------------------------------------------------------------
export async function startMfaEnrollment() {
  const res = await apiRequest("/api/mfa/enroll", {
    method: "POST",
  });

  if (!res.ok) {
    return { error: res.data?.detail || "Failed to start MFA enrollment" };
  }

  return res.data; // contains QR code URL or secret
}

// ------------------------------------------------------------
// MFA: VERIFY ENROLLMENT CODE
// ------------------------------------------------------------
export async function verifyMfaEnrollment(code) {
  const res = await apiRequest("/api/mfa/verify", {
    method: "POST",
    body: JSON.stringify({ code }),
  });

  if (!res.ok) {
    return { error: res.data?.detail || "Invalid MFA code" };
  }

  return res.data;
}

// ------------------------------------------------------------
// MFA: DISABLE
// ------------------------------------------------------------
export async function disableMfa() {
  const res = await apiRequest("/api/mfa/disable", {
    method: "POST",
  });

  if (!res.ok) {
    return { error: res.data?.detail || "Failed to disable MFA" };
  }

  return res.data;
}

// ------------------------------------------------------------
// Default export (for compatibility with existing imports)
// ------------------------------------------------------------
export default {
  fetchSettings,
  updateSettings,
  startMfaEnrollment,
  verifyMfaEnrollment,
  disableMfa,
};
