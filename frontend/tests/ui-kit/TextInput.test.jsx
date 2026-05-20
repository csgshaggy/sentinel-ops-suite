// ============================================
// TextInput.test.jsx
// Path: frontend/tests/ui-kit/TextInput.test.jsx
// Tests including variant behavior
// ============================================

import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import TextInput from "../../src/ui-kit/components/TextInput/TextInput";

describe("TextInput Component", () => {
  test("renders label", () => {
    render(<TextInput label="Username" />);
    expect(screen.getByText("Username")).toBeInTheDocument();
  });

  test("renders input element", () => {
    render(<TextInput />);
    expect(screen.getByRole("textbox")).toBeInTheDocument();
  });

  test("fires onChange", () => {
    const fn = jest.fn();
    render(<TextInput onChange={fn} />);
    fireEvent.change(screen.getByRole("textbox"), { target: { value: "abc" } });
    expect(fn).toHaveBeenCalled();
  });

  test("shows error message", () => {
    render(<TextInput error="Required" />);
    expect(screen.getByText("Required")).toBeInTheDocument();
  });

  test("applies disabled state", () => {
    render(<TextInput disabled />);
    expect(screen.getByRole("textbox")).toBeDisabled();
  });

  test("applies success variant class", () => {
    render(<TextInput variant="success" />);
    const wrapper = screen.getByRole("textbox").closest(".textinput-wrapper");
    expect(wrapper).toHaveClass("textinput-variant-success");
  });

  test("applies warning variant class", () => {
    render(<TextInput variant="warning" />);
    const wrapper = screen.getByRole("textbox").closest(".textinput-wrapper");
    expect(wrapper).toHaveClass("textinput-variant-warning");
  });

  test("applies secure variant class", () => {
    render(<TextInput variant="secure" />);
    const wrapper = screen.getByRole("textbox").closest(".textinput-wrapper");
    expect(wrapper).toHaveClass("textinput-variant-secure");
  });

  test("applies error variant class", () => {
    render(<TextInput variant="error" />);
    const wrapper = screen.getByRole("textbox").closest(".textinput-wrapper");
    expect(wrapper).toHaveClass("textinput-variant-error");
  });
});
