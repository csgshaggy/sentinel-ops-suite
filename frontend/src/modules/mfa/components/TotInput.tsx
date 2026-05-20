import { useState } from "react";

interface TotpInputProps {
  onSubmit: (code: string) => void;
  isLoading?: boolean;
}

export function TotpInput({ onSubmit, isLoading }: TotpInputProps) {
  const [code, setCode] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (code.trim().length === 6) {
      onSubmit(code.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3">
      <input
        type="text"
        inputMode="numeric"
        maxLength={6}
        value={code}
        onChange={(e) => setCode(e.target.value)}
        className="border rounded px-3 py-2 text-center tracking-widest text-lg"
        placeholder="123456"
        disabled={isLoading}
      />

      <button
        type="submit"
        disabled={isLoading || code.length !== 6}
        className="bg-blue-600 text-white py-2 rounded disabled:opacity-50"
      >
        {isLoading ? "Verifying..." : "Verify Code"}
      </button>
    </form>
  );
}
