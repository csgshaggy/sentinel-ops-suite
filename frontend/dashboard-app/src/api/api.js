// src/api/api.js

import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  withCredentials: true,
});

// Optional: handle 401 → session expired
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response && err.response.status === 401) {
      window.dispatchEvent(new Event("session-expired"));
    }
    return Promise.reject(err);
  }
);

export default api;
