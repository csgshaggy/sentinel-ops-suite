// /src/pages/admin/AuditLogsPage.jsx

import DashboardGrid from "../../components/DashboardGrid.jsx";
import Panel from "../../components/Panel.jsx";

export default function AuditLogsPage() {
  return (
    
      <DashboardGrid>
        <Panel title="Audit Log Stream">
          <p>No audit events available.</p>
        </Panel>

        <Panel title="Filters">
          <p>No filters applied.</p>
        </Panel>

        <Panel title="Event Inspector">
          <p>Select an event to view details.</p>
        </Panel>
      </DashboardGrid>
    
  );
}
