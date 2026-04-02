import React from "react";
import { Route,Routes } from "react-router-dom";

import MfaChallenge from "./MfaChallenge";
import MfaEnrollment from "./MfaEnrollment";
import MfaSettings from "./MfaSettings";

export default function MfaRouter() {
  return (
    <Routes>
      <Route path="/" element={<MfaSettings />} />
      <Route path="/enroll" element={<MfaEnrollment />} />
      <Route path="/challenge" element={<MfaChallenge />} />
    </Routes>
  );
}
