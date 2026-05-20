// File: /home/ubuntu/sentinel-ops-suite/frontend/src/ui-kit/components/TextInput/TextInput.stories.jsx
// Storybook Stories for TextInput Component

import React, { useState } from "react";
import TextInput from "./TextInput.jsx";
import variants from "./TextInput.variants.js";

export default {
  title: "UI-Kit/TextInput",
  component: TextInput,
  argTypes: {
    variant: {
      control: "select",
      options: Object.keys(variants),
    },
  },
};

const Template = (args) => {
  const [value, setValue] = useState("");

  return (
    <TextInput
      {...args}
      value={value}
      onChange={(e) => setValue(e.target.value)}
    />
  );
};

export const Default = Template.bind({});
Default.args = {
  label: "Default Input",
  placeholder: "Type here...",
  variant: "default",
};

export const Ghost = Template.bind({});
Ghost.args = {
  label: "Ghost Variant",
  placeholder: "Ghost input",
  variant: "ghost",
};

export const Solid = Template.bind({});
Solid.args = {
  label: "Solid Variant",
  placeholder: "Solid input",
  variant: "solid",
};

export const Underline = Template.bind({});
Underline.args = {
  label: "Underline Variant",
  placeholder: "Underline input",
  variant: "underline",
};

export const Compact = Template.bind({});
Compact.args = {
  label: "Compact Variant",
  placeholder: "Compact input",
  variant: "compact",
};

export const WithError = Template.bind({});
WithError.args = {
  label: "With Error",
  placeholder: "Triggers error",
  error: "Example error message",
  variant: "default",
};
