from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.audit import AuditModel
from app.services.audit import log_action

router = APIRouter()
@router.get("/logs")
def read_logs(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        log_action(db, current_user.id, "Access logs : access_forbidden")
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    logs = db.query(AuditModel).all()
    return logs
