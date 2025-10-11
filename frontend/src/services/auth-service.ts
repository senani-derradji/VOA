// Authentication Service
// Handles all authentication-related API calls

import { ApiService } from './api';
import { buildUrl } from '../config/api';
import { API_ENDPOINTS } from '../config/api';
import { LoginRequest, LoginResponse, User } from '../types/api';

export class AuthService {
  /**
   * Login user with username and password
   * POST /api/v1/auth/login
   * 
   * Note: FastAPI OAuth2 typically uses form data with 'username' and 'password' fields
   */
  static async login(credentials: LoginRequest): Promise<LoginResponse> {
    const url = buildUrl(API_ENDPOINTS.auth.login);
    
    // OAuth2PasswordRequestForm expects form data
    return ApiService.postForm<LoginResponse>(url, {
      username: credentials.username,
      password: credentials.password,
    });
  }

  /**
   * Refresh access token
   * POST /api/v1/auth/refresh
   */
  static async refreshToken(refreshToken: string): Promise<LoginResponse> {
    const url = buildUrl(API_ENDPOINTS.auth.refresh);
    
    return ApiService.post<LoginResponse>(url, {
      refresh_token: refreshToken,
    }, false); // Don't require auth for refresh
  }

  /**
   * Logout user (optional - usually just clears local storage)
   * POST /api/v1/auth/logout
   */
  static async logout(): Promise<void> {
    try {
      const url = buildUrl(API_ENDPOINTS.auth.logout);
      await ApiService.post<void>(url);
    } catch (error) {
      // Logout anyway even if API call fails
      console.error('Logout API call failed:', error);
    } finally {
      // Clear local storage
      localStorage.removeItem('voa_access_token');
      localStorage.removeItem('voa_refresh_token');
      localStorage.removeItem('voa_user');
    }
  }

  /**
   * Get current user info from token
   * FastAPI token structure: {"sub": username, "role": role}
   */
  static getCurrentUserFromToken(): User | null {
    const token = localStorage.getItem('voa_access_token');
    if (!token) return null;

    try {
      // Decode JWT token (basic implementation)
      const payload = token.split('.')[1];
      const decoded = JSON.parse(atob(payload));
      
      // Extract user info from token
      // FastAPI structure: sub = username, role = role
      const username = decoded.sub;
      const role = decoded.role || 'viewer';
      
      if (!username) {
        throw new Error('Username not found in token');
      }
      
      // Generate a temporary ID from username hash
      // In production, you should fetch full user info from /users/me endpoint
      const tempId = Math.abs(username.split('').reduce((a: number, b: string) => {
        a = ((a << 5) - a) + b.charCodeAt(0);
        return a & a;
      }, 0));
      
      return {
        id: tempId,
        username: username,
        role: role as 'admin' | 'developer' | 'viewer',
      };
    } catch (error) {
      console.error('Failed to decode token:', error);
      return null;
    }
  }

  /**
   * Get full user info from backend
   * Fetches complete user data from /users/me endpoint
   */
  static async getCurrentUser(): Promise<User> {
    const url = buildUrl(API_ENDPOINTS.users.me);
    return ApiService.get<User>(url);
  }

  /**
   * Store authentication tokens
   */
  static storeTokens(tokens: LoginResponse, user: User): void {
    localStorage.setItem('voa_access_token', tokens.access_token);
    if (tokens.refresh_token) {
      localStorage.setItem('voa_refresh_token', tokens.refresh_token);
    }
    localStorage.setItem('voa_user', JSON.stringify(user));
  }

  /**
   * Check if user is authenticated
   */
  static isAuthenticated(): boolean {
    return !!localStorage.getItem('voa_access_token');
  }
}
