from app.models.audit import AuditModel as AUD
from sqlalchemy.orm import Session
from app.utils.logging_logs import get_logger
from hashlib import sha256

logger = get_logger(__name__)

def verify(db: Session):
    logs = db.query(AUD).order_by(AUD.id).all()
    previous_hash = "0"
    for log in logs:
        data = f"{str(previous_hash)}:{log.user_id}:{log.action}"
        check = sha256(data.encode()).hexdigest()
        if check != log.integrity_checks:
            logger.warning(f"Integrity broken at log ID {log.id}")
            return False
        previous_hash = check
    logger.info("Integrity check passed")
    return True
