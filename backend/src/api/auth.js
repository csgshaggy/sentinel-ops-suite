// File: /home/ubuntu/sentinel-ops-suite/backend/src/api/auth.js
// Unified Frontend Auth API for SentinelOps
// All requests include credentials for session-cookie auth.

// -----------------------------
// LOGIN
// -----------------------------
export async function login(username, password) {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Login failed' }));
    throw new Error(error.detail || 'Login failed');
  }

  return response.json();
}

// -----------------------------
// MFA COMPLETE (if required)
// -----------------------------
export async function completeMfa(userId) {
  const response = await fetch('/api/auth/login/mfa-complete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ user_id: userId }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'MFA failed' }));
    throw new Error(error.detail || 'MFA failed');
  }

  return response.json();
}

// -----------------------------
// LOGOUT
// -----------------------------
export async function logout() {
  const response = await fetch('/api/auth/logout', {
    method: 'POST',
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error('Logout failed');
  }

  return response.json();
}

// -----------------------------
// GET CURRENT USER (session check)
// -----------------------------
export async function getCurrentUser() {
  const response = await fetch('/api/auth/me', {
    method: 'GET',
    credentials: 'include',
  });

  if (!response.ok) {
    return null; // Not authenticated
  }

  return response.json();
}

// -----------------------------
// RESTORE SESSION (optional helper)
// -----------------------------
export async function restoreSession() {
  return getCurrentUser();
}
