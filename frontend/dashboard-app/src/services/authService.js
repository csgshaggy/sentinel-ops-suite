// frontend/dashboard-app/src/services/authService.js

const API_BASE = "/api/auth";

export async function login(username, password) {
  const response = await fetch(`${API_BASE}/login`, {
    method: "POST",
    credentials: "include", // REQUIRED for cookies
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || "Login failed");
  }

  return response.json();
}

export async function logout() {
  await fetch("/api/auth/logout", {
    method: "POST",
    credentials: "include",
  });
}

export function getToken() {
  return null; // no JWTs anymore — cookie handles auth
}

export function authHeader() {
  return {}; // not needed for cookie sessions
}
