import "./Login.css";
import { useState } from "react";
import { requestPasswordReset } from "../";
import { useNavigate } from "react-router-dom";
import logo from "../assets/SentinelOps.jpg";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    const res = await requestPasswordReset(email);
    setLoading(false);

    if (res?.error) {
      setError(res.error);
      return;
    }

    setSent(true);
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <img src={logo} alt="Sentinel Ops Logo" className="auth-logo" />

        {!sent ? (
          <>
            <h1 className="auth-title">Forgot Password</h1>
            <h2 className="auth-subtitle">
              Enter your email to receive a reset link
            </h2>

            {error && <div className="auth-error">{error}</div>}

            <form className="auth-form" onSubmit={handleSubmit}>
              <label>Email Address</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="email"
                required
              />

              <button type="submit" disabled={loading}>
                {loading ? "Sending..." : "Send Reset Link"}
              </button>
            </form>

            <div className="auth-footer">
              <a onClick={() => navigate("/")}>Back to Login</a>
            </div>
          </>
        ) : (
          <>
            <h1 className="auth-title">Check Your Email</h1>
            <h2 className="auth-subtitle">
              A password reset link has been sent.
            </h2>

            <div className="auth-footer">
              <a onClick={() => navigate("/")}>Return to Login</a>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
