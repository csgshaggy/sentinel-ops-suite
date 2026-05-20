export function validateUsername(username) {
  if (!username.trim()) return "Username is required";
  return "";
}

export function validatePassword(password) {
  if (!password.trim()) return "Password is required";
  return "";
}

export function validateLoginForm({ username, password }) {
  const errors = {
    username: validateUsername(username),
    password: validatePassword(password),
  };

  return {
    ...errors,
    isValid: !errors.username && !errors.password,
  };
}
