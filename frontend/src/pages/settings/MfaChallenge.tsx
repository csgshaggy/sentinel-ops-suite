// frontend/src/pages/settings/MfaChallenge.tsx

import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function MfaChallenge() {
  const [code, setCode] = useState("");
  const navigate = useNavigate();

  const handleVerify = (e) => {
    e.preventDefault();

    // Fake MFA verification
    if (code.length === 6) {
      localStorage.setItem("mfa_verified", "true");
      navigate("/");
    }
  };

  return (
    <div className="p-8 max-w-md mx-auto">
      <h1 className="text-3xl font-bold mb-6">MFA Challenge</h1>

      <form onSubmit={handleVerify} className="space-y-4">
        <input
          className="w-full border p-2 rounded"
          placeholder="Enter 6-digit code"
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />

        <button
          type="submit"
          className="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700"
        >
          Verify
        </button>
      </form>
    </div>
  );
}
