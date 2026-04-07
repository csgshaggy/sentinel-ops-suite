import React, { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import TextInput from "../components/forms/TextInput";
import {
  validateUsername,
  validatePassword,
  validateLoginForm
} from "../utils/validation/loginSchema";
import "./Login.css";

export default function Login() {
  const { login, loading } = useAuth();

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const [errors, setErrors] = useState({
    username: "",
    password: "",
  });

  const [touched, setTouched] = useState({
    username: false,
    password: false,
  });

  const [submitError, setSubmitError] = useState("");

  // Debounced real-time validation
  useEffect(() => {
    const timer = setTimeout(() => {
      const newErrors = {};

      if (touched.username) {
        newErrors.username = validateUsername(form.username);
      }

      if (touched.password) {
        newErrors.password = validatePassword(form.password);
      }

      setErrors((prev) => ({ ...prev, ...newErrors }));
    }, 250);

    return () => clearTimeout(timer);
  }, [form, touched]);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));

    setTouched((prev) => ({
      ...prev,
      [name]: true,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError("");

    const result = validateLoginForm(form);
    setErrors({
      username: result.username,
      password: result.password,
    });

    if (!result.isValid) return;

    try {
      await login(form.username, form.password);
    } catch (err) {
      setSubmitError("Invalid username or password");
    }
  };

  const isUsernameValid =
    touched.username &&
    !errors.username &&
    form.username.trim() !== "";

  const isPasswordValid =
    touched.password &&
    !errors.password &&
    form.password.trim() !== "";

  return (
    <div className="login-page">
      <div className="login-card">
        <h1 className="login-title">Operator Login</h1>

        {submitError && <div className="login-error">{submitError}</div>}

        <form className="login-form" onSubmit={handleSubmit}>
          <TextInput
            id="username"
            label="Username"
            type="text"
            value={form.username}
            onChange={handleChange}
            autoComplete="username"
            required
            error={errors.username}
            valid={isUsernameValid}
          />

          <TextInput
            id="password"
            label="Password"
            type="password"
            value={form.password}
            onChange={handleChange}
            autoComplete="current-password"
            required
            error={errors.password}
            valid={isPasswordValid}
          />

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading ? "Authenticating..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
}
