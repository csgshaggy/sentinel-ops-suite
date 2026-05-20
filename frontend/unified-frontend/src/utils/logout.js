// /src/utils/logout.js

import apiClient from "../api/apiClient.js";

/**
 * logout()
 * Low-level logout request helper.
 * - Calls backend logout endpoint
 * - Does NOT redirect (AuthContext handles navigation)
 */
export async function logout() {
  try {
    await apiClient.post("/auth/logout");
  } catch {
    // ignore — AuthContext handles fallback cleanup
  }
}
