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
  // Normalize (remove trailing slash except root)
  if (pathname.length > 1 && pathname.endsWith("/")) {
    pathname = pathname.slice(0, -1);
  }

  const isPublic = AUTH_ROUTE_PREFIXES.some(
    (prefix) =>
      pathname === prefix || pathname.startsWith(prefix + "/")
  );

  return isPublic;
}
