from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.secrets import SecretsModel as Secret
from app.models.user import UserModel as User
from app.core.encryption import encrypt, decrypt
from app.services.audit import log_action
from app.schemas.secrets import (SecretsUpdate, 
                                 SecretsCreate)
from app.utils.logging_logs import get_logger


logger = get_logger(__name__)
router = APIRouter()


@router.post(
    "/create",
    summary="Create a new secret",
    description="Creates and stores a new secret for the authenticated user."
)
def create_secret(
    data_form: SecretsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    name = data_form.name
    env = data_form.environment
    value = data_form.value

    if db.query(Secret).filter_by(name=name).first():
        log_action(db, current_user.id, f"secret_exists ({name})")
        raise HTTPException(status_code=400, detail="Secret name already exists")

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

    log_action(db, current_user.id, f"create_secret")
    logger.info(f"Secret created: {new_secret.name}")

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
    if current_user.role == "admin": 
        logger.info(f"Admin {current_user.username} user accessing secrets")
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
            "owner_id": secret.owner_id
        })

    log_action(db, current_user.id, "list_secrets")

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

    if not secret: raise HTTPException(status_code=404, detail="Secret not found")

    if current_user.role == "admin": decrypted_value = decrypt(secret.value)[:5] + "..."*5

    else: 
        decrypted_value = secret.value
        raise HTTPException(status_code=403, detail="Not authorized to view this secret")
    

    log_action(db, current_user.id, f"read_secret")
    logger.info(f"Secret accessed: {secret.name}")


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

    if current_user.role != "admin":
        logger.warning(f"{current_user.username} Tried to update Secret {secret.name}")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if secret_data.value is not None:
        secret.value = encrypt(secret_data.value)
    if secret_data.name is not None:
        secret.name = secret_data.name
    if secret_data.environment is not None:
        secret.environment = secret_data.environment

    db.commit()
    db.refresh(secret)
    log_action(db, current_user.id, f"update_secret")
    logger.info(f"{current_user.username} updated Secret : {secret.name}")


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
        logger.warning(f"{current_user.username} Tried to delete Secret {secret.name}")
        raise HTTPException(status_code=403, detail="Not authorized to delete this secret")
    
    db.delete(secret)
    db.commit()
    log_action(db, current_user.id, f"delete_secret")
    logger.info(f"{current_user.username} deleted Secret : {secret.name}")

    return {"message": "Secret deleted successfully"}