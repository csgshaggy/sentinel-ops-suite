import React, { useState } from "react";

import TotpInput from "../../components/mfa/TotpInput";
import { useVerifyMfa } from "../../features/mfa-query/useVerifyMfa";

export default function MfaChallenge() {
  const [code, setCode] = useState("");
  const verify = useVerifyMfa();

  const submit = async () => {
    verify.mutate(code, {
      onSuccess: (data: any) => {
        localStorage.setItem("access_token", data.access_token);
        window.location.href = "/";
      },
    });
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>MFA Verification</h1>

      {verify.isError && (
        <div style={{ color: "red" }}>{(verify.error as Error).message}</div>
      )}

      <TotpInput value={code} onChange={setCode} />

      <button
        onClick={submit}
        disabled={verify.isPending}
        style={{ marginLeft: "1rem" }}
      >
        {verify.isPending ? "Verifying..." : "Verify"}
      </button>
    </div>
  );
}
