import React, { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import TextInput from "../components/forms/TextInput";
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

  // ---------------------------
  // Advanced Validation Rules
  // ---------------------------
  const validateField = (name, value) => {
    switch (name) {
      case "username":
        if (!value.trim()) return "Username is required";
        if (value.length < 3) return "Must be at least 3 characters";
        if (!/^[a-zA-Z0-9._-]+$/.test(value))
          return "Only letters, numbers, ., _, - allowed";
        return "";

      case "password":
        if (!value.trim()) return "Password is required";
        if (value.length < 8) return "Must be at least 8 characters";
        if (!/[A-Z]/.test(value)) return "Must include an uppercase letter";
        if (!/[a-z]/.test(value)) return "Must include a lowercase letter";
        if (!/[0-9]/.test(value)) return "Must include a number";
        if (!/[^A-Za-z0-9]/.test(value)) return "Must include a symbol";
        return "";

      default:
        return "";
    }
  };

  // ---------------------------
  // Debounced Real-Time Validation (Phase 2)
  // ---------------------------
  useEffect(() => {
    const timer = setTimeout(() => {
      const newErrors = {};

      Object.keys(form).forEach((field) => {
        if (touched[field]) {
          newErrors[field] = validateField(field, form[field]);
        }
      });

      setErrors((prev) => ({ ...prev, ...newErrors }));
    }, 250); // 250ms debounce

    return () => clearTimeout(timer);
  }, [form, touched]);

  // ---------------------------
  // Input Change Handler
  // ---------------------------
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

  // ---------------------------
  // Final Form Validation
  // ---------------------------
  const validateForm = () => {
    const newErrors = {
      username: validateField("username", form.username),
      password: validateField("password", form.password),
    };

    setErrors(newErrors);

    return !newErrors.username && !newErrors.password;
  };

  // ---------------------------
  // Submit Handler
  // ---------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError("");

    if (!validateForm()) return;

    try {
      await login(form.username, form.password);
    } catch (err) {
      setSubmitError("Invalid username or password");
    }
  };

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
