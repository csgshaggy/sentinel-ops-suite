import axios from './api.js';

export type UserPreferences = {
  theme: string;
  accent_color?: string;
  layout_density?: string;
};

export async function getUserPreferences(): Promise<UserPreferences> {
  const { data } = await axios.get('/api/v1/user/preferences');
  return data;
}

export async function updateUserPreferences(prefs: Partial<UserPreferences>) {
  const { data } = await axios.put('/api/v1/user/preferences', prefs);
  return data;
}
