import React, { useState } from "react";

import TotpInput from "../../components/mfa/TotpInput";
import { useDisableMfa } from "../../features/mfa-query/useDisableMfa";
import { useEnrollMfa } from "../../features/mfa-query/useEnrollMfa";
import { useMfaStatus } from "../../features/mfa-query/useMfaStatus";
import { useVerifyMfa } from "../../features/mfa-query/useVerifyMfa";

export default function MfaSettingsTailwind() {
  const [code, setCode] = useState("");

  const status = useMfaStatus();
  const enroll = useEnrollMfa();
  const verify = useVerifyMfa();
  const disable = useDisableMfa();

  if (status.isLoading) {
    return <div className="p-6 text-gray-300">Loading MFA status…</div>;
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Multi‑Factor Authentication</h1>

      {/* Enable MFA */}
      {!status.data?.enabled && !enroll.data && (
        <button
          onClick={() => enroll.mutate()}
          className="px-4 py-2 bg-blue-600 text-white rounded shadow hover:bg-blue-700"
        >
          Enable MFA
        </button>
      )}

      {/* Enrollment */}
      {enroll.data && !status.data?.enabled && (
        <div className="space-y-4">
          <img src={enroll.data.qr_code} className="w-48" />

          <p className="text-gray-300">Secret: {enroll.data.secret}</p>

          <TotpInput value={code} onChange={setCode} />

          <button
            onClick={() => verify.mutate(code, { onSuccess: () => status.refetch() })}
            className="px-4 py-2 bg-green-600 text-white rounded shadow hover:bg-green-700"
          >
            Verify
          </button>
        </div>
      )}

      {/* MFA Enabled */}
      {status.data?.enabled && (
        <div className="space-y-4">
          <p className="text-green-400 font-semibold">MFA is enabled</p>

          <button
            onClick={() => disable.mutate(undefined, { onSuccess: () => status.refetch() })}
            className="px-4 py-2 bg-red-600 text-white rounded shadow hover:bg-red-700"
          >
            Disable MFA
          </button>
        </div>
      )}
    </div>
  );
}
