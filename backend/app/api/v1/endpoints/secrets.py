from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.secrets import SecretsModel as Secret
from app.models.user import UserModel as User
from app.core.encryption import encrypt, decrypt
from app.services.audit import log_action
from app.schemas.secrets import SecretsUpdate


router = APIRouter()


@router.post(
    "/create",
    summary="Create a new secret",
    description="Creates and stores a new secret for the authenticated user."
)
def create_secret(
    name: str,
    value: str,
    env: str = "dev",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if db.query(Secret).filter_by(name=name).first():
        raise HTTPException(status_code=400, detail="Secret name already exists")
    
    if env not in ["dev", "test" ,"prod"]:
        raise HTTPException(status_code=400, detail="Invalid environment")
    

    encrypted_value = encrypt(value)
    new_secret = Secret(
        name=name,
        value=encrypted_value,
        owner_id=current_user.id,
        environment=env
    )
    db.add(new_secret)
    db.commit()
    db.refresh(new_secret)

    log_action(db, current_user.id, f"create_secret ({name})")
    return {"message": "Secret created successfully", "secret_id": new_secret.id}



@router.get(
    "/",
    summary="Get all secrets",
    description="Retrieves all secrets accessible by the current user."
)
def get_all_secrets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all secrets"""
    if current_user.role == "admin":
        secrets = db.query(Secret).all()
    elif current_user.role == "developer":
        secrets = db.query(Secret).filter(Secret.owner_id == current_user.id).all()
    else:
        raise HTTPException(status_code=403, detail="Access denied")

    result = []
    for secret in secrets:
        result.append({
            "id": secret.id,
            "name": secret.name,
            "env": getattr(secret, 'environment', 'development'),
            "owner_id": secret.owner_id
        })

    log_action(db, current_user.id, f"get_all_secrets")
    # print(f"Current user: {current_user.username}, role: {current_user.role}, id: {current_user.id}")

    return result



@router.get(
    "/{secret_id}",
    summary="Get a specific secret",
    description="Retrieves a secret by its ID if the user has permission."
)
def get_secret(
    secret_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    secret = db.query(Secret).filter_by(id=secret_id).first()

    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")

    if current_user.role == "admin" or secret.owner_id == current_user.id:
        decrypted_value = decrypt(secret.value)
    else:
        raise HTTPException(status_code=403, detail="Not authorized to view this secret")

    log_action(db, current_user.id, f"get_secret ({secret.name})")
    return {
        "id": secret.id,
        "name": secret.name,
        "value": decrypted_value,
        "env": getattr(secret, 'environment', 'development')
    }

@router.put(
    "/{secret_id}",
    summary="Update a secret",
    description="Updates an existing secret if the user is the owner or an admin."
)
def update_secret(
    secret_id: int,
    secret_data: SecretsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    secret = db.query(Secret).filter_by(id=secret_id).first()

    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")

    if current_user.role != "admin" and secret.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if secret_data.value is not None:
        secret.value = encrypt(secret_data.value)
    if secret_data.name is not None:
        secret.name = secret_data.name
    if secret_data.environment is not None:
        secret.environment = secret_data.environment

    db.commit()
    db.refresh(secret)
    log_action(db, current_user.id, f"update_secret ({secret.name})")

    return {"message": "Secret updated successfully"}



@router.delete(
    "/{secret_id}",
    summary="Delete a secret",
    description="Deletes a secret by ID. Only admins or the owner can delete it."
)
def delete_secret(
    secret_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    secret = db.query(Secret).filter_by(id=secret_id).first()

    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this secret")
    
    db.delete(secret)
    db.commit()
    log_action(db, current_user.id, f"delete_secret ({secret.name})")


    return {"message": "Secret deleted successfully"}