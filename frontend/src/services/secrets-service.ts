// Secrets Service
// Handles all secrets management API calls

import { ApiService } from './api';
import { buildUrl } from '../config/api';
import { API_ENDPOINTS } from '../config/api';
import { Secret, CreateSecretRequest, UpdateSecretRequest } from '../types/api';

export class SecretsService {
  /**
   * Create a new secret
   * POST /api/v1/secrets/create
   * Note: Backend expects query parameters, not JSON body
   */
  static async create(data: CreateSecretRequest): Promise<Secret> {
    const url = buildUrl(API_ENDPOINTS.secrets.create);
    // Backend expects query parameters
    const urlWithParams = `${url}?name=${encodeURIComponent(data.name)}&value=${encodeURIComponent(data.value)}&env=${encodeURIComponent(data.env)}`;
    return ApiService.post<Secret>(urlWithParams);
  }

  /**
   * Get all secrets visible to the user
   * GET /api/v1/secrets/
   */
  static async list(): Promise<Secret[]> {
    const url = buildUrl(API_ENDPOINTS.secrets.list);
    return ApiService.get<Secret[]>(url);
  }

  /**
   * Get specific secret by ID (decrypts value)
   * GET /api/v1/secrets/{secret_id}
   */
  static async get(id: number): Promise<Secret> {
    const url = buildUrl(API_ENDPOINTS.secrets.get(id));
    return ApiService.get<Secret>(url);
  }

  /**
   * Update a secret
   * PUT /api/v1/secrets/{secret_id}
   * Note: Backend expects JSON body with Pydantic model
   */
  static async update(id: number, data: UpdateSecretRequest): Promise<Secret> {
    const url = buildUrl(API_ENDPOINTS.secrets.update(id));
    // Map frontend field names to backend field names
    const backendData = {
      name: data.name,
      value: data.value,
      environment: data.env,  // Backend uses 'environment' instead of 'env'
    };
    return ApiService.put<Secret>(url, backendData);
  }

  /**
   * Delete a secret
   * DELETE /api/v1/secrets/{secret_id}
   */
  static async delete(id: number): Promise<void> {
    const url = buildUrl(API_ENDPOINTS.secrets.delete(id));
    return ApiService.delete<void>(url);
  }
}
