// Simple in-memory auth token store to avoid using browser storage in artifact environments
let accessToken: string | null = null;
let idToken: string | null = null;
let userProfile: any = null;

export function setAuthTokens(tokens: { accessToken?: string | null; idToken?: string | null; userProfile?: any | null }) {
  accessToken = tokens.accessToken || null;
  idToken = tokens.idToken || null;
  userProfile = tokens.userProfile || null;
}

export function getAccessToken() {
  return accessToken;
}

export function getIdToken() {
  return idToken;
}

export function getUserProfile() {
  return userProfile;
}

export function clearAuthTokens() {
  accessToken = null;
  idToken = null;
  userProfile = null;
}
