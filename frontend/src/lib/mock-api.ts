// Mock API for VOA Secrets Manager
// In production, replace with actual API calls to FastAPI backend

export interface Secret {
  id: number;
  name: string;
  value: string;
  env: 'development' | 'staging' | 'production';
  owner_id: number;
  created_at: string;
}

export interface User {
  id: number;
  username: string;
  role: 'admin' | 'developer' | 'viewer';
  created_at: string;
}

// Mock data storage
let mockSecrets: Secret[] = [
  {
    id: 1,
    name: 'DB_PASSWORD',
    value: 'super_secret_password_123',
    env: 'production',
    owner_id: 1,
    created_at: new Date().toISOString(),
  },
  {
    id: 2,
    name: 'API_KEY',
    value: 'sk_live_abc123xyz789',
    env: 'production',
    owner_id: 1,
    created_at: new Date().toISOString(),
  },
  {
    id: 3,
    name: 'REDIS_URL',
    value: 'redis://localhost:6379',
    env: 'development',
    owner_id: 2,
    created_at: new Date().toISOString(),
  },
  {
    id: 4,
    name: 'STRIPE_SECRET',
    value: 'sk_test_xyz123',
    env: 'staging',
    owner_id: 1,
    created_at: new Date().toISOString(),
  },
  {
    id: 5,
    name: 'JWT_SECRET',
    value: 'my-super-secret-jwt-key',
    env: 'production',
    owner_id: 1,
    created_at: new Date().toISOString(),
  },
];

let mockUsers: User[] = [
  {
    id: 1,
    username: 'admin',
    role: 'admin',
    created_at: new Date().toISOString(),
  },
  {
    id: 2,
    username: 'developer',
    role: 'developer',
    created_at: new Date().toISOString(),
  },
  {
    id: 3,
    username: 'viewer',
    role: 'viewer',
    created_at: new Date().toISOString(),
  },
];

// Helper to simulate API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Secrets API
export const secretsApi = {
  list: async (): Promise<Secret[]> => {
    await delay(300);
    return [...mockSecrets];
  },

  get: async (id: number): Promise<Secret> => {
    await delay(200);
    const secret = mockSecrets.find(s => s.id === id);
    if (!secret) throw new Error('Secret not found');
    return { ...secret };
  },

  create: async (data: Omit<Secret, 'id' | 'created_at'>): Promise<Secret> => {
    await delay(400);
    const newSecret: Secret = {
      ...data,
      id: Math.max(...mockSecrets.map(s => s.id), 0) + 1,
      created_at: new Date().toISOString(),
    };
    mockSecrets.push(newSecret);
    return newSecret;
  },

  update: async (id: number, data: Partial<Omit<Secret, 'id' | 'created_at'>>): Promise<Secret> => {
    await delay(300);
    const index = mockSecrets.findIndex(s => s.id === id);
    if (index === -1) throw new Error('Secret not found');
    mockSecrets[index] = { ...mockSecrets[index], ...data };
    return mockSecrets[index];
  },

  delete: async (id: number): Promise<void> => {
    await delay(300);
    mockSecrets = mockSecrets.filter(s => s.id !== id);
  },
};

// Users API
export const usersApi = {
  list: async (): Promise<User[]> => {
    await delay(300);
    return [...mockUsers];
  },

  create: async (username: string, password: string, role: 'admin' | 'developer' | 'viewer'): Promise<User> => {
    await delay(400);
    const newUser: User = {
      id: Math.max(...mockUsers.map(u => u.id), 0) + 1,
      username,
      role,
      created_at: new Date().toISOString(),
    };
    mockUsers.push(newUser);
    return newUser;
  },

  update: async (id: number, role: 'admin' | 'developer' | 'viewer'): Promise<User> => {
    await delay(300);
    const index = mockUsers.findIndex(u => u.id === id);
    if (index === -1) throw new Error('User not found');
    mockUsers[index].role = role;
    return mockUsers[index];
  },

  delete: async (id: number): Promise<void> => {
    await delay(300);
    mockUsers = mockUsers.filter(u => u.id !== id);
  },
};
