import React, { useState } from "react";

export default function RepoHealthPanel() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runHealth = async () => {
    setLoading(true);
    const res = await fetch("/validators/run");
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">Repo Health</h1>

      <button
        onClick={runHealth}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        {loading ? "Running..." : "Run Repo Health"}
      </button>

      {result && (
        <div className="space-y-4">
          <div
            className={`px-3 py-1 rounded ${
              result.exit_code === 0
                ? "bg-green-600 text-white"
                : "bg-red-600 text-white"
            }`}
          >
            Exit Code: {result.exit_code}
          </div>

          <div>
            <h2 className="font-semibold">Stdout</h2>
            <pre className="bg-black text-green-400 p-3 rounded max-h-64 overflow-auto">
              {result.stdout}
            </pre>
          </div>

          <div>
            <h2 className="font-semibold">Stderr</h2>
            <pre className="bg-black text-red-400 p-3 rounded max-h-64 overflow-auto">
              {result.stderr}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
