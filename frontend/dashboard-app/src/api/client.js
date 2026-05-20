// frontend/dashboard-app/src/api/client.js

export async function apiFetch(url, options = {}) {
  const opts = {
    credentials: "include",
    ...options,
  };

  const res = await fetch(url, opts);

  // Auto-redirect on expired session
  if (res.status === 401) {
    window.location.href = "/login/";
    return; // prevent further processing
  }

  return res;
}
