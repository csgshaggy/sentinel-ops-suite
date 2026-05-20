import { render, screen } from "@testing-library/react";
import App from "../App";

test("renders application root", () => {
  render(<App />);
  const root = screen.getByTestId("app-root");
  expect(root).toBeInTheDocument();
});
