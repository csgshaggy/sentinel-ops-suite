// /src/utils/isAuthRoute.js

/**
 * Determines whether a route belongs to the public/auth namespace.
 *
 * Public routes include:
 * - /login
 * - /mfa
 * - /reset-password
 * - /reset-password-request
 * - /forgot-password
 * - /auth/*
 *
 * Admin routes (/admin/*) must NEVER be treated as public.
 */

const AUTH_ROUTE_PREFIXES = [
  "/login",
  "/mfa",
  "/reset-password",
  "/reset-password-request",
  "/forgot-password",
  "/auth",
];

export function isAuthRoute(pathname) {
  // 🔒 Never treat admin routes as public
  if (pathname.startsWith("/admin")) return false;

  // 🔍 Only match exact prefix or prefix + "/"
  return AUTH_ROUTE_PREFIXES.some((prefix) =>
    pathname === prefix || pathname.startsWith(prefix + "/")
  );
}
