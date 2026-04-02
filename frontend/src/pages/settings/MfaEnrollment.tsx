import React, { useState } from "react";

import TotpInput from "../../components/mfa/TotpInput";
import { useEnrollMfa } from "../../features/mfa-query/useEnrollMfa";
import { useVerifyMfa } from "../../features/mfa-query/useVerifyMfa";

export default function MfaEnrollment() {
  const [code, setCode] = useState("");

  const enroll = useEnrollMfa();
  const verify = useVerifyMfa();

  const start = () => enroll.mutate();
  const submit = () => verify.mutate(code);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>MFA Enrollment</h1>

      {enroll.isError && <div style={{ color: "red" }}>{(enroll.error as Error).message}</div>}

      {!enroll.data && (
        <button onClick={start} disabled={enroll.isPending}>
          {enroll.isPending ? "Starting..." : "Start Enrollment"}
        </button>
      )}

      {enroll.data && (
        <>
          <img
            src={enroll.data.qr_code}
            alt="QR Code"
            style={{ width: 200, marginBottom: "1rem" }}
          />

          <p>Secret: {enroll.data.secret}</p>

          <TotpInput value={code} onChange={setCode} />

          <button onClick={submit} disabled={verify.isPending} style={{ marginLeft: "1rem" }}>
            {verify.isPending ? "Verifying..." : "Verify"}
          </button>

          {verify.isError && (
            <div style={{ color: "red", marginTop: "1rem" }}>{(verify.error as Error).message}</div>
          )}

          {verify.isSuccess && (
            <div style={{ color: "green", marginTop: "1rem" }}>MFA Enabled Successfully</div>
          )}
        </>
      )}
    </div>
  );
}
