from app.models.audit import AuditModel as AUD
from sqlalchemy.orm import Session
from app.schemas.audit import Action
from app.utils.logging_logs import get_logger
from hashlib import sha256
from datetime import datetime


logger = get_logger(__name__)

def log_action(db: Session, user_id: int, action: Action):
    try:
        last_entry = (
            db.query(AUD)
            .filter(AUD.integrity_checks.isnot(None))
            .order_by(AUD.id.desc())
            .first()
        )

        previous_hash = last_entry.integrity_checks if last_entry else "1"

        data = f"{previous_hash}:{str(user_id)}:{action}"
        integrity_checks_data = sha256(data.encode()).hexdigest()

        log = AUD(
            user_id=user_id,
            action=action,
            timestamp=datetime.utcnow(),
            integrity_checks=integrity_checks_data
        )
        print(log)

        db.add(log)
        db.commit()


    except Exception as e:
        db.rollback()
        logger.error(f"Error logging action for user {user_id}, action {action}: {e}")