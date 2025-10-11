// Base API Service
// Provides centralized HTTP client with error handling and interceptors

import { API_CONFIG } from '../config/api';
import { ApiError } from '../types/api';

export class ApiService {
  private static getAuthToken(): string | null {
    return localStorage.getItem('voa_access_token');
  }

  private static getRefreshToken(): string | null {
    return localStorage.getItem('voa_refresh_token');
  }

  private static async refreshAccessToken(): Promise<string | null> {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) return null;

    try {
      const response = await fetch(`${API_CONFIG.baseURL}${API_CONFIG.apiPrefix}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('voa_access_token', data.access_token);
        return data.access_token;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
    }

    return null;
  }

  private static async handleResponse<T>(response: Response): Promise<T> {
    // Handle different status codes
    if (response.status === 204) {
      return {} as T; // No content
    }

    const contentType = response.headers.get('content-type');
    const isJson = contentType?.includes('application/json');

    if (!response.ok) {
      let errorMessage = `HTTP Error ${response.status}: ${response.statusText}`;
      let errorDetails: any = null;

      if (isJson) {
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorData.message || errorMessage;
          errorDetails = errorData;
        } catch (e) {
          // JSON parsing failed, use default message
        }
      }

      const error: ApiError = {
        message: errorMessage,
        status: response.status,
        details: errorDetails,
      };

      // Handle specific error codes
      if (response.status === 401) {
        error.code = 'UNAUTHORIZED';
        // Try to refresh token
        const newToken = await this.refreshAccessToken();
        if (newToken) {
          error.code = 'TOKEN_REFRESHED';
        } else {
          // Clear auth and redirect to login
          localStorage.removeItem('voa_access_token');
          localStorage.removeItem('voa_refresh_token');
          localStorage.removeItem('voa_user');
          window.location.href = '/';
        }
      } else if (response.status === 403) {
        error.code = 'FORBIDDEN';
      } else if (response.status === 404) {
        error.code = 'NOT_FOUND';
      } else if (response.status === 429) {
        error.code = 'RATE_LIMIT';
        error.message = 'Too many requests. Please try again later.';
      } else if (response.status >= 500) {
        error.code = 'SERVER_ERROR';
        error.message = 'Server error. Please try again later.';
      }

      throw error;
    }

    if (isJson) {
      return response.json();
    }

    return response.text() as any;
  }

  private static async executeRequest<T>(
    url: string,
    options: RequestInit,
    retry = 0
  ): Promise<T> {
    try {
      const response = await fetch(url, {
        ...options,
        signal: AbortSignal.timeout(API_CONFIG.timeout),
      });

      return await this.handleResponse<T>(response);
    } catch (error: any) {
      // Handle network errors and retries
      if (error.name === 'AbortError' || error.name === 'TimeoutError') {
        throw {
          message: 'Request timeout. Please check your connection.',
          code: 'TIMEOUT',
        } as ApiError;
      }

      // Retry on network errors
      if (retry < API_CONFIG.retry.maxRetries && !error.status) {
        await new Promise(resolve => 
          setTimeout(resolve, API_CONFIG.retry.retryDelay * (retry + 1))
        );
        return this.executeRequest<T>(url, options, retry + 1);
      }

      if (error.message && error.status !== undefined) {
        throw error; // Already an ApiError
      }

      throw {
        message: error.message || 'Network error. Please check your connection.',
        code: 'NETWORK_ERROR',
      } as ApiError;
    }
  }

  static async get<T>(url: string, requiresAuth = true): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (requiresAuth) {
      const token = this.getAuthToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    return this.executeRequest<T>(url, {
      method: 'GET',
      headers,
    });
  }

  static async post<T>(
    url: string,
    data?: any,
    requiresAuth = true
  ): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (requiresAuth) {
      const token = this.getAuthToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    return this.executeRequest<T>(url, {
      method: 'POST',
      headers,
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  static async put<T>(
    url: string,
    data?: any,
    requiresAuth = true
  ): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (requiresAuth) {
      const token = this.getAuthToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    return this.executeRequest<T>(url, {
      method: 'PUT',
      headers,
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  static async delete<T>(url: string, requiresAuth = true): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (requiresAuth) {
      const token = this.getAuthToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    return this.executeRequest<T>(url, {
      method: 'DELETE',
      headers,
    });
  }

  // Special method for form data (OAuth2 password flow)
  static async postForm<T>(url: string, data: Record<string, string>): Promise<T> {
    const formData = new URLSearchParams();
    Object.entries(data).forEach(([key, value]) => {
      formData.append(key, value);
    });

    return this.executeRequest<T>(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData.toString(),
    });
  }
}
