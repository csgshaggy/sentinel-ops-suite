import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { User, LogOut, Settings, ChevronDown } from "lucide-react";
import { GlassPanel, NeonDivider } from "@/components/ui";

export default function UserMenu({ user, onLogout }) {
  const [open, setOpen] = useState(false);
  const menuRef = useRef(null);

  const toggleMenu = () => setOpen((prev) => !prev);

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("touchstart", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("touchstart", handleClickOutside);
    };
  }, []);

  return (
    <div ref={menuRef} className="relative">
      {/* Trigger */}
      <button
        onClick={toggleMenu}
        className="group flex items-center gap-2 px-3 py-1.5 rounded-xl glass-panel hover-glow"
      >
        <Avatar name={user?.name} />

        <span className="hidden sm:block text-sm text-white/80 group-hover:text-white transition">
          {user?.name || "User"}
        </span>

        <ChevronDown
          size={16}
          className={`text-white/50 transition-transform duration-300 ${
            open ? "rotate-180 text-cyan-300" : ""
          }`}
        />
      </button>

      {/* Dropdown */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -12, scale: 0.94 }}
            animate={{ opacity: 1, y: 10, scale: 1 }}
            exit={{ opacity: 0, y: -12, scale: 0.94 }}
            transition={{ duration: 0.22, ease: "easeOut" }}
            className="absolute right-0 mt-3 w-60 z-50"
          >
            <GlassPanel className="relative overflow-hidden rounded-2xl">
              {/* Glow Border */}
              <div className="pointer-events-none absolute inset-0 rounded-2xl p-[1px] bg-gradient-to-br from-cyan-400/40 via-purple-500/30 to-blue-400/40 blur-[1px] opacity-80" />

              <div className="relative">
                <MenuHeader user={user} />

                <div className="flex flex-col py-1">
                  <MenuItem icon={<User size={16} />} label="Profile" />
                  <MenuItem icon={<Settings size={16} />} label="Settings" />

                  <div className="px-3 py-1">
                    <NeonDivider />
                  </div>

                  <MenuItem
                    icon={<LogOut size={16} />}
                    label="Logout"
                    onClick={onLogout}
                    danger
                  />
                </div>
              </div>
            </GlassPanel>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

/* ========================
   Subcomponents
======================== */

function Avatar({ name }) {
  return (
    <div className="relative w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400 to-purple-500 flex items-center justify-center text-black font-bold shadow-[0_0_10px_rgba(0,255,255,0.6)]">
      {name?.[0] || "U"}
      <div className="absolute inset-0 rounded-full border border-cyan-400/40 blur-[2px]" />
    </div>
  );
}

function MenuHeader({ user }) {
  return (
    <div className="px-4 py-3 border-b border-white/10">
      <p className="text-white text-sm font-medium tracking-wide">
        {user?.name || "Guest User"}
      </p>
      <p className="text-xs text-cyan-300/70">
        {user?.email || "no-email@example.com"}
      </p>
    </div>
  );
}

function MenuItem({ icon, label, onClick, danger = false }) {
  return (
    <button
      onClick={onClick}
      className={`group relative flex items-center gap-3 px-4 py-2.5 text-sm overflow-hidden transition-all duration-200 ${
        danger
          ? "text-red-400 hover:text-red-300"
          : "text-white/70 hover:text-white"
      }`}
    >
      <span className="absolute inset-0 opacity-0 group-hover:opacity-100 transition duration-300 bg-gradient-to-r from-cyan-500/10 via-transparent to-purple-500/10" />

      <span className="relative opacity-70 group-hover:opacity-100 transition">
        {icon}
      </span>

      <span className="relative">{label}</span>
    </button>
  );
}
