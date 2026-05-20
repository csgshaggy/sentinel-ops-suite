import React from "react";

import ThemeToggle from "./ThemeToggle";

export default function StatusBar() {
  return (
    <div className="w-full bg-gray-900 text-gray-300 px-4 py-2 flex items-center justify-between border-b border-gray-700">
      <div className="flex items-center space-x-4">
        <span className="font-semibold text-white">Sentinel Ops Suite</span>
        <span className="text-sm text-green-400">● Backend Online</span>
        <span className="text-sm text-blue-400">● Dashboard Active</span>
      </div>

      <div className="flex items-center space-x-4">
        <ThemeToggle />
      </div>
    </div>
  );
}
