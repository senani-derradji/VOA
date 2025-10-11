// Real API implementation replacing mock-api.ts
// This file provides the same interface but calls the actual FastAPI backend

import { SecretsService } from '../services/secrets-service';
import { UsersService } from '../services/users-service';
import { Secret, User, CreateSecretRequest, UpdateSecretRequest, RegisterUserRequest } from '../types/api';

// Helper to simulate API delay (can be removed in production)
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Secrets API
export const secretsApi = {
  list: async (): Promise<Secret[]> => {
    const secrets = await SecretsService.list();
    // Add missing fields if not present
    return secrets.map(secret => ({
      ...secret,
      value: secret.value || '',
      created_at: secret.created_at || new Date().toISOString(),
    }));
  },

  get: async (id: number): Promise<Secret> => {
    const secret = await SecretsService.get(id);
    return {
      ...secret,
      created_at: secret.created_at || new Date().toISOString(),
    };
  },

  create: async (data: Omit<Secret, 'id' | 'created_at'>): Promise<Secret> => {
    const createData: CreateSecretRequest = {
      name: data.name,
      value: data.value,
      env: data.env,
    };
    const result = await SecretsService.create(createData);
    // Backend returns {message, secret_id}, transform to Secret
    return {
      id: (result as any).secret_id || 0,
      name: data.name,
      value: data.value,
      env: data.env,
      owner_id: data.owner_id,
      created_at: new Date().toISOString(),
    };
  },

  update: async (id: number, data: Partial<Omit<Secret, 'id' | 'created_at'>>): Promise<Secret> => {
    await SecretsService.update(id, data);
    // Backend returns {message}, fetch the updated secret
    return SecretsService.get(id);
  },

  delete: async (id: number): Promise<void> => {
    return SecretsService.delete(id);
  },
};

// Users API
export const usersApi = {
  list: async (): Promise<User[]> => {
    const users = await UsersService.list();
    // Add missing created_at field if not present
    return users.map(user => ({
      ...user,
      created_at: user.created_at || new Date().toISOString(),
    }));
  },

  create: async (username: string, password: string, role: 'admin' | 'developer' | 'viewer'): Promise<User> => {
    const data: RegisterUserRequest = {
      username,
      password,
      role,
    };
    await UsersService.register(data);
    // Backend returns {message}, return a mock user object
    // In production, you should fetch the created user
    const users = await UsersService.list();
    const newUser = users.find(u => u.username === username);
    if (newUser) return newUser;
    
    // Fallback
    return {
      id: Date.now(),
      username,
      role,
      created_at: new Date().toISOString(),
    };
  },

  update: async (id: number, role: 'admin' | 'developer' | 'viewer'): Promise<User> => {
    await UsersService.update(id, { role });
    // Backend returns {message}, fetch updated user list
    const users = await UsersService.list();
    const updatedUser = users.find(u => u.id === id);
    if (updatedUser) return updatedUser;
    
    // Fallback
    return {
      id,
      username: 'unknown',
      role,
      created_at: new Date().toISOString(),
    };
  },

  delete: async (id: number): Promise<void> => {
    return UsersService.delete(id);
  },
};

// Re-export types for convenience
export type { Secret, User };
