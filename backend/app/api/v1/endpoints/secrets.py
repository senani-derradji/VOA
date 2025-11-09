from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.extentions.database import get_db
from app.core.deps import get_current_user
from app.models.secrets import SecretsModel as Secret, SecretVersionModel as SecretVersion
from app.models.user import UserModel as User
from app.core.encryption import encrypt, decrypt
from app.services.audit import log_action
from app.schemas.secrets import SecretsUpdate, SecretsCreate
from app.RBAC.roles import admin_required, CEO_required
from app.utils.logging_logs import get_logger
from datetime import datetime

logger = get_logger(__name__)
router = APIRouter()

@router.post("/create", summary="Create a new secret")
def create_secret(
    data_form: SecretsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    name = data_form.name
    env = data_form.environment
    value = data_form.value

    if db.query(Secret).filter_by(name=name).first():
        logger.warning(f"Secret name already exists - {name}")
        raise HTTPException(status_code=400, detail="Secret name already exists")

    if current_user.role != "admin":
        user_secret_count = db.query(Secret).filter_by(owner_id=current_user.id).count()
        if user_secret_count >= 10:
            logger.warning(f"Secret limit reached for user {current_user.id}")
            raise HTTPException(status_code=400, detail="Secret limit reached")

    encrypted_value = encrypt(value)
    logger.warning(f"Secret_AFTER_ENCRYPT : {encrypted_value}")
    new_secret = Secret(
        name=name,
        value=encrypted_value,
        owner_id=current_user.id,
        environment=env
    )
    db.add(new_secret)
    db.commit()
    db.refresh(new_secret)

    new_version = SecretVersion(
        secret_id=new_secret.id,
        value=encrypted_value
    )
    db.add(new_version)
    db.commit()

    log_action(db, current_user.id, f"create_secret")
    logger.info(f"Secret created by {current_user.username} - {name}")

    return {"message": "Secret created successfully", "secret_id": new_secret.id, "version": 1}


@router.get("/", summary="Get all secrets")
def get_all_secrets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if admin_required(current_user, "get_all_secrets"):
        secrets = db.query(Secret).all()
    else:
        secrets = db.query(Secret).filter_by(owner_id=current_user.id).all()

    results = [ {"id": s.id, "name": s.name, "env": s.environment, "owner": s.owner_id} for s in secrets ]
    log_action(db, current_user.id, "list_secrets")
    logger.info(f"Secrets listed by - {current_user.username}")
    return results


@router.get("/{secret_name}", summary="Get a secret (latest version)")
def get_secret(
    secret_name,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    secret = db.query(Secret).filter_by(name=secret_name).first()
    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")

    if not admin_required(current_user, f"get_secret_{secret.name}"):
        raise HTTPException(status_code=403, detail="Not authorized to view this secret")

    latest_version = (
        db.query(SecretVersion)
        .filter_by(secret_id=secret.id)
        .order_by(SecretVersion.version_number.desc())
        .first()
    )

    decrypted_value = decrypt(latest_version.value)

    log_action(db, current_user.id, f"read_secret")
    logger.info(f"Secret read by - {current_user.username} - {secret.name}")
    return {
        "id": secret.id,
        "name": secret.name,
        "environment": secret.environment,
        "latest_version": latest_version.version_number,
        "value": decrypted_value
    }


@router.get("/versions/{secret_id}", summary="Get all versions of a secret")
def get_secret_versions(
    secret_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    secret = db.query(Secret).filter_by(id=secret_id).first()
    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")

    if not admin_required(current_user, f"get_secret_versions_{secret.name}"):
        raise HTTPException(status_code=403, detail="Not authorized")

    versions = (db.query(SecretVersion).filter_by(secret_id=secret.id).order_by(SecretVersion.version_number.desc()).all())

    version_list = [
        {
            "version": v.version_number,
            "created_at": v.created_at,
            "value_preview": decrypt(v.value) if CEO_required(current_user, f"get_secret_versions_{secret.name}") else decrypt(v.value)[:4] + "***"
        }
        for v in versions
    ]

    log_action(db, current_user.id, f"list_secrets_versions")
    logger.info(f"Secret versions listed by - {current_user.username} - {secret.name}")
    return {"secret_id": secret.id, "versions": version_list}


@router.put("/{secret_id}", summary="Update a secret (new version)")
def update_secret(
    secret_id: int,
    data: SecretsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    secret = db.query(Secret).filter_by(id=secret_id).first()
    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")

    if not admin_required(current_user, f"update_secret_{secret.name}") and secret.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if data.value:
        encrypted_value = encrypt(data.value)
        secret.value = encrypted_value
        last_version = (db.query(SecretVersion).filter_by(secret_id=secret.id).order_by(SecretVersion.version_number.desc()).first())
        if not last_version: new_version_number = 1
        else: new_version_number = (last_version.version_number if last_version else 0) + 1
        new_version = SecretVersion(secret_id=secret.id, version_number=new_version_number, value=encrypted_value,created_at=datetime.utcnow())
        db.add(new_version)

    if data.name:
        secret.name = data.name
    if data.environment:
        secret.environment = data.environment


    db.commit()
    db.refresh(secret)
    log_action(db, current_user.id, f"update_secret")
    logger.info(f"Secret updated by - {current_user.username} - {secret.name}")

    return {"message": "Secret updated successfully", "new_version": new_version_number}


@router.delete("/{secret_id}", summary="Delete a secret and its versions")
def delete_secret(
    secret_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    secret = db.query(Secret).filter_by(id=secret_id).first()
    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")

    if not admin_required(current_user, f"delete_secret_{secret.name}") and secret.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(secret) # when the admin delete the main secret , all versions will deleted also (cascade in models relationship)
    db.commit()

    log_action(db, current_user.id, f"delete_secret")
    logger.info(f"Secret deleted by - {current_user.username} - {secret.name}")

    return {"message": f"Secret '{secret.name}' and its versions deleted successfully"}
