// /src/pages/admin/SecurityPage.jsx

import DashboardGrid from "../../components/DashboardGrid.jsx";
import Panel from "../../components/Panel.jsx";

import MFAStatusWidget from "../../components/widgets/security/MFAStatusWidget.jsx";
import ActiveSessionWidget from "../../components/widgets/security/ActiveSessionWidget.jsx";
import RBACOverviewWidget from "../../components/widgets/security/RBACOverviewWidget.jsx";
import AuthEventStreamWidget from "../../components/widgets/security/AuthEventStreamWidget.jsx";

export default function SecurityPage() {
  return (
    
      <DashboardGrid>
        <Panel title="MFA Status">
          <MFAStatusWidget />
        </Panel>

        <Panel title="Active Sessions">
          <ActiveSessionWidget />
        </Panel>

        <Panel title="RBAC Overview">
          <RBACOverviewWidget />
        </Panel>

        <Panel title="Authentication Events">
          <AuthEventStreamWidget />
        </Panel>
      </DashboardGrid>
    
  );
}
