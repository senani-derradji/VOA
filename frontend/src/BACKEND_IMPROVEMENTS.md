# Backend API Improvements

## Current Issues

Your backend has a few inconsistencies that can be improved for better API design:

## 1. Use Request Bodies Instead of Query Parameters

### Current (Not RESTful):
```python
@router.post("/create")
def create_secret(
    name: str,  # Query parameter
    value: str,  # Query parameter
    env: str = "development",  # Query parameter
    ...
):
```

### Recommended (RESTful):
```python
from pydantic import BaseModel

class SecretCreate(BaseModel):
    name: str
    value: str
    env: str = "development"

@router.post("/create")
def create_secret(
    secret: SecretCreate,  # Request body
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    encrypted_value = encrypt(secret.value)
    new_secret = Secret(
        name=secret.name,
        value=encrypted_value,
        owner_id=current_user.id,
        environment=secret.env
    )
    db.add(new_secret)
    db.commit()
    db.refresh(new_secret)
    
    return {
        "id": new_secret.id,
        "name": new_secret.name,
        "env": new_secret.environment,
        "owner_id": new_secret.owner_id,
        "created_at": new_secret.created_at.isoformat() if hasattr(new_secret, 'created_at') else None
    }
```

## 2. Consistent Response Format

### Current:
```python
# Sometimes returns message
return {"message": "Secret created successfully", "secret_id": new_secret.id}

# Sometimes returns data
return {"id": secret.id, "name": secret.name, ...}
```

### Recommended:
```python
# Always return the created/updated resource
return {
    "id": new_secret.id,
    "name": new_secret.name,
    "env": new_secret.environment,
    "owner_id": new_secret.owner_id,
    "created_at": new_secret.created_at.isoformat() if hasattr(new_secret, 'created_at') else None
}
```

## 3. Add /users/me Endpoint

```python
# In users.py
@router.get("/me")
def get_current_user_info(
    current_user: UserModel = Depends(get_current_user)
):
    """Get current authenticated user's information"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "created_at": current_user.created_at.isoformat() if hasattr(current_user, 'created_at') else None
    }
```

## 4. Consistent Field Naming

Your backend uses `environment` but the frontend expects `env`. Choose one:

**Option A: Keep backend as `environment`**
```python
# Backend stays the same
environment: str
```
```typescript
// Frontend adapts (already done)
environment: data.env  // Map env to environment
```

**Option B: Change backend to `env`** (Recommended - shorter)
```python
# Change in models and schemas
env: str  # Instead of environment
```

## 5. Update Users Endpoints

### Register endpoint:
```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "viewer"

@router.post("/register")
def register(
    user: UserCreate,  # Use request body
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    if db.query(UserModel).filter(UserModel.username == user.username).first():
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = get_password_hash(user.password)
    new_user = UserModel(
        username=user.username, 
        password=hashed_password, 
        role=user.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Return the created user, not just a message
    return {
        "id": new_user.id,
        "username": new_user.username,
        "role": new_user.role,
        "created_at": new_user.created_at.isoformat() if hasattr(new_user, 'created_at') else None
    }
```

### Update role endpoint:
```python
class UserRoleUpdate(BaseModel):
    role: str

@router.put("/{user_id}")
def change_user_role(
    user_id: int,
    update_data: UserRoleUpdate,  # Use request body
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    valid_roles = ["admin", "developer", "viewer"]
    if update_data.role not in valid_roles:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    user.role = update_data.role
    db.commit()
    db.refresh(user)
    
    # Return the updated user
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "created_at": user.created_at.isoformat() if hasattr(user, 'created_at') else None
    }
```

## Summary of Changes

1. ✅ Use Pydantic models for request bodies (not query params)
2. ✅ Always return created/updated resource (not just success message)
3. ✅ Add `/users/me` endpoint
4. ✅ Consistent field naming (`env` vs `environment`)
5. ✅ Include `created_at` in all responses

## Quick Migration

If you want to keep your current API as-is, the frontend is already adapted to work with query parameters. But for better API design and future scalability, consider these improvements!

The frontend code I provided works with your **current** backend but also gracefully handles improved responses.
