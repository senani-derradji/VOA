# VOA: Vaulity Ops - API Integration Guide

This guide explains how to connect the React frontend with the FastAPI backend.

## 🚀 Quick Start

### 1. Environment Setup

Create a `.env.local` file in your project root:

```bash
cp .env.example .env.local
```

Edit `.env.local`:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_ENV=development
```

### 2. Start Both Servers

#### Option A: Run Separately

**Terminal 1 - Backend (FastAPI):**
```bash
cd backend  # Your FastAPI project directory
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend (React + Vite):**
```bash
npm run dev
# or
yarn dev
```

#### Option B: Run Concurrently (Recommended)

Install concurrently:
```bash
npm install -D concurrently
```

Add to `package.json`:
```json
{
  "scripts": {
    "dev": "vite",
    "dev:backend": "cd ../backend && uvicorn main:app --reload --port 8000",
    "dev:all": "concurrently \"npm run dev\" \"npm run dev:backend\"",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

Then run:
```bash
npm run dev:all
```

### 3. Verify Connection

1. Open http://localhost:3000
2. Check the Health Check component on the dashboard
3. Status should show "Healthy" with a green indicator

## 📁 File Structure

```
src/
├── config/
│   └── api.ts                 # API configuration and endpoints
├── services/
│   ├── api.ts                 # Base API service with interceptors
│   ├── auth-service.ts        # Authentication API calls
│   ├── secrets-service.ts     # Secrets CRUD operations
│   ├── users-service.ts       # User management API calls
│   └── health-service.ts      # Health check API
├── types/
│   └── api.ts                 # TypeScript type definitions
├── hooks/
│   ├── use-api.ts            # Generic API hook
│   ├── use-secrets.ts        # Secrets-specific hooks
│   └── use-users.ts          # Users-specific hooks
├── lib/
│   ├── auth-context.tsx      # Auth context (now uses real API)
│   ├── api.ts                # API wrapper (replaces mock-api.ts)
│   └── mock-api.ts           # Old mock API (can be deleted)
└── components/
    └── health-check.tsx       # API health status component
```

## 🔧 Configuration

### API Configuration (`/config/api.ts`)

```typescript
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  apiPrefix: '/api/v1',
  timeout: 30000,
  retry: {
    maxRetries: 3,
    retryDelay: 1000,
  },
};
```

### Environment Variables

- `VITE_API_BASE_URL`: Backend API URL (default: http://localhost:8000)
- `VITE_ENV`: Environment (development/production)

## 🔌 API Service Layer

### Base API Service (`/services/api.ts`)

Provides HTTP methods with:
- ✅ Automatic token management
- ✅ Request/response interceptors
- ✅ Error handling
- ✅ Token refresh on 401
- ✅ Retry logic
- ✅ Timeout handling

```typescript
// Example usage
import { ApiService } from './services/api';

const data = await ApiService.get('/secrets/');
const created = await ApiService.post('/secrets/create', secretData);
```

### Authentication Service (`/services/auth-service.ts`)

```typescript
import { AuthService } from './services/auth-service';

// Login
const tokens = await AuthService.login({ username, password });

// Refresh token
const newTokens = await AuthService.refreshToken(refreshToken);

// Logout
await AuthService.logout();
```

### Secrets Service (`/services/secrets-service.ts`)

```typescript
import { SecretsService } from './services/secrets-service';

// List all secrets
const secrets = await SecretsService.list();

// Get specific secret (decrypted)
const secret = await SecretsService.get(1);

// Create secret
const newSecret = await SecretsService.create({
  name: 'API_KEY',
  value: 'secret123',
  env: 'production',
});

// Update secret
const updated = await SecretsService.update(1, { value: 'newvalue' });

// Delete secret
await SecretsService.delete(1);
```

### Users Service (`/services/users-service.ts`)

```typescript
import { UsersService } from './services/users-service';

// List users (admin only)
const users = await UsersService.list();

// Create user (admin only)
const user = await UsersService.register({
  username: 'newuser',
  password: 'password123',
  role: 'developer',
});

// Update user role
const updated = await UsersService.update(1, { role: 'admin' });

