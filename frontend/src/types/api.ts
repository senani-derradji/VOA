// TypeScript types for API requests and responses

export interface ApiError {
  message: string;
  status?: number;
  code?: string;
  details?: any;
}

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

// Auth types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

// User types
export interface User {
  id: number;
  username: string;
  role: 'admin' | 'developer' | 'viewer';
  created_at?: string;
}

export interface RegisterUserRequest {
  username: string;
  password: string;
  role?: 'admin' | 'developer' | 'viewer';
}

export interface UpdateUserRequest {
  role: 'admin' | 'developer' | 'viewer';
}

// Secret types
export interface Secret {
  id: number;
  name: string;
  value: string;
  env: 'development' | 'staging' | 'production';
  owner_id: number;
  created_at?: string;
  updated_at?: string;
}

export interface CreateSecretRequest {
  name: string;
  value: string;
  env: 'development' | 'staging' | 'production';
}

export interface UpdateSecretRequest {
  name?: string;
  value?: string;
  env?: 'development' | 'staging' | 'production';
}

// Health check
export interface HealthResponse {
  status: string;
  version?: string;
  timestamp?: string;
}
