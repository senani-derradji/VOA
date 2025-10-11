import React, { createContext, useContext, useState, useEffect } from 'react';
import { AuthService } from '../services/auth-service';
import { User } from '../types/api';

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for stored auth on mount
    const storedUser = localStorage.getItem('voa_user');
    const storedToken = localStorage.getItem('voa_access_token');
    
    if (storedUser && storedToken) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (error) {
        console.error('Failed to parse stored user:', error);
        localStorage.removeItem('voa_user');
      }
    }
    
    setIsLoading(false);
  }, []);

  const login = async (username: string, password: string) => {
    try {
      // Call real API to get tokens
      const tokens = await AuthService.login({ username, password });
      
      // Store tokens temporarily
      localStorage.setItem('voa_access_token', tokens.access_token);
      if (tokens.refresh_token) {
        localStorage.setItem('voa_refresh_token', tokens.refresh_token);
      }
      
      // Try to get full user info from backend
      let userInfo: User;
      try {
        // Attempt to fetch full user data from /users/me endpoint
        userInfo = await AuthService.getCurrentUser();
      } catch (error) {
        // Fallback to decoding token if /users/me endpoint doesn't exist
        console.warn('Could not fetch user from /users/me, falling back to token decode');
        const userFromToken = AuthService.getCurrentUserFromToken();
        if (!userFromToken) {
          throw new Error('Failed to get user information');
        }
        userInfo = userFromToken;
      }
      
      // Store user info and update state
      localStorage.setItem('voa_user', JSON.stringify(userInfo));
      setUser(userInfo);
      
    } catch (error: any) {
      // Clean up on error
      localStorage.removeItem('voa_access_token');
      localStorage.removeItem('voa_refresh_token');
      localStorage.removeItem('voa_user');
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await AuthService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user, isLoading }}>
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
