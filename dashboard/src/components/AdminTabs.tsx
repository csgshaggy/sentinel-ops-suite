// =====================================================================
// SSRF Command Console — AdminTabs
// Reusable tabbed navigation for admin pages
// =====================================================================

import { ReactNode, useState } from "react";

export type TabConfig = {
  id: string;
  label: string;
  content: ReactNode;
};

type Props = {
  tabs: TabConfig[];
  defaultTabId?: string;
};

export default function AdminTabs({ tabs, defaultTabId }: Props) {
  const [activeId, setActiveId] = useState(
    defaultTabId ?? (tabs[0] ? tabs[0].id : "")
  );

  const activeTab = tabs.find((t) => t.id === activeId);

  return (
    <div className="admin-tabs">
      <div className="admin-tabs-header">
        {tabs.map((t) => (
          <button
            key={t.id}
            className={t.id === activeId ? "active" : ""}
            onClick={() => setActiveId(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="admin-tabs-body">
        {activeTab?.content}
      </div>
    </div>
  );
}
