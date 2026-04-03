// frontend/src/routes/AppRoutes.tsx

import { Routes, Route } from "react-router-dom";

// Auth
import Login from "../pages/Login";
import LoginPage from "../pages/LoginPage";

// Dashboard home
import DashboardHome from "../pages/DashboardHome";

// Dashboard pages (newly generated)
import CISummary from "../pages/CISummary";
import GitSnapshots from "../pages/GitSnapshots";
import WorkflowRuns from "../pages/WorkflowRuns";
import RepoHealth from "../pages/RepoHealth";
import RouterDrift from "../pages/RouterDrift";
import MakefileHealth from "../pages/MakefileHealth";

// MFA pages
import MfaChallenge from "../pages/settings/MfaChallenge";
import MfaEnrollment from "../pages/settings/MfaEnrollment";
import MfaSettings from "../pages/settings/MfaSettings";

// Auth gate
import ProtectedRoute from "../components/ProtectedRoute";

export default function AppRoutes() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<Login />} />
      <Route path="/login-page" element={<LoginPage />} />

      {/* Protected dashboard routes */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <DashboardHome />
          </ProtectedRoute>
        }
      />

      <Route
        path="/ci-summary"
        element={
          <ProtectedRoute>
            <CISummary />
          </ProtectedRoute>
        }
      />

      <Route
        path="/git-snapshots"
        element={
          <ProtectedRoute>
            <GitSnapshots />
          </ProtectedRoute>
        }
      />

      <Route
        path="/workflow-runs"
        element={
          <ProtectedRoute>
            <WorkflowRuns />
          </ProtectedRoute>
        }
      />

      <Route
        path="/repo-health"
        element={
          <ProtectedRoute>
            <RepoHealth />
          </ProtectedRoute>
        }
      />

      <Route
        path="/router-drift"
        element={
          <ProtectedRoute>
            <RouterDrift />
          </ProtectedRoute>
        }
      />

      <Route
        path="/makefile-health"
        element={
          <ProtectedRoute>
            <MakefileHealth />
          </ProtectedRoute>
        }
      />

      {/* MFA routes */}
      <Route
        path="/mfa/challenge"
        element={
          <ProtectedRoute>
            <MfaChallenge />
          </ProtectedRoute>
        }
      />

      <Route
        path="/mfa/enroll"
        element={
          <ProtectedRoute>
            <MfaEnrollment />
          </ProtectedRoute>
        }
      />

      <Route
        path="/mfa/settings"
        element={
          <ProtectedRoute>
            <MfaSettings />
          </ProtectedRoute>
        }
      />

      {/* Fallback */}
      <Route
        path="*"
        element={
          <ProtectedRoute>
            <DashboardHome />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
