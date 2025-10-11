// Users Service
// Handles all user management API calls

import { ApiService } from './api';
import { buildUrl } from '../config/api';
import { API_ENDPOINTS } from '../config/api';
import { User, RegisterUserRequest, UpdateUserRequest } from '../types/api';

export class UsersService {
  /**
   * Register a new user (Admin only)
   * POST /api/v1/users/register
   * Note: Backend expects query parameters, not JSON body
   */
  static async register(data: RegisterUserRequest): Promise<User> {
    const url = buildUrl(API_ENDPOINTS.users.register);
    // Backend expects query parameters
    const urlWithParams = `${url}?username=${encodeURIComponent(data.username)}&password=${encodeURIComponent(data.password)}&role=${encodeURIComponent(data.role || 'viewer')}`;
    return ApiService.post<User>(urlWithParams);
  }

  /**
   * Get all users (Admin only)
   * GET /api/v1/users/
   */
  static async list(): Promise<User[]> {
    const url = buildUrl(API_ENDPOINTS.users.list);
    return ApiService.get<User[]>(url);
  }

  /**
   * Get specific user by ID
   * GET /api/v1/users/{user_id}
   */
  static async get(id: number): Promise<User> {
    const url = buildUrl(API_ENDPOINTS.users.get(id));
    return ApiService.get<User>(url);
  }

  /**
   * Get current user profile
   * GET /api/v1/users/me
   */
  static async me(): Promise<User> {
    const url = buildUrl(API_ENDPOINTS.users.me);
    return ApiService.get<User>(url);
  }

  /**
   * Update user role
   * PUT /api/v1/users/{user_id}
   * Note: Backend expects query parameter for role
   */
  static async update(id: number, data: UpdateUserRequest): Promise<User> {
    const url = buildUrl(API_ENDPOINTS.users.update(id));
    // Backend expects query parameter
    const urlWithParams = `${url}?new_role=${encodeURIComponent(data.role)}`;
    return ApiService.put<User>(urlWithParams);
  }

  /**
   * Delete user
   * DELETE /api/v1/users/{user_id}
   */
  static async delete(id: number): Promise<void> {
    const url = buildUrl(API_ENDPOINTS.users.delete(id));
    return ApiService.delete<void>(url);
  }
}
