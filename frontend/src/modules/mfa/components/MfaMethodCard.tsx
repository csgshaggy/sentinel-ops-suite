interface MfaMethodCardProps {
  title: string;
  description: string;
  enabled: boolean;
  onManage: () => void;
}

export function MfaMethodCard({
  title,
  description,
  enabled,
  onManage,
}: MfaMethodCardProps) {
  return (
    <div className="border rounded p-4 flex justify-between items-center">
      <div>
        <h3 className="font-semibold">{title}</h3>
        <p className="text-sm text-gray-600">{description}</p>
      </div>

      <button
        onClick={onManage}
        className="bg-blue-600 text-white px-3 py-1 rounded"
      >
        {enabled ? "Manage" : "Enable"}
      </button>
    </div>
  );
}
