interface MfaStatusBadgeProps {
  enabled: boolean;
}

export function MfaStatusBadge({ enabled }: MfaStatusBadgeProps) {
  return (
    <span
      className={`px-2 py-1 rounded text-xs font-semibold ${
        enabled
          ? "bg-green-100 text-green-700"
          : "bg-red-100 text-red-700"
      }`}
    >
      {enabled ? "Enabled" : "Disabled"}
    </span>
  );
}
