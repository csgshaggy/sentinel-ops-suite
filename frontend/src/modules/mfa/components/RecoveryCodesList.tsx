interface RecoveryCodesListProps {
  codes: string[];
}

export function RecoveryCodesList({ codes }: RecoveryCodesListProps) {
  return (
    <div className="bg-gray-100 p-4 rounded border">
      <h3 className="font-semibold mb-2">Recovery Codes</h3>

      <ul className="grid grid-cols-2 gap-2 font-mono text-sm">
        {codes.map((code) => (
          <li key={code} className="bg-white p-2 rounded border text-center">
            {code}
          </li>
        ))}
      </ul>

      <p className="text-xs text-gray-600 mt-3">
        Store these codes somewhere safe. Each code can be used once.
      </p>
    </div>
  );
}
