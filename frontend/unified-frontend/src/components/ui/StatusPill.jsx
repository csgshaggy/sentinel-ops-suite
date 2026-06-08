export default function StatusPill({ text = "Secure Session" }) {
  return (
    <div className="flex items-center gap-2 text-xs text-cyan-300/80 glass-panel px-2.5 py-1 rounded-md">
      
      {/* Status Dot */}
      <span className="w-2 h-2 rounded-full bg-cyan-400 shadow-[0_0_8px_rgba(0,255,255,0.8)] animate-pulse" />

      {/* Label */}
      <span className="tracking-wide">{text}</span>
    </div>
  );
}
