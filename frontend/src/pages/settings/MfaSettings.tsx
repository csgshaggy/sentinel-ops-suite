import React, { useState } from "react";

import TotpInput from "../../components/mfa/TotpInput";
import { useDisableMfa } from "../../features/mfa-query/useDisableMfa";
import { useEnrollMfa } from "../../features/mfa-query/useEnrollMfa";
import { useMfaStatus } from "../../features/mfa-query/useMfaStatus";
import { useVerifyMfa } from "../../features/mfa-query/useVerifyMfa";

export default function MfaSettings() {
  const [code, setCode] = useState("");

  const status = useMfaStatus();
  const enroll = useEnrollMfa();
  const verify = useVerifyMfa();
  const disable = useDisableMfa();

  const start = () => enroll.mutate();
  const submit = () => verify.mutate(code, { onSuccess: () => status.refetch() });
  const turnOff = () => disable.mutate(undefined, { onSuccess: () => status.refetch() });

  if (status.isLoading) return <div>Loading MFA status...</div>;

  return (
    <div style={{ padding: "2rem" }}>
      <h1>MFA Settings</h1>

      {/* ---------------------- */}
      {/* MFA Disabled           */}
      {/* ---------------------- */}
      {!status.data?.enabled && !enroll.data && (
        <button onClick={start} disabled={enroll.isPending}>
          {enroll.isPending ? "Starting..." : "Enable MFA"}
        </button>
      )}

      {/* ---------------------- */}
      {/* Enrollment Step        */}
      {/* ---------------------- */}
      {enroll.data && !status.data?.enabled && (
        <div>
          <h3>Scan this QR Code</h3>

          <img
            src={enroll.data.qr_code}
            alt="QR Code"
            style={{ width: 200, marginBottom: "1rem" }}
          />

          <p>Secret: {enroll.data.secret}</p>

          <TotpInput value={code} onChange={setCode} />

          <button
            onClick={submit}
            disabled={verify.isPending}
            style={{ marginLeft: "1rem" }}
          >
            {verify.isPending ? "Verifying..." : "Verify"}
          </button>

          {verify.isError && (
            <div style={{ color: "red", marginTop: "1rem" }}>
              {(verify.error as Error).message}
            </div>
          )}
        </div>
      )}

      {/* ---------------------- */}
      {/* MFA Enabled            */}
      {/* ---------------------- */}
      {status.data?.enabled && (
        <div>
          <h3>MFA is enabled</h3>

          <button onClick={turnOff} disabled={disable.isPending}>
            {disable.isPending ? "Disabling..." : "Disable MFA"}
          </button>

          {disable.isError && (
            <div style={{ color: "red", marginTop: "1rem" }}>
              {(disable.error as Error).message}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
