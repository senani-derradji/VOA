// Health Service
// Handles health check API calls

import { ApiService } from './api';
import { buildRootUrl } from '../config/api';
import { API_ENDPOINTS } from '../config/api';
import { HealthResponse } from '../types/api';

export class HealthService {
  /**
   * Check API health status
   * GET /health
   */
  static async check(): Promise<HealthResponse> {
    const url = buildRootUrl(API_ENDPOINTS.health);
    return ApiService.get<HealthResponse>(url, false); // No auth required
  }
}
