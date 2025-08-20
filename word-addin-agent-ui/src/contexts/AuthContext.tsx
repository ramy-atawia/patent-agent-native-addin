import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Auth0Client, User } from '@auth0/auth0-spa-js';
import { setAuthTokens, getAccessToken, getUserProfile, clearAuthTokens } from '../services/authTokenStore';

interface AuthContextType {
  isAuthenticated: boolean;
  token: string | null;
  user: User | null;
  loginWithRedirect: () => Promise<void>;
  handleRedirectCallback: () => Promise<void>;
  logout: () => void;
  loading: boolean;
  refreshFromStorage: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [auth0Client, setAuth0Client] = useState<Auth0Client | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Listen to global auth-tokens event dispatched by dialog/popup
    const onAuthTokens = (e: Event) => {
      try {
        // @ts-ignore
        const detail = (e as CustomEvent).detail || {};
        setAuthTokens({ accessToken: detail.accessToken || null, idToken: detail.idToken || null, userProfile: detail.userProfile || null });
        refreshFromStorage();
      } catch (err) {
        console.warn('Failed to process auth-tokens event', err);
      }
    };
    window.addEventListener('auth-tokens', onAuthTokens as EventListener);
    let mounted = true;
    const initAuth = async () => {
      try {
        const config = (window as any).__AUTH0_CONFIG__ || {};

        // Use in-memory token store instead of sessionStorage (artifacts environment cannot use browser storage)
        const storedAccess = getAccessToken();
        const storedProfile = getUserProfile();
        if (storedAccess) {
          if (!mounted) return;
          setToken(storedAccess);
          try { setUser(storedProfile || null); } catch (e) { setUser(null); }
      setIsAuthenticated(true);
          setLoading(false);
          return;
        }

        // No stored tokens: initialize Auth0 SPA client to support silent flows
        const domain = config.domain || 'dev-bktskx5kbc655wcl.us.auth0.com';
        const clientId = config.clientId || 'INws849yDXaC6MZVXnLhMJi6CZC4nx6U';
        const redirectUri = config.redirectUri || (window.location.origin + '/auth-callback.html');
        const scope = config.scope || 'openid profile email';

        // No SPA fallback — rely solely on dialog flow and sessionStorage tokens (exact myword behaviour)
        if (!mounted) return;
        setAuth0Client(null);
        setIsAuthenticated(false);
      } catch (e) {
        console.error('Auth initialization failed', e);
      } finally {
    setLoading(false);
      }
    };
    initAuth();
    return () => {
      mounted = false;
      try { window.removeEventListener('auth-tokens', onAuthTokens as EventListener); } catch (e) {}
    };
  }, []);

  const loginWithRedirect = async () => {
    if (!auth0Client) throw new Error('Auth0 client not initialized');
    await auth0Client.loginWithRedirect();
  };

  const handleRedirectCallback = async () => {
    if (!auth0Client) throw new Error('Auth0 client not initialized');
    setLoading(true);
    try {
      await auth0Client.handleRedirectCallback();
      const silentToken = await auth0Client.getTokenSilently();
      setToken(silentToken);
      const profile = await auth0Client.getUser();
      setUser(profile || null);
    setIsAuthenticated(true);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    if (auth0Client) {
      auth0Client.logout({ logoutParams: { returnTo: window.location.origin } });
    }
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
  };

  // Refresh auth state from in-memory store
  const refreshFromStorage = () => {
    const storedAccess = getAccessToken();
    const storedProfile = getUserProfile();
    if (storedAccess) {
      setToken(storedAccess);
      try { setUser(storedProfile || null); } catch (e) { setUser(null); }
      setIsAuthenticated(true);
    }
  };

  const value: AuthContextType = {
    isAuthenticated,
    token,
    user,
    loginWithRedirect,
    handleRedirectCallback,
    logout,
    loading,
    refreshFromStorage,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
