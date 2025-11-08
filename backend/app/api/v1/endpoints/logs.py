from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.extentions.database import get_db
from app.core.deps import get_current_user
from app.models.audit import AuditModel
from app.services.audit import log_action
from app.utils.logging_logs import get_logger
from app.RBAC.roles import admin_required

logger = get_logger(__name__)

router = APIRouter()
@router.get("/logs")
def read_logs(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not admin_required(current_user, "read_logs"):
        pass

    logs = db.query(AuditModel).all()
    log_action(db, current_user.id, "read_logs")
    return logs
