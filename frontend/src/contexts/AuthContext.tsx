import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  getAuthHeader: () => { Authorization: string } | {};
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const TOKEN_KEY = 'ppt_auth_token';
const USER_KEY = 'ppt_user';

const API_BASE = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for stored auth on mount
    const storedToken = localStorage.getItem(TOKEN_KEY);
    const storedUser = localStorage.getItem(USER_KEY);
    
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string): Promise<void> => {
    if (!email || !password) {
      throw new Error('Please enter email and password');
    }

    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error((data && (data.detail || data.message)) || 'Login failed');
    }

    const access = data.access_token || data.accessToken || data.token;
    if (!access) throw new Error('No access token returned from server');

    // Try to parse JWT to extract user id (sub) if available
    let userId = '';
    try {
      const payload = access.split('.')[1];
      const decoded = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
      userId = decoded.sub || '';
    } catch (e) {
      userId = '';
    }

    const loggedUser: User = { id: userId || '', email, name: email.split('@')[0] };

    localStorage.setItem(TOKEN_KEY, access);
    localStorage.setItem(USER_KEY, JSON.stringify(loggedUser));

    setToken(access);
    setUser(loggedUser);
  };

  const register = async (name: string, email: string, password: string): Promise<void> => {
    if (!name || !email || !password) {
      throw new Error('Please fill in all fields');
    }

    const res = await fetch(`${API_BASE}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password }),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error((data && (data.detail || data.message)) || 'Signup failed');
    }

    const access = data.access_token || data.accessToken || data.token;
    if (!access) throw new Error('No access token returned from server');

    let userId = '';
    try {
      const payload = access.split('.')[1];
      const decoded = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
      userId = decoded.sub || '';
    } catch (e) {
      userId = '';
    }

    const newUser: User = { id: userId || '', email, name };

    localStorage.setItem(TOKEN_KEY, access);
    localStorage.setItem(USER_KEY, JSON.stringify(newUser));

    setToken(access);
    setUser(newUser);
  };

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    setToken(null);
    setUser(null);
  };

  const getAuthHeader = () => {
    if (token) {
      return { Authorization: `Bearer ${token}` };
    }
    return {};
  };

  return (
    <AuthContext.Provider value={{ user, token, isLoading, login, register, logout, getAuthHeader }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
