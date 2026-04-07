// ============================================
// TextInput.variants.js
// Path: frontend/src/ui-kit/components/TextInput/TextInput.variants.js
// Variant mapping for TextInput
// ============================================

export const TEXTINPUT_VARIANTS = {
  default: "",
  success: "textinput-variant-success",
  warning: "textinput-variant-warning",
  error: "textinput-variant-error",
  secure: "textinput-variant-secure",
};

export function getTextInputVariantClass(variant) {
  if (!variant) return "";
  return TEXTINPUT_VARIANTS[variant] || "";
}

// Example integration (for reference only):
// import { getTextInputVariantClass } from "./TextInput.variants";
//
// <div
//   className={`textinput-wrapper ${getTextInputVariantClass(variant)} ${
//     disabled ? "disabled" : ""
//   }`}
// >
//   ...
// </div>
