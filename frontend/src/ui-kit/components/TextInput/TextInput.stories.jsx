// ============================================
// TextInput.stories.jsx
// Path: frontend/src/ui-kit/components/TextInput/TextInput.stories.jsx
// Storybook stories for TextInput variants
// ============================================

import React, { useState } from "react";
import TextInput from "./TextInput";
import "./TextInput.css";
import "./TextInput.theme.css";
import "./TextInput.variants.css";

export default {
  title: "UI-Kit/TextInput",
  component: TextInput,
  args: {
    label: "Label",
    placeholder: "Type here..."
  }
};

function Template(args) {
  const [value, setValue] = useState("");
  return (
    <div className="operator-panel" style={{ padding: 20, maxWidth: 420 }}>
      <TextInput
        {...args}
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
    </div>
  );
}

export const Default = Template.bind({});
Default.args = {
  variant: "default"
};

export const Success = Template.bind({});
Success.args = {
  variant: "success"
};

export const Warning = Template.bind({});
Warning.args = {
  variant: "warning"
};

export const Secure = Template.bind({});
Secure.args = {
  variant: "secure",
  type: "password"
};

export const Error = Template.bind({});
Error.args = {
  variant: "error",
  error: "Something went wrong"
};

