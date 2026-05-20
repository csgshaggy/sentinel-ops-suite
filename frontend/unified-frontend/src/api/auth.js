// /src/api/auth.js

// ------------------------------------------------------------
// Generic API wrapper
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
// LOGIN (username + password)
// Backend returns: { success: true, user: {...} }
// ------------------------------------------------------------
export async function login(username, password) {
  const res = await apiRequest("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });

  // MFA required
  if (res.data?.mfa_required) {
    return {
      mfa_required: true,
      pending_login_token: res.data?.pending_login_token,
      delivery_hint: res.data?.delivery_hint,
    };
  }

  // Login error
  if (!res.ok || !res.data?.success) {
    return { error: res.data?.detail || "Invalid credentials" };
  }

  // Successful login
  return {
    success: true,
    user: res.data.user,
  };
}

// ------------------------------------------------------------
// VERIFY TOTP (MFA)
// Backend returns: { success: true, user: {...} }
// ------------------------------------------------------------
export async function verifyTotp(pending_login_token, code) {
  const res = await apiRequest("/api/auth/verify-totp", {
    method: "POST",
    body: JSON.stringify({ pending_login_token, code }),
  });

  if (!res.ok || !res.data?.success) {
    return { error: res.data?.detail || "Invalid code" };
  }

  return {
    success: true,
    user: res.data.user,
  };
}

// ------------------------------------------------------------
// RESTORE SESSION
// Backend returns: { success: true/false, user: {...} }
// ------------------------------------------------------------
export async function restoreSession() {
  const res = await apiRequest("/api/auth/session/restore", {
    method: "GET",
  });

  if (!res.ok) {
    console.error("Session restore failed:", res.status);
    return { success: false, user: null };
  }

  // Return the full backend object:
  // { success: true, user: {...} }
  return res.data;
}

// ------------------------------------------------------------
// HEARTBEAT
// ------------------------------------------------------------
export async function heartbeat() {
  const res = await apiRequest("/api/auth/heartbeat", {
    method: "POST",
  });

  return res.ok;
}

// ------------------------------------------------------------
// LOGOUT
// ------------------------------------------------------------
export async function logout() {
  await apiRequest("/api/auth/logout", {
    method: "POST",
  });

  return true;
}
