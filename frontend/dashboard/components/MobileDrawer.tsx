import React from "react";

import Nav from "../Nav";

export default function MobileDrawer({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  return (
    <div
      className={`fixed inset-0 z-50 md:hidden transition ${
        open ? "block" : "hidden"
      }`}
    >
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black bg-opacity-50"
        onClick={onClose}
      />

      {/* Drawer */}
      <div className="absolute left-0 top-0 h-full w-64 bg-gray-900 dark:bg-gray-950 shadow-xl p-4">
        <button
          onClick={onClose}
          className="text-gray-300 hover:text-white mb-4"
        >
          Close ✕
        </button>

        <Nav collapsed={false} />
      </div>
    </div>
  );
}
