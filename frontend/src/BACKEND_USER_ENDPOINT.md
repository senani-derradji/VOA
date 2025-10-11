# Backend User Endpoint Recommendation

## Issue
The current login flow needs the user's full information (including ID) after authentication, but the JWT token only contains `username` and `role`.

## Solution
Add a `/users/me` endpoint to your FastAPI backend to return the current authenticated user's full information.

## Implementation

Add this endpoint to your FastAPI `users.py` or `auth.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import UserModel

router = APIRouter()

@router.get(
    "/me",
    summary="Get current user",
    description="Returns the currently authenticated user's information"
)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current authenticated user's full information.
    Requires a valid JWT token in the Authorization header.
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "created_at": current_user.created_at.isoformat() if hasattr(current_user, 'created_at') else None
    }
```

## get_current_user Dependency

If you don't have a `get_current_user` dependency, add this to your `app/core/deps.py`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import UserModel
from app.core.security import SEC_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserModel:
    """
    Validate JWT token and return the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SEC_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user
```

## Register the endpoint

Make sure to include the endpoint in your API router:

```python
# In your main.py or api router setup
from app.api.v1.endpoints import users

app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"]
)
```

## Alternative: Include User ID in Token

If you prefer not to add a `/users/me` endpoint, you can include the user ID in the JWT token payload:

```python
# In your login endpoint (auth.py)
access_token = create_access_token({
    "sub": user.username,
    "user_id": user.id,  # Add this
    "role": user.role
}, access_token_expires)
```

Then update the frontend token decoder to use `user_id`:

```typescript
// In auth-service.ts getCurrentUserFromToken()
return {
  id: decoded.user_id || tempId,  // Use user_id from token
  username: decoded.sub,
  role: decoded.role,
};
```

## Recommended Approach

The `/users/me` endpoint is **recommended** because:
1. ✅ Keeps tokens lightweight
2. ✅ Allows fetching additional user data (email, profile, etc.)
3. ✅ Standard REST API pattern
4. ✅ Can be used to verify token validity
5. ✅ Easier to extend in the future

## Testing

After adding the endpoint, test it:

```bash
# Login first
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=yourpassword"

# Use the token from login response
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Expected response:
```json
{
  "id": 1,
  "username": "admin",
  "role": "admin",
  "created_at": "2025-10-10T12:00:00"
}
```

---

The frontend is already configured to use this endpoint and will fall back to token decoding if the endpoint doesn't exist yet.