// Delete user
await UsersService.delete(1);
```

## 🎣 React Hooks

### Generic API Hook

```typescript
import { useApi } from './hooks/use-api';

function MyComponent() {
  const { data, error, isLoading, refetch } = useApi({
    apiFunc: () => SecretsService.list(),
    immediate: true,
  });

  return <div>{isLoading ? 'Loading...' : data?.length}</div>;
}
```

### Mutation Hook

```typescript
import { useMutation } from './hooks/use-api';

function MyComponent() {
  const { mutate, isLoading } = useMutation({
    mutationFn: (data) => SecretsService.create(data),
    onSuccess: (data) => console.log('Created!', data),
    onError: (error) => console.error('Failed!', error),
  });

  const handleCreate = () => {
    mutate({ name: 'KEY', value: 'val', env: 'dev' });
  };

  return <button onClick={handleCreate}>Create</button>;
}
```

### Secrets Hooks

```typescript
import { useSecrets, useCreateSecret } from './hooks/use-secrets';

function SecretsPage() {
  const { data: secrets, isLoading, refetch } = useSecrets();
  const { mutate: createSecret } = useCreateSecret();

  // Use secrets data...
}
```

## 🔐 Authentication Flow

1. **Login**: User enters credentials
2. **Token Storage**: Access & refresh tokens saved to localStorage
3. **API Requests**: Access token added to Authorization header
4. **Token Refresh**: On 401 error, automatically refreshes token
5. **Logout**: Clears tokens and redirects to login

### Token Management

```typescript
// Tokens are stored in localStorage:
// - voa_access_token
// - voa_refresh_token
// - voa_user (user info)

// Access token is automatically added to requests
Authorization: Bearer <access_token>

// On 401 Unauthorized:
// 1. Calls /auth/refresh with refresh_token
// 2. Updates access_token
// 3. Retries original request
// 4. If refresh fails, logs out user
```

## 🛡️ CORS Configuration

Your FastAPI backend must allow CORS from the frontend origin.

Add to your FastAPI `main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Vite dev server
        "http://localhost:5173",  # Alternative Vite port
        # Add production origins here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## ✅ Testing the Connection

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### 2. Login Test

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=yourpassword"
```

Should return:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### 3. Authenticated Request

```bash
curl http://localhost:8000/api/v1/secrets/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🆕 Adding New API Endpoints

### Step 1: Add endpoint to config

```typescript
// /config/api.ts
export const API_ENDPOINTS = {
  // ... existing endpoints
  
  newResource: {
    list: '/newresource/',
    get: (id: number) => `/newresource/${id}`,
    create: '/newresource/create',
  },
};
```

### Step 2: Create TypeScript types

```typescript
// /types/api.ts
export interface NewResource {
  id: number;
  name: string;
  // ... other fields
}

export interface CreateNewResourceRequest {
  name: string;
  // ... other fields
}
```

### Step 3: Create service

```typescript
// /services/newresource-service.ts
import { ApiService } from './api';
import { buildUrl, API_ENDPOINTS } from '../config/api';
import { NewResource, CreateNewResourceRequest } from '../types/api';

export class NewResourceService {
  static async list(): Promise<NewResource[]> {
    const url = buildUrl(API_ENDPOINTS.newResource.list);
    return ApiService.get<NewResource[]>(url);
  }

  static async create(data: CreateNewResourceRequest): Promise<NewResource> {
    const url = buildUrl(API_ENDPOINTS.newResource.create);
    return ApiService.post<NewResource>(url, data);
  }
  
  // ... other methods
}
```

### Step 4: Create hooks (optional)

```typescript
// /hooks/use-newresource.ts
import { useApi, useMutation } from './use-api';
import { NewResourceService } from '../services/newresource-service';
import { NewResource, CreateNewResourceRequest } from '../types/api';

export function useNewResources() {
  return useApi<NewResource[]>({
    apiFunc: () => NewResourceService.list(),
    immediate: true,
  });
}

export function useCreateNewResource() {
  return useMutation<NewResource, CreateNewResourceRequest>({
    mutationFn: (data) => NewResourceService.create(data),
  });
}
```

### Step 5: Use in components

