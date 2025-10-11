# CORS Configuration Fix

## Problem
The frontend is getting 400 Bad Request errors for OPTIONS (preflight) requests, and the backend needs to allow port 5173 (Vite's alternative port).

## Solution

Update your FastAPI `main.py` CORS configuration:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="VOA : VAULITY OPS API",
    description="Secrets Manager API for secure credential and secret management.",
    version="1.0.0"
)

# IMPORTANT: Add CORS middleware BEFORE @app.get("/health")
origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Add this - Vite's alternative port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://localhost:8000",  # Allow same origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods including OPTIONS
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"],
)

# Health check should be AFTER CORS middleware
@app.get("/health")
def health_check():
    return {"status": "ok"}

# ... rest of your app code
```

## Key Points

1. **Add port 5173** - Vite uses this port sometimes
2. **CORS before routes** - Middleware must be added before route definitions
3. **Allow OPTIONS** - The `allow_methods=["*"]` includes OPTIONS for preflight
4. **Restart backend** - After making changes, restart your FastAPI server

## Testing

After updating, test CORS:

```bash
# Test preflight request
curl -X OPTIONS http://localhost:8000/health \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET" \
  -v

# Should return 200 with CORS headers
```

## Common CORS Errors and Solutions

### 400 Bad Request on OPTIONS
**Cause**: CORS middleware not configured before routes
**Fix**: Move `app.add_middleware()` before route definitions

### "CORS policy: No 'Access-Control-Allow-Origin' header"
**Cause**: Origin not in allowed list
**Fix**: Add your frontend URL to `origins` list

### "CORS policy: The response had HTTP status code 405"
**Cause**: OPTIONS method not allowed
**Fix**: Ensure `allow_methods=["*"]` is set

## Verify Frontend Port

Check which port your Vite dev server is using:

```bash
# In your frontend terminal, you should see:
# VITE v5.x.x ready in xxx ms
# ➜ Local:   http://localhost:3000  # or 5173
```

Make sure this port is in the `origins` list!
