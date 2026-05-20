// /src/pages/admin/DashboardPage.jsx

import DashboardGrid from "../../components/DashboardGrid.jsx";
import Panel from "../../components/Panel.jsx";

import BackendHeartbeatWidget from "../../components/widgets/BackendHeartbeatWidget.jsx";
import EnvironmentStatusWidget from "../../components/widgets/EnvironmentStatusWidget.jsx";
import SandboxLogWidget from "../../components/widgets/SandboxLogWidget.jsx";
import PluginRegistryWidget from "../../components/widgets/PluginRegistryWidget.jsx";

export default function DashboardPage() {
  return (
    
      <DashboardGrid>
        <Panel title="Backend Heartbeat">
          <BackendHeartbeatWidget />
        </Panel>

        <Panel title="Environment Status">
          <EnvironmentStatusWidget />
        </Panel>

        <Panel title="Sandbox Logs">
          <SandboxLogWidget />
        </Panel>

        <Panel title="Plugin Registry">
          <PluginRegistryWidget />
        </Panel>
      </DashboardGrid>
    
  );
}