```typescript
import { useNewResources, useCreateNewResource } from '../hooks/use-newresource';

function MyComponent() {
  const { data, isLoading, error, refetch } = useNewResources();
  const { mutate: create } = useCreateNewResource();

  // Use the data...
}
```

## 🐛 Troubleshooting

### Issue: Cannot connect to API

**Symptoms**: Health check shows "Unhealthy", network errors in console

**Solutions**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check CORS is configured correctly in FastAPI
3. Verify `VITE_API_BASE_URL` in `.env.local`
4. Check browser console for detailed errors

### Issue: 401 Unauthorized errors

**Symptoms**: Logged out unexpectedly, API calls fail with 401

**Solutions**:
1. Check token expiration time in backend
2. Verify refresh token endpoint is working
3. Check localStorage has tokens: `localStorage.getItem('voa_access_token')`
4. Verify JWT secret matches between frontend/backend

### Issue: CORS errors

**Symptoms**: "CORS policy" errors in browser console

**Solutions**:
1. Add frontend origin to CORS allowed origins in FastAPI
2. Ensure credentials are allowed: `allow_credentials=True`
3. Check preflight requests are handled
4. Verify headers are allowed

### Issue: Slow API responses

**Symptoms**: Long loading times, timeouts

**Solutions**:
1. Increase timeout: `API_CONFIG.timeout = 60000`
2. Check backend performance
3. Enable caching for frequently accessed data
4. Use pagination for large datasets

### Issue: Token refresh loop

**Symptoms**: Continuous refresh requests, infinite loop

**Solutions**:
1. Check refresh token expiration
2. Verify refresh endpoint doesn't require access token
3. Check token storage is working correctly

## 📊 Error Handling

All API errors follow this structure:

```typescript
interface ApiError {
  message: string;      // Human-readable error message
  status?: number;      // HTTP status code
  code?: string;        // Error code (UNAUTHORIZED, FORBIDDEN, etc.)
  details?: any;        // Additional error details from backend
}
```

Common error codes:
- `UNAUTHORIZED` (401): Invalid or expired token
- `FORBIDDEN` (403): Insufficient permissions
- `NOT_FOUND` (404): Resource not found
- `RATE_LIMIT` (429): Too many requests
- `SERVER_ERROR` (500+): Backend error
- `TIMEOUT`: Request timeout
- `NETWORK_ERROR`: Network failure

## 🔄 Migration from Mock API

The old mock API (`/lib/mock-api.ts`) has been replaced with real API calls in `/lib/api.ts`.

**What changed:**
- Same interface, different implementation
- All components import from `/lib/api.ts` instead of `/lib/mock-api.ts`
- Real HTTP calls instead of mock delays
- Proper error handling from backend

**To switch back to mock (for testing):**
1. Change imports in components from `../lib/api` to `../lib/mock-api`
2. Or create a flag in config to switch between mock and real API

## 🚀 Production Deployment

### Environment Variables

Create `.env.production`:
```env
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_ENV=production
```

### Build

```bash
npm run build
```

### Serve

```bash
npm run preview
```

### Backend Requirements

1. HTTPS enabled
2. CORS configured for production domain
3. Secure JWT secrets
4. Rate limiting enabled
5. Proper error handling
6. Logging and monitoring

## 📚 Additional Resources

- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [JWT Authentication](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [React Hooks](https://react.dev/reference/react)

## 🆘 Support

If you encounter issues:

1. Check this guide's troubleshooting section
2. Verify backend is running and accessible
3. Check browser console for errors
4. Review network tab in DevTools
5. Check backend logs for errors

## ✨ Best Practices

1. **Always use hooks**: Use `useApi` and `useMutation` instead of direct service calls
2. **Handle errors**: Always show user-friendly error messages
3. **Loading states**: Show loading indicators for better UX
4. **Token security**: Never log tokens or commit them to git
5. **Type safety**: Use TypeScript types for all API calls
6. **Error boundaries**: Wrap components in error boundaries
7. **Retry logic**: Use built-in retry for transient failures
8. **Cache wisely**: Cache frequently accessed, rarely changed data

---

**VOA: Vaulity Ops** - Secure Secrets Management Platform
