# VOA: Vaulity Ops - Complete Setup Instructions

## 📋 Prerequisites

- Node.js 18+ installed
- Python 3.9+ installed
- FastAPI backend project ready
- npm or yarn package manager

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
npm install
# or
yarn install
```

### Step 2: Install Concurrently (for running both servers)

```bash
npm install -D concurrently
```

### Step 3: Create Environment File

```bash
cp .env.example .env.local
```

Edit `.env.local`:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_ENV=development
```

### Step 4: Configure Backend CORS

Add to your FastAPI `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

See `FASTAPI_CORS_SETUP.py` for complete example.

### Step 5: Update package.json

Add these scripts to your `package.json`:

```json
{
  "scripts": {
    "dev": "vite",
    "dev:backend": "cd ../backend && uvicorn main:app --reload --port 8000",
    "dev:all": "concurrently \"npm run dev\" \"npm run dev:backend\""
  }
}
```

Adjust the path in `dev:backend` to match your backend directory location.

### Step 6: Run Both Servers

```bash
npm run dev:all
```

This will start:
- Frontend on http://localhost:3000 (or 5173)
- Backend on http://localhost:8000

## ✅ Verify Setup

1. **Check Backend Health**
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status":"ok",...}`

2. **Open Frontend**
   Navigate to http://localhost:3000

3. **Check Health Component**
   The dashboard should show "API Health Status" as "Healthy" in green

4. **Test Login**
   Try logging in with your backend credentials

## 🔧 Manual Setup (if concurrent doesn't work)

### Terminal 1 - Backend
```bash
cd ../backend  # Adjust path to your backend
uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend
```bash
npm run dev
```

## 📁 Project Structure

After setup, your structure should look like:

```
your-workspace/
├── frontend/              # This React project
│   ├── src/
│   │   ├── config/       # API configuration
│   │   ├── services/     # API services
│   │   ├── hooks/        # React hooks
│   │   ├── components/   # React components
│   │   └── types/        # TypeScript types
│   ├── .env.local        # Your environment config
│   └── package.json
│
└── backend/              # Your FastAPI project
    ├── main.py
    ├── requirements.txt
    └── ...
```

## 🐛 Troubleshooting

### Issue: "Cannot connect to API"

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check CORS is configured in FastAPI
3. Verify `.env.local` has correct URL
4. Check backend logs for errors

### Issue: "CORS policy error"

**Solution:**
1. Add CORS middleware to FastAPI (see FASTAPI_CORS_SETUP.py)
2. Ensure frontend origin is in allowed origins
3. Restart backend after adding CORS

### Issue: "401 Unauthorized"

**Solution:**
1. Check your backend authentication is working
2. Verify JWT token generation
3. Check token expiration times
4. Clear browser localStorage and try again

### Issue: Port already in use

**Solution:**
```bash
# For port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# For port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

## 🔐 Backend Requirements

Your FastAPI backend should have these endpoints:

### Authentication
- `POST /api/v1/auth/login` - Login (OAuth2 form)
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - Logout (optional)

### Users
- `GET /api/v1/users/` - List users (admin)
- `POST /api/v1/users/register` - Create user (admin)
- `GET /api/v1/users/{id}` - Get user
- `PUT /api/v1/users/{id}` - Update user role
- `DELETE /api/v1/users/{id}` - Delete user
- `GET /api/v1/users/me` - Current user

### Secrets
- `GET /api/v1/secrets/` - List secrets
- `POST /api/v1/secrets/create` - Create secret
- `GET /api/v1/secrets/{id}` - Get secret (decrypted)
- `PUT /api/v1/secrets/{id}` - Update secret
- `DELETE /api/v1/secrets/{id}` - Delete secret

### Health
- `GET /health` - Health check (no auth)

## 📝 Environment Variables

### Frontend (.env.local)
```env
# Required
VITE_API_BASE_URL=http://localhost:8000

# Optional
VITE_ENV=development
```

### Backend (.env)
```env
# Example backend variables
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## 🧪 Testing the Connection

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=yourpassword"
```

### 3. List Secrets (with token)
```bash
curl http://localhost:8000/api/v1/secrets/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🎯 Next Steps

After setup:

1. ✅ Verify health check shows green
2. ✅ Test login with real credentials
3. ✅ Create a test secret
4. ✅ Test user management (if admin)
5. ✅ Review API integration docs (README_API_INTEGRATION.md)

## 📚 Documentation

- **API Integration Guide**: `README_API_INTEGRATION.md`
- **CORS Setup**: `FASTAPI_CORS_SETUP.py`
- **Package Config**: `package.json.example`

## 🆘 Getting Help

If you're stuck:

1. Check the troubleshooting section above
2. Review `README_API_INTEGRATION.md`
3. Check browser console for errors
4. Check backend logs
5. Verify environment variables

## ✨ Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Health check returns "Healthy"
- [ ] Can login successfully
- [ ] Dashboard loads with data
- [ ] Secrets page shows/creates secrets
- [ ] No CORS errors in console
- [ ] No 401/403 errors (unless expected)

---

**You're all set!** 🎉

The frontend is now connected to your FastAPI backend. Check the dashboard for the health status indicator.
