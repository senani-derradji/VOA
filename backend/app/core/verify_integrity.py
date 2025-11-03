from sqlalchemy.orm import Session
import os,sys
from hashlib import sha256

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.audit import AuditModel as AUD
from app.utils.logging_logs import get_logger


logger = get_logger(__name__)

def verify(db: Session):
    logs = db.query(AUD).order_by(AUD.id).all()
    if len(logs) <= 2:
        logger.warning("No logs <= 2")
        return False

    for i in range(len(logs) - 1):
        try:
            log = logs[i]
            next_log = logs[i + 1]
            previous_hash = log.integrity_checks if log.integrity_checks else "0"
            data = f"{str(previous_hash)}:{str(log.user_id)}:{log.action}"
            check = sha256(data.encode()).hexdigest()
            if check != next_log.integrity_checks:
                logger.warning(f"Integrity broken at log ID {log.id}")
                return False
        except Exception as e:
            logger.error(f"Integrity check failed: {e}")
            return False

    logger.info("Integrity check passed")
    return True