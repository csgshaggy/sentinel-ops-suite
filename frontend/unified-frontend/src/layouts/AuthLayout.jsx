// /src/layouts/AuthLayout.jsx


/**
 * AuthLayout
 * - Used ONLY for public authentication routes:
 *   /login, /mfa, /reset-password, /forgot-password, etc.
 * - Fully isolated from the main application layout.
 * - No Sidebar, No TopBar, No SessionManager.
 * - Provides centered auth container on animated grid background.
 */
export default function AuthLayout({ children }) {
  return (
    <div className="auth-layout">
      <div className="auth-center">
        {children}
      </div>
    </div>
  );
}
