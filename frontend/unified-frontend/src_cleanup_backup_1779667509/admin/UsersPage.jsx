// /src/pages/UsersPage.jsx

import DashboardGrid from "../../components/DashboardGrid.jsx";
import Panel from "../../components/Panel.jsx";

export default function UsersPage() {
  return (
    
      <DashboardGrid>
        <Panel title="Users">
          <p>No users found.</p>
        </Panel>

        <Panel title="Roles">
          <p>No roles defined.</p>
        </Panel>

        <Panel title="User Sessions">
          <p>No active sessions.</p>
        </Panel>

        <Panel title="User Inspector">
          <p>Select a user to view details.</p>
        </Panel>
      </DashboardGrid>
    
  );
}
