import React from "react";

export interface PluginDetail {
  id: string;
  name: string;
  description?: string;
  lastRunAt: string | null;
}

interface DetailDrawerProps {
  open: boolean;
  plugin: PluginDetail | null;
  onClose: () => void;
}

const DetailDrawer: React.FC<DetailDrawerProps> = ({ open, plugin, onClose }) => {
  if (!open || !plugin) return null;

  return (
    <div className="detail-drawer">
      <button onClick={onClose}>Close</button>
      <h2>{plugin.name}</h2>
      {plugin.description && <p>{plugin.description}</p>}
      <p>
        <strong>Last Run:</strong>{" "}
        {plugin.lastRunAt ? new Date(plugin.lastRunAt).toLocaleString() : "Never"}
      </p>
    </div>
  );
};

export default DetailDrawer;
