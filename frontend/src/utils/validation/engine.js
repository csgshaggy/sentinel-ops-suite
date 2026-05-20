// frontend/src/utils/validation/engine.js

/**
 * Shared validation engine for all forms.
 * Each rule returns either "" (valid) or a string error message.
 */

export function runValidationRules(value, rules = []) {
  for (const rule of rules) {
    const result = rule(value);
    if (result) return result; // return first error
  }
  return "";
}

/**
 * Rule helpers
 */
export const rules = {
  required: (msg = "This field is required") => (value) =>
    !value || !value.trim() ? msg : "",

  minLength: (len, msg) => (value) =>
    value.length < len ? msg || `Must be at least ${len} characters` : "",

  pattern: (regex, msg) => (value) =>
    !regex.test(value) ? msg : "",

  uppercase: (msg = "Must include an uppercase letter") => (value) =>
    /[A-Z]/.test(value) ? "" : msg,

  lowercase: (msg = "Must include a lowercase letter") => (value) =>
    /[a-z]/.test(value) ? "" : msg,

  number: (msg = "Must include a number") => (value) =>
    /[0-9]/.test(value) ? "" : msg,

  symbol: (msg = "Must include a symbol") => (value) =>
    /[^A-Za-z0-9]/.test(value) ? "" : msg,
};

/**
 * Validate an entire form using a schema object:
 *
 * {
 *   username: [rules.required(), rules.minLength(3)],
 *   password: [rules.required(), rules.uppercase(), ...]
 * }
 */
export function validateFormSchema(form, schema) {
  const errors = {};
  let isValid = true;

  for (const field in schema) {
    const fieldRules = schema[field];
    const value = form[field];

    const error = runValidationRules(value, fieldRules);
    errors[field] = error;

    if (error) isValid = false;
  }

  return { errors, isValid };
}
