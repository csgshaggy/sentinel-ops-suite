import { useContext, useState } from "react";

import { loginRequest } from "../api/auth";
import { AuthContext } from "../context/AuthContext";

export default function Login() {
  const { login } = useContext(AuthContext);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const data = await loginRequest(email, password);
      login(data.access_token);
      window.location.href = "/"; // redirect to dashboard
    } catch (err) {
      setError("Invalid email or password");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-container">
      <form className="login-box" onSubmit={handleSubmit}>
        <h2>Sign In</h2>

        {error && <div className="error">{error}</div>}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Signing in..." : "Login"}
        </button>
      </form>

      <style>{`
        .login-container {
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          background: var(--bg);
        }

        .login-box {
          background: var(--panel);
          padding: 2rem;
          border-radius: 8px;
          width: 320px;
          display: flex;
          flex-direction: column;
          gap: 1rem;
          box-shadow: 0 0 20px rgba(0,0,0,0.2);
        }

        input {
          padding: 0.75rem;
          border-radius: 6px;
          border: 1px solid var(--border);
          background: var(--input-bg);
          color: var(--text);
        }

        button {
          padding: 0.75rem;
          background: var(--accent);
          color: white;
          border: none;
          border-radius: 6px;
          cursor: pointer;
        }

        .error {
          background: #ff4d4d;
          color: white;
          padding: 0.5rem;
          border-radius: 4px;
          text-align: center;
        }
      `}</style>
    </div>
  );
}
