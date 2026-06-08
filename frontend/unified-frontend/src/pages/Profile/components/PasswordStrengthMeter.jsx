// /src/pages/Profile/components/PasswordStrengthMeter.jsx
// SentinelOps — Password Strength Meter (Neon‑Glassy)

import "./PasswordStrengthMeter.css";

export default function PasswordStrengthMeter({ password }) {
  if (!password) {
    return <div className="password-strength-meter empty"></div>;
  }

  const score = calculateStrength(password);

  return (
    <div className="password-strength-meter">
      <div className={`strength-bar s1 ${score >= 1 ? "active" : ""}`}></div>
      <div className={`strength-bar s2 ${score >= 2 ? "active" : ""}`}></div>
      <div className={`strength-bar s3 ${score >= 3 ? "active" : ""}`}></div>
      <div className={`strength-bar s4 ${score >= 4 ? "active" : ""}`}></div>

      <div className="strength-label">
        {score === 1 && "Weak"}
        {score === 2 && "Fair"}
        {score === 3 && "Good"}
        {score === 4 && "Strong"}
      </div>
    </div>
  );
}

function calculateStrength(pw) {
  let score = 0;

  if (pw.length >= 8) score++;
  if (/[A-Z]/.test(pw)) score++;
  if (/[0-9]/.test(pw)) score++;
  if (/[^A-Za-z0-9]/.test(pw)) score++;

  return score;
}
