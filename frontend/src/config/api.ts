// API Configuration
// Manages base URLs and endpoints for different environments

// Safely access environment variables
const getEnvVar = (key: string, defaultValue: string): string => {
  try {
    return import.meta?.env?.[key] || defaultValue;
  } catch {
    return defaultValue;
  }
};

export const API_CONFIG = {
  // Base URL - reads from environment variable or defaults to localhost
  baseURL: getEnvVar('VITE_API_BASE_URL', 'http://localhost:8000'),
  
  // API version prefix
  apiPrefix: '/api/v1',
  
  // Request timeout in milliseconds
  timeout: 30000,
  
  // Retry configuration
  retry: {
    maxRetries: 3,
    retryDelay: 1000,
  },
};

// API Endpoints
export const API_ENDPOINTS = {
  // Health
  health: '/health',
  
  // Authentication
  auth: {
    login: '/auth/login',
    refresh: '/auth/refresh',
    logout: '/auth/logout',
  },
  
  // Users
  users: {
    register: '/users/register',
    list: '/users/',
    get: (id: number) => `/users/${id}`,
    update: (id: number) => `/users/${id}`,
    delete: (id: number) => `/users/${id}`,
    me: '/users/me',
  },
  
  // Secrets
  secrets: {
    create: '/secrets/create',
    list: '/secrets/',
    get: (id: number) => `/secrets/${id}`,
    update: (id: number) => `/secrets/${id}`,
    delete: (id: number) => `/secrets/${id}`,
  },
};

// Build full URL
export function buildUrl(endpoint: string): string {
  return `${API_CONFIG.baseURL}${API_CONFIG.apiPrefix}${endpoint}`;
}

// Build full URL without API prefix (for health checks)
export function buildRootUrl(endpoint: string): string {
  return `${API_CONFIG.baseURL}${endpoint}`;
}
