import { useEffect, useState } from "react";

export default function MfaSettingsTailwind() {
  const [verify, setVerify] = useState<any>(null);

  useEffect(() => {
    import("../../features/mfa-query/useVerifyMfa").then((mod) => {
      setVerify(() => mod.useVerifyMfa());
    });
  }, []);

  if (!verify) return <div className="p-4">Loading MFA module…</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">MFA Settings (Tailwind)</h1>
      <p className="mt-2 text-gray-600">
        Manage your multi‑factor authentication settings.
      </p>

      <button
        className="mt-6 px-4 py-2 bg-blue-600 text-white rounded"
        onClick={() => verify.mutate()}
      >
        Verify MFA
      </button>
    </div>
  );
}
