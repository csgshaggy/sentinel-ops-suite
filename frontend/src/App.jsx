import { Routes, Route } from "react-router-dom";
import LoginPage from "./pages/Login.jsx";
import UiKitTest from "./pages/UiKitTest.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/ui-kit-test" element={<UiKitTest />} />
    </Routes>
  );
}
